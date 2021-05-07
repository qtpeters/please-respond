import unittest
import threading
from time import sleep
from pleaserespond import flag

# Here is a test thread we can use to try
# out the flag class.
class TestThread( threading.Thread ):

    def __init__( self, flag ):

        threading.Thread.__init__( self )

        self.flag = flag
        self.centiseconds = 0


    def run( self ):
        while True:
            if self.flag.keep_going():
                sleep( 0.01 )
                self.centiseconds += 1
            else: break

    def get_centiseconds( self ):
        return self.centiseconds

class TestFlag( unittest.TestCase ):

    def test_flag( self ):

        # create a flag and a thread
        f = flag.Flag()
        tt = TestThread( f )

        # Start the thread and sleep for four seconds
        tt.start()
        sleep( 0.1 )

        # Stop the flag and sleep a bit longer
        f.stop()
        sleep( 0.5 )

        # Join the thead
        tt.join()

        # Get how long the thread was running
        # before the flag told it to stop
        s = tt.get_centiseconds()

        # This is a bit of a fuzzy test, but it should prove the
        # flag works if we sleep for 0.6s total and the thread
        # was working for only 0.1s
        self.assertTrue( s in [ 9, 10, 11 ] )

if __name__ == '__main__':
    unittest.main()