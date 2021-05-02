
from shutil import rmtree
from invoke import task
from os.path import exists

@task
def clean( c ):

    """
    Remove unversioned artifacts.
    """

    # rmtree doesn't like it when there
    # is no file/folder, so we have to test
    # before we delete.
    def rm_f( dir ):
        if exists( dir ):
            rmtree( dir )

    rm_f( "dist" )
    rm_f( "build" )
    rm_f( "__pycache__" )


@task( clean )
def build( c ):

    """
    Build the software and create an executable for distribution.
    """

    print("Building Please Respond...")
    c.run( "pyinstaller -y please_respond.py" )


@task( build )
def run( c, seconds="" ):

    """
    Execute the code.
    """

    cmd = "./dist/please_respond/please_respond %s" % seconds
    c.run( cmd )

@task
def rerun( c, seconds="" ):

    """
    Execute the code.
    """
    
    try:
        exe = "./dist/please_respond/please_respond"
        result = c.run( "test -e %s" % exe )
        cmd = "%s %s" % ( exe, seconds )
        c.run( cmd )
    except:
        print("No previous build exists, use: inv run [--seconds <seconds>]")


