#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Name			:	
# Description	:	
# Author		: Sven Hergenhahn
#
# $Id$
# 
###################################################

import sys
import os
from subprocess import Popen, PIPE
from time import time
import logging

logging.basicConfig(filename='/home/svenh/tmp/oi.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s [%(process)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

FLAGFILE='/tmp/oi_running'
OI_CMD='/usr/local/bin/offlineimap -o -u quiet'
MAX_RUNTIME = 5
NOW = time()

logging.info('*** Starting ***')

if os.path.exists(FLAGFILE):
    logging.debug('Flagfile exists')
    with open(FLAGFILE) as f:
        mtime = os.fstat(f.fileno())[-2]
        if (NOW - mtime)/60.0 > MAX_RUNTIME:
            logging.debug('Flagfile is old enough - try to end process')
            pid=f.read()
            try:
                os.kill(int(pid), 9)
                logging.info('Killed OK - removing file')
                os.remove(FLAGFILE)
            except OSError, e:
                if e.errno == 2:
                    pass
                elif e.errno == 3:
                    logging.debug('No such process - removing file')
                    os.remove(FLAGFILE)
                else:
                    logging.error("Could not remove flagfile: %s" % e)
                    sys.exit(1)
        else:
            logging.info('Flagfile is not ancient. Exiting quietly')
            sys.exit(0)
else:
    logging.debug("No Flagfile")

cmd = list( OI_CMD.split(' '))
p = Popen(
    cmd,
    stdout=PIPE, 
    stderr=PIPE
)

with open(FLAGFILE, 'w') as f:
    logging.debug("writing flagfile")
    f.write(str(p.pid))

logging.info("Starting offlineimap process")
out, err = p.communicate()

logging.debug("Removing flagfile")

try:
    os.remove(FLAGFILE)
except OSError, e:
    if e.errno == 2:
        pass
    else:
        logging.error("Could not remove flagfile: %s" % e)
        sys.exit(1)


logging.debug("*** Proper end ***")

