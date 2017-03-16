# -*- encoding: utf-8 -*-
import sys

import const
import server

from db import db

### HACK
import socket
socket.getfqdn = lambda name=None: ""
### HACK

def main(argv = None):
    try:
        server.run()
        return 0
    except:
        raise 
        return -1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))