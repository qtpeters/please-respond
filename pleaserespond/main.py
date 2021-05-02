
from pleaserespond.prm import PleaseRespond
from sys import exit

def format_input( seconds ):
    try:
        if seconds == "":
            seconds = 60
        return int( seconds )
    except:
        print( "This (%s) is not acceptable input, please enter an integer" % seconds )
        exit( 1 )

def main( seconds ):

    # Get the duration from the user and make sure it's what we expect
    if not seconds:
        seconds = input( "Specify the number of seconds[60]: " )
    i_seconds = format_input( seconds )

    # Start collecting RSVPs from Meetup.com
    please_respond = PleaseRespond( i_seconds )
    please_respond.stream()

    # Get the report and display it.
    num_venues = please_respond.report()
    print( "There were a total of %d RSVPs" % num_venues )

