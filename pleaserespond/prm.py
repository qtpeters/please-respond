
from time import sleep
from pleaserespond.aggregator import Aggregator

class PleaseRespond( object ):

    def __init__( self, seconds ):
        self.seconds = seconds
        self.ag = Aggregator()

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

        report = "%d,%s,%s,%s,%d,%s,%d,%s,%d" % (
            total, latest_date, latest_url, 
            no1.strip(), vl1, no2.strip(), 
            vl2, no3.strip(), vl3
        )

        return report

        