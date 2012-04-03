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
import argparse


# Interessante Züge (füge 'S 8' zum testen hinzu)
#ZUEGE = [ 'EC 391', 'IC 391', 'IC 2373', 'RB 15365' ]
ZUEGE = [ 'S8', 'EC391', 'IC391', 'IC2373' ]

parser = argparse.ArgumentParser(
            description='Fragt die DB Haltestelleninformationen nach aktuellen Zügen ab.')

parser.add_argument(
   '--zug', '-Z', metavar='ZUG', nargs='+', type=str,
    help='Zugbezeichnung(en) in normalisierter Form (ohne Leerzeichen)')

#parser.add_argument(
#   '--bahnhof', '-B', metavar='BAHNHOF', type=str,
#    default='Frankfurt(Main)Hbf', help='Bahnhofsbezeichnung für URL in normalisierter Form')

parser.add_argument(
   '--notify', '-n', action='store_true',
   help='Ergebnisse n der Notification-Area ausgeben')

args = parser.parse_args()

if args.zug:
  ZUEGE = args.zug

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
    string = re.sub(r'\s', '', string)
    return string

TREE = lxml.html.parse(URL)

PATTERN = re.compile('|'.join(ZUEGE))

try:
# heavy use of xpath
  ALLE_ZUEGE =  [(normalize(leaf.xpath('a/text()')[0]),
        leaf.getparent().xpath('td[@class="time"]/text()')[0],
        leaf.getparent().xpath('td[@class="ris"]/span/span/text()')[0]) 
          for leaf in TREE.xpath('.//td[@class="train"]') 
          if PATTERN.search( normalize(str(leaf.xpath('a/text()')))) ]
except IndexError:
  pass

OUTPUT = '\n'.join([ "%s %s %s" % zug for zug in ALLE_ZUEGE ])

if len(OUTPUT):
  if args.notify:
    pynotify.init('Haltestelleninformation')
    NOTIFY = pynotify.Notification("Haltestelleninformation", 
                              OUTPUT, None )
    NOTIFY.show()
  else:
    print OUTPUT
