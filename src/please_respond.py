#!/usr/bin/env python3

import sys
from pleaserespond.main import main

# Run this program only as a script.
if __name__ == "__main__":
    seconds = None
    if len( sys.argv ) == 2:
        seconds = sys.argv[1]
    main( seconds )
