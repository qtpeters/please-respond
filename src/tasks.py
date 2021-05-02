
from shutil import rmtree
from invoke import Task

@Task
def build( c ):
    print("Building Please Respond...")
    c.run( "pyinstaller -y please_respond.py" )

@Task
def clean( c ):
    rmtree( "dist" )
    rmtree( "build" )
    rmtree( "__pycache__" )
