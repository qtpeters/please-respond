# Please Respond Solution

## Author
Quinn Peters, 02-May-2021

## Dependences

1. Python==3.8.6
1. altgraph==0.17
1. certifi==2020.12.5
1. chardet==4.0.0
1. geographiclib==1.50
1. geopy==2.1.0
1. idna==2.10
1. invoke==1.5.0
1. numpy==1.20.2
1. pyinstaller==4.3
1. pyinstaller-hooks-contrib==2021.1
1. python-dateutil==2.8.1
1. pytz==2021.1
1. requests==2.25.1
1. six==1.15.0
1. timezonefinder==5.2.0
1. urllib3==1.26.4

The user is required to install Python 3.8.6.  I recommend [pyenv](https://github.com/pyenv/pyenv).
A requirements.txt file is checked in and can be used to install all requirements at once save Python itelf. If
Python is correctly installed, you can use *pip install -r requirements.txt* to update your environment with the correct
modules necessary to run Please Respond.

## Running the code

The code can be run three ways, where ${root} is the top level directory of this repository: 

1. With the Invoke task runner.
1. With the main script ( ${root}/please_respond.py ) in the top level directory
1. (Experimental) The deployable executable: '${root}/dist/please_respond/please_respond.
    1. I'm checking out Pyinstaller and that is a mostly untested artifact that, with a bit of tweaking could easily be used to deploy with a CI/CD pippeline.

### With Python Invoke

The Invoke task runner is installed as one of the required packages.  You can run Please Respond by executing: *inv run [--seconds <seconds>]*. As required, the default is 60 seconds.  If the --seconds flag is omitted, you will be prompted for the number of seconds.  The code the Invoke executes is contained in ${root}/tasks.py.

### With ${root}/please_respond.py

This script, please_respond.py, is the entry point for the pyinstaller executable and it executes the code as it is in the repository. 

### With '${root}/dist/please_respond/please_respond.'

This executable is a distilled and deployable version of Please Respond.  I haven't tested this, but you should have all the dependencies necessary built into the executable so it can be executed anywhere without external dependences on any compatable architecture. This makes it simple to be dockerized and deployed to a Kubernetes cluster should horizontal scaling be required.