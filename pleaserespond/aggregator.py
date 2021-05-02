
import threading
import requests

from json import loads
from pleaserespond.flag import Flag

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
        self.total = 0
        self.latest_event = ()
        self.latest_url = ()
        self.top_three_num_rsvps = {}

    def consume( self, data ):

        # Decode the data into a json string
        json_str = data.decode( "utf-8"  )
        entry = loads( json_str )

        # Update the metrics

        # Add one to the # of RSVPs
        # TODO this is wrong if there is more than one RSVP per venue
        self.total += 1

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
        return self.total

    def have_enough( self ):

        """ This method is run when enough
        data has been collected and it's time
        to report """

        self.flag.stop()

