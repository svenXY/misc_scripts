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

import urllib
import urllib2
import lxml.html
import re
import pynotify
import argparse


# Interessante Züge (füge 'S8' zum testen hinzu)
ZUEGE = [ 'EC391', 'IC391', 'IC2373' ]

parser = argparse.ArgumentParser(
            description='Fragt die DB Haltestelleninformationen nach aktuellen Zügen ab.')

parser.add_argument(
   '--zug', '-Z', metavar='ZUG', nargs='+', type=str,
    help='Zugbezeichnung(en) in normalisierter Form (ohne Leerzeichen)')

parser.add_argument(
   '--bahnhof', '-B', metavar='BAHNHOF', type=str,
    default='Frankfurt(Main)Hbf', help='Bahnhofsbezeichnung für URL in normalisierter Form')

parser.add_argument(
   '--notify', '-n', action='store_true',
   help='Ergebnisse n der Notification-Area ausgeben')

args = parser.parse_args()

if args.zug:
  ZUEGE = args.zug

# URL für Frankfurt a. M. Hbf
postParams = urllib.urlencode({
        'input'             : args.bahnhof,
        'boardType'         : 'dep',
        'time'              : 'actual',
        'productsDefault'   : '1111111111',
        'productsLocal'     : '0000010111',
        'productsFilter'    : '1111111111',
        'distance'          : '1',
        'rt'                : '1',
        'start'             : "yes"
})

conn = urllib2.urlopen(
        "http://reiseauskunft.bahn.de/bin/bhftafel.exe/dn",
        postParams
)

data = ''.join(conn.readlines())
TREE = lxml.html.fromstring(data)

#### no more configuration ###
def normalize(string, complete=False):
    '''Normalisiere die Zugnamen'''
    string = re.sub(r'\n', '', string)
    string = re.sub(r'\s+', ' ', string)
    if complete:
        string = re.sub(r'\s', '', string)
    return string


PATTERN = re.compile('|'.join(ZUEGE))
ALLE_ZUEGE = []

try:
# heavy use of xpath
  ALLE_ZUEGE =  [
                  (
        normalize(leaf.xpath('a/text()')[0]),
        leaf.getparent().xpath('td[@class="time"]/text()')[0],
        normalize(''.join(leaf.getparent().xpath('td[@class="ris"]')[0].text_content()))
                  )
          for leaf in TREE.xpath('//td[@class="train"]') 
          if PATTERN.search( normalize(str(leaf.xpath('a/text()')), True)) ]
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
