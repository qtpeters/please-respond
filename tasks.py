
from shutil import rmtree
from invoke import task

@task
def build( c ):

    """
    Build the software and create an executable for distribution.
    """

    print("Building Please Respond...")
    c.run( "pyinstaller -y please_respond.py" )

@task
def clean( c ):

    """
    Remove unversioned artifacts.
    """

    rmtree( "dist" )
    rmtree( "build" )
    rmtree( "__pycache__" )

@task(build)
def run( c, seconds="" ):

    """
    Execute the code.
    """

    cmd = "./dist/please_respond/please_respond %s" % seconds
    c.run( cmd )
