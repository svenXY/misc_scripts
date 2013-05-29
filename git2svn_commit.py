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

import pysvn
import sys
import getpass

log_msg = ''.join(sys.argv[1:])

client = pysvn.Client()
client.set_default_username(getpass.getuser())
client.set_default_password(getpass.getpass())
client.exception_style = 0

ignore = client.propset('svn:ignore', '.git', '.')
states = client.status('.')

new     = [ i.path for i in states if str(i.text_status) == 'unversioned' ]
missing = [ i.path for i in states if str(i.text_status) == 'missing' ]
mod     = [ i.path for i in states if str(i.text_status) == 'modified' ]

for i in new:
    client.add(i)

for o in missing:
    client.remove(o)

try:
    revision = client.checkin('.', log_msg)
except pysvn.ClientError, e:
     print e.args

if revision:
    print 'New SVN revision %d' % revision.number
    client.update('.')


