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
'''Überprüfe DB-Anzeigetafel (url) auf bestimtme Züge und notify

'''

import lxml.html
import re
import pynotify

# Interessante Züge (füge 'S 8' zum testen hinzu)
ZUEGE = [ 'EC 391', 'IC 391', 'IC 2373', 'RB 15365' ]
#ZUEGE = [ 'S 8', 'EC 391', 'IC 391', 'IC 2373' ]

# URL für Frankfurt a. M. Hbf
URL = ''.join( ['http://reiseauskunft.bahn.de/bin/bhftafel.exe/',
                'dn?ld=9644&rt=1&input=Frankfurt(Main)Hbf', 
                '%238000105&boardType=dep&time=actual&',
                'productsFilter=111111&start=yes' 
               ])

#### no more configuration ###

def normalize(string):
    '''Normalisiere die Zugnamen'''
    string = re.sub(r'\n', '', string)
    string = re.sub(r'\s+', ' ', string)
    return string

TREE = lxml.html.parse(URL)

PATTERN = re.compile('|'.join(ZUEGE))

# heavy use of xpath
ALLE_ZUEGE =  [(normalize(leaf.xpath('a/text()')[0]),
        leaf.getparent().xpath('td[@class="time"]/text()')[0],
        leaf.getparent().xpath('td[@class="ris"]/span/span/text()')[0]) 
          for leaf in TREE.xpath('.//td[@class="train"]') 
          if PATTERN.search( normalize(str(leaf.xpath('a/text()')))) ]


OUTPUT = '\n'.join([ "%s %s %s" % zug for zug in ALLE_ZUEGE ])

if len(OUTPUT):
    pynotify.init('Feierabend')
    NOTIFY = pynotify.Notification("Feierabend", 
                              OUTPUT, None )
    NOTIFY.show()
