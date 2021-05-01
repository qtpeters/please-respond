#!/usr/bin/env python3

import requests
import time
import concurrent.futures
import threading

from urllib.parse import unquote
from os import system
from os.path import exists
from time import sleep
from json import loads
from threading import Thread, Lock

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

class Aggregator( Thread ):

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

class PleaseRespond( object ):

    def __init__( self, seconds ):
        self.seconds = seconds
        self.ag = Aggregator()

    def stream( self ):

        """
        stream() starts the collection of RSVPs from Meetup.com

        I've commented every line because threading can be confusing

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

def format_input( seconds ):
    try:
        return int( seconds )
    except:
        print( "This (%s) is not acceptable input, please enter an integer" % seconds )
        exit( 1 )

def main():

    # Get the duration from the user and make sure it's what we expect
    seconds = input( "Specify the number of seconds[60]: " )
    i_seconds = format_input( seconds )

    # Start collecting RSVPs from Meetup.com
    please_respond = PleaseRespond( i_seconds )
    please_respond.stream()

    # Get the report and display it.
    num_venues = please_respond.report()
    print( "There were a total of %d RSVPs" % num_venues )


# Run this program only as a script.
if __name__ == "__main__":
    main()


