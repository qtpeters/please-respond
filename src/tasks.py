
from shutil import rmtree
from invoke import task

@task
def build( c ):
    print("Building Please Respond...")
    c.run( "pyinstaller -y please_respond.py" )

@task
def clean( c ):
    rmtree( "dist" )
    rmtree( "build" )
    rmtree( "__pycache__" )

@task(build)
def run( c, seconds="" ):
    cmd = "./dist/please_respond/please_respond %s" % seconds
    c.run( cmd )
