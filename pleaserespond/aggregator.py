
import threading
import requests
import pytz

from json import loads
from datetime import datetime
from pleaserespond.flag import Flag
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim

class Aggregator( threading.Thread ):

    """
    The Aggregator is Thread who's function it is to gather
    the data from the Meetup.com RSVP Service.

    This class contains the business logic
    to create the deliverable report

    """

    def __init__( self ):

        threading.Thread.__init__( self )

        self.flag = Flag()
        self.rsvp_url = "http://stream.meetup.com/2/rsvps"

        now = datetime.now()
        GMT_tz = pytz.timezone( "Europe/London" )
        default_dt = GMT_tz.localize( now )

        self.data = {
            
            # If updated, "updated" will be true.
            "updated": False,

            # Total number of RSVPs
            "total": 0,
            
            # Initial data for the latest RSVP
            "latest": {
                "url": "No RSVPs received...",
                "date": default_dt
            },

            # The number of rsvps per country
            "npc": {}
        }

    def _get_coords( self, entry ):
        
        """ Get the lat/lon from the data """

        lat = 0.0
        lon = 0.0

        try:
            # Try to get the lat/lon from the venue
            venue = entry[ "venue" ]
            lat = venue[ "lat" ]
            lon = venue[ "lon" ]
        except:
            try:
                # If the venue doesn't exist, try the group.
                group = entry[ "group" ]
                lat = group[ "group_lat"]
                lon = group[ "lon" ]
            except:

                # If the group is missiong something, then we give up.
                # I hope it's a swimming group in Africa. 
                pass
        
        return ( lat, lon )

    def _get_tz( self, entry ):

        # Extract the values

        ( lat, lon ) = self._get_coords( entry )

        # Use a handy TimezonFinder to get the timezone
        tz_finder = TimezoneFinder()
        tz = tz_finder.timezone_at( lng=lon, lat=lat )

        return pytz.timezone( tz )

    def _get_country( self, entry ):

        ( lat, lon ) = self._get_coords( entry )

        # Use GeoPy's Nominatim class to determine the rest of the information
        # about the location. Another note is that we can use the Nominatim
        # class to find the timezone somehow, but the TimezoneFinder() is already
        # working, so maybe later.
        geolocator = Nominatim( user_agent="pleaserespond" )
        location = geolocator.reverse( "%f,%f" % ( lat, lon ) )

        if location: return location.address.split(",")[-1]
        else: return "Nowhere"


    def consume( self, data ):

        """
        This method receives the data from the Meetup.com stream and
        it will be run each time this client receives data. 
        """

        # Decode the data into a json string
        json_str = data.decode( "utf-8"  )
        entry = loads( json_str )

        # Get the event and the timezone it's happening in
        event = entry[ "event" ]
        tz = self._get_tz( entry )

        # Get the event datetime from the timestamp 
        ts_micro = event[ "time" ]

        # Microseconds?? OMG, why?
        ts_milli = ts_micro/1000.0
        incoming_dt_tzu = datetime.fromtimestamp( ts_milli )
        
        # Now the incoming datetime will be timezone aware
        # and we can do a more realistic comparison of the times
        incoming_dt = tz.localize( incoming_dt_tzu )
        existing_dt = self.data["latest"][ "date" ]

        if not existing_dt or incoming_dt > existing_dt:            
            self.data[ "updated" ] = True
            self.data["latest"][ "url" ] = event[ "event_url" ]
            self.data["latest"][ "date" ] = incoming_dt

        #
        # Update the metrics
        #

        country = self._get_country( entry )
        num_per_country = self.data[ "npc" ]

        try:
            current_num = num_per_country[ country ]
            num_per_country[ country ] = current_num + 1
        except:
            num_per_country[ country ] = 1

        # Add one to the # of RSVPs
        self.data["total"] += 1

    def run( self ):
        s = requests.Session()
        with s.get( self.rsvp_url, headers=None, stream=True ) as resp:
            for line in resp.iter_lines():

                # As long as there is a line from the stream and we haven't
                # collected enough data yet, keep collecting.
                if line and self.flag.keep_going():
                    self.consume( line )
                else: break

    def get_data( self ):
        return self.data

    def have_enough( self ):

        """ This method is run when enough
        data has been collected and it's time
        to report """

        self.flag.stop()

