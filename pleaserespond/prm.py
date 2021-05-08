
import country_converter as coco
from time import sleep
from pleaserespond import aggregator
from datetime import datetime 

NO_COUNTRY = "no_country"

class PleaseRespond( object ):

    """ 
    PleaseRespond coordinates the activity of the streaming data
    and builds the report from the data collected by the Aggregator
    """

    def __init__( self, seconds ):

        """
        Sets the initial number of seconds and initilize the Aggregator
        """

        self.seconds = seconds
        self.ag = aggregator.Aggregator()
        self.cc = coco.CountryConverter()

    def _map_country( self, country ):

        """
        Maps a country name to it's ISO2 equivalent ( two letter name )
        """

        country = country.strip()
        f_country = NO_COUNTRY

        # Some of the Chinese names result in "Not Found"
        # At least it's a lot better than I could do with 
        # a Python dictionary.
        if country != NO_COUNTRY: 
            result = self.cc.convert( names=country, to='ISO2' )
            
            # country_converter was unable to find a country,
            # so we can try and grab the first two letters.
            if result == "not_found":
                f_country = country[0:2]
            else:
                f_country = result

        return f_country
        
    def stream( self ):

        """
        stream() starts the collection of RSVPs from Meetup.com
        """

        print( f"Streaming RSVPs for {self.seconds} seconds" )

        # Start the thread that streams from Meetup.com
        self.ag.start()

        # Sleep for the number of requested seconds
        sleep( self.seconds )

        # Tell the Aggregator to stop collectiong
        self.ag.have_enough()

        # Join the threads and the stream is finished
        self.ag.join()

    def _get_winner( self, npc_sorted, npc ):

        """
        Returns the country and associated value from the
        top of the list.
        """

        country = NO_COUNTRY
        num = 0

        try:
            country = npc_sorted.pop()
            num = npc[ country ]
        except: pass

        return ( country, num )

    def report( self ):

        def _prep( country_name ):

            """
            A small tool to map the country names to to letter
            versions, clean off the whitespace and change to lower
            case as specified in the requirements.
            """

            mapped_country_name = self._map_country( country_name )
            clean_mapped_country_name = mapped_country_name.strip()
            return clean_mapped_country_name.lower()
             

        """
        Creates the report that will be displayed to 
        the user after data collection and aggregation
        """

        data = self.ag.get_data()

        # Extract the total number of RSVPs
        total = data[ "total" ]

        # Get the latest url and date
        latest = data[ "latest" ]
        latest_url = latest[ "url" ]
        latest_date = latest[ "date" ]

        # Change to actual datetime object
        formatted_date = latest_date.strftime( "%m-%d-%Y %H:%M" )

        # Get the no1, no2 and no3 most RSVPs per country
        # "npc" = number per country: npc[ "<Country Name>" ] = <#RSVPs per country>
        npc = data[ "npc" ]
        npc_sorted = sorted( npc, key=npc.get )


        ( no1, vl1 ) = self._get_winner( npc_sorted, npc )
        ( no2, vl2 ) = self._get_winner( npc_sorted, npc )
        ( no3, vl3 ) = self._get_winner( npc_sorted, npc )


        # Build the report
        report =  f"{total},{formatted_date},{latest_url},{_prep( no1 )},{vl1},{_prep( no2 )},{vl2},{_prep( no3 )},{vl3}"

        return report

        