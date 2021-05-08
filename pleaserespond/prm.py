
from time import sleep
from pleaserespond import aggregator
import country_converter as coco

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

        # Some of the Chinese names result in "Not Found"
        # At least it's a lot better than I could do with 
        # a Python dictionary
        return self.cc.convert( names=country, to='ISO2' )
        
    def stream( self ):

        """
        stream() starts the collection of RSVPs from Meetup.com
        """

        print( "Streaming RSVPs for %d seconds" % self.seconds )

        # Start the thread that streams from Meetup.com
        self.ag.start()

        # Sleep for the number of requested seconds
        sleep( self.seconds )

        # Tell the Aggregator to stop collectiong
        self.ag.have_enough()

        # Join the threads and the stream is finished
        self.ag.join()

    def report( self ):

        def _prep( country_name ):
            cn = country_name.strip()
            return self._map_country( country_name ).lower()

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

        # Get the no1, no2 and no3 most RSVPs per country
        npc = data[ "npc" ]
        npc_sorted = sorted( npc, key=npc.get )

        no1 = npc_sorted.pop()
        vl1 = npc[ no1 ]
        
        no2 = npc_sorted.pop()
        vl2 = npc[ no2 ]

        no3 = npc_sorted.pop()
        vl3 = npc[ no3 ]

        # Build the report
        report = "%d,%s,%s,%s,%d,%s,%d,%s,%d" % (
            total, latest_date, latest_url, 
            _prep( no1 ), vl1, 
            _prep( no2 ), vl2, 
            _prep( no3 ), vl3
        )

        return report

        