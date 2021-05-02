
from pleaserespond.prm import PleaseRespond
from sys import exit

DEFAULT_SEC = 60

def format_input( seconds ):

    """
    Verifies that the value passed in is an integer 
    and if nothing is poassed in, the default is set.
    """

    try:
        if seconds == "":
            seconds = DEFAULT_SEC
        return int( seconds )
    except:
        print( "This (%s) is not acceptable input, please enter an integer" % seconds )
        exit( 1 )

def main( seconds ):

    """
    The main method. This gathers user 
    input and starts the application.
    After the process is finished, it
    displays the report to the user.
    """

    # Get the duration from the user and make sure it's what we expect
    if not seconds:
        seconds = input( "Specify the number of seconds[%s]: " % DEFAULT_SEC )
    i_seconds = format_input( seconds )

    # Start collecting RSVPs from Meetup.com
    please_respond = PleaseRespond( i_seconds )
    please_respond.stream()

    # Get the report and display it.
    data = please_respond.report()
    print( data )

