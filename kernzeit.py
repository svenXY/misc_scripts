#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# sven
#
# gib anfangs- und endzeiten ein und schau, wie lange Du gearbeitet hast, bzw.
# wie lange Du noch musst, um optimal die Zeiten zu erreichen


from time import *
import re

daymins = 480

class NoValidTime(Exception):
    pass

class Zeiten(object):
    
    THRESHOLDS = [ (6,0), (8,30), (9,30), (10,45) ]
    muster = re.compile(r'(^\d{1,2}):(\d{1,2})$')

    def __init__(self, timestring):
        if not self.valid_time(timestring):
            raise NoValidTime, 'Keine gültige Zeit: %s' % timestring
        else:
            self.jahr, self.monat, self.tag, \
            bla,blu,blo, \
            self.wday,self.jtag,self.szeit = localtime()
            
            self.string = timestring
            self.as_stamp = self.to_seconds()
            
    def valid_time(self, timestring):
        mystrings  = Zeiten.muster.search(timestring)
        if not mystrings:
            return False
        hr, mn = mystrings.group(1,2)
        if int(hr) < 24 and int(mn) < 60:
            return True
        else:
            return False

    def to_seconds(self):
        stunde,minute = self.string.split(":")
        sekunden = mktime((self.jahr, self.monat, self.tag,int(stunde),int(minute),0,self.wday,self.jtag,self.szeit))
        return int(sekunden)

    def __cmp__(self, other):
        if self.as_stamp < other: return -1
        if self.as_stamp == other: return 0
        if self.as_stamp > other: return 1

    def __int__(self):
        return int(self.as_stamp)

    def duration(self,other):
        if self.as_stamp > other:
            return int(self.as_stamp) - int(other)
        if self.as_stamp < other:
            return int(other) - int(self.as_stamp)

    def calc_opts(max_s,pause,a_zeit,bisher_s, summe_pause):
        ''' Berechnet die optimale Endzeit für optimale Pausenzeitenausnutzung
            bei Berücksichtigung bereits genommener Pausen.

            Gibt einen String zurück
        '''
        e_zeit = max_s*60*60 - bisher_s + a_zeit + ( pause*60 - summe_pause )
        return " ".join([strftime("%H:%M", 
                        localtime(e_zeit)), 
                        " für genau ", 
                        str(max_s), 
                        " Stunden, ",
                        str(int(pause - summe_pause/60)),
                        " Minuten Pause verschenkt"
                        ])
    calc_opts = staticmethod(calc_opts)

def main():
    zeiten     = []
    while 1:
        input = raw_input("Zeit (hh:mm  oder q fuer Ende)> ")
        if input == 'q': break
        try:
            zeit = Zeiten(input)

            if len(zeiten) and zeit < zeiten[-1]:
                raise NoValidTime, "Zeit vor Vorheriger: %s <=> %s" \
                    % (zeiten[-1].string, zeit.string)

        except NoValidTime, e:
            print "Fehler: %s" % e
            continue
        
        zeiten.append(zeit)
    
    what         = 'anfangszeit'
    summe_sek     = 0
    summe_pause    = 0
    a_zeit         = 0
    e_zeit         = 0

    for zeit in zeiten:
        if what == 'anfangszeit':
            a_zeit = zeit.as_stamp
            if e_zeit:
                summe_pause += zeit.duration(e_zeit)
                e_zeit = 0
            what = 'endzeit'
        else:
            summe_sek += zeit.duration(a_zeit)
            e_zeit = zeit.as_stamp
            a_zeit = zeit.as_stamp
            what = 'anfangszeit'


    Zeiten.THRESHOLDS.reverse()
    pflichtpause = 0
    for t,p in Zeiten.THRESHOLDS:
        if summe_sek > t*60*60:
            pflichtpause = p*60
            break
    Zeiten.THRESHOLDS.reverse()
    genommene_pause = int(summe_pause/60)

    if  pflichtpause >= summe_pause:
        pause = pflichtpause
        pause_diff = pause - summe_pause
    else:
        pause = summe_pause
        pause_diff = 0

    summe_sek = summe_sek - pause_diff    
    pause = int(pause/60)
    
    hour,minute = divmod(summe_sek/60, 60)

    print "%d Stunde(n) und %d Minute(n) (plus %d (genommen: %d) min. Pause) registriert" \
            % ( hour, minute, pause, genommene_pause )

    print "\n".join([Zeiten.calc_opts(t,p,a_zeit,summe_sek, summe_pause) 
                        for t,p in Zeiten.THRESHOLDS]
                    )

if __name__ == "__main__":
    main()
