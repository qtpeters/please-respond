
from threading import Lock

class Flag( object ):

    """
    This Flag class creates a nice interface
    to verify the Aggregator should still be running,
    or if it's has enough data to report

    Flags are "Single Use", so once they are stopped, a new
    Flag must be created for use.

    """

    def __init__( self ):
        self.go = True
        self.lock = Lock()

    def stop( self ):
        with self.lock:
            self.go = False

    def keep_going( self ):
        with self.lock:
            return self.go

