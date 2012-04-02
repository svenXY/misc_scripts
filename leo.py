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
'''
Spanisch-Deutsch Wörterbuch für die commandline
'''

import lxml.html
import sys

search = '+'.join(sys.argv[1:])
URL = 'http://dict.leo.org/esde?search=' + search

tree = lxml.html.parse(URL)
mytable = tree.xpath('.//table[@id="results"]')

for rows in mytable:
    for row in rows:
        if row[0].text_content() == '': continue
        if row[1].text_content().find('Keine') > -1: continue
        if row[0].text_content().find('rter im Trainer') > -1: continue
        if row.text_content().find('Umfeld der Suche') > -1: break
        if len(row) < 4:
            print row[1].text_content()
        else:
            print '%s <-> %s' % (row[1].text_content(), row[3].text_content())



