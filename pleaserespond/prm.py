
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
        return self.ag.get_data()

        