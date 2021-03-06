# ~*~ encoding: utf-8 ~*~

###########################################################################
#  Copyright 2011 Theodor Nolte                                           #
#                                                                         #
#  This file is part of haw2iCalendar.                                    #
#                                                                         #
#  haw2iCalendar is free software: you can redistribute it and/or modify  #
#  it under the terms of the GNU General Public License as published by   #
#  the Free Software Foundation, either version 3 of the License, or      #
#  (at your option) any later version.                                    #
#                                                                         #
#  haw2iCalendar is distributed in the hope that it will be useful,       #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
#  GNU General Public License for more details.                           #
#                                                                         #
#  You should have received a copy of the GNU General Public License      #
#  along with haw2iCalendar.  If not, see <http://www.gnu.org/licenses/>. #
###########################################################################

from simpleparse import dispatchprocessor
from simpleparse.dispatchprocessor import dispatchList, getString, multiMap

class HawDispatchProcessor( dispatchprocessor.DispatchProcessor ):

    def __init__(self):
        self.next_count = "01"

    def semestergruppe(self,tup,buffer):
        """@result: 
        
        [
          (semestergruppe, gruppenKuerzel, fach, dozent, raum, jahr, woche, wochentag, anfang, ende, infoString, version),
          (eintrag-Tupel), ...
        ]
        """
        subTree = multiMap(tup[-1],buffer=buffer)

        infoString, version, semester, jahr, semestergruppe = dispatchList(self,subTree['header'], buffer)[0]

        result = []
        if "sections" in subTree:
            eintraege = dispatchList(self,subTree['sections'], buffer)[0]

            if semestergruppe == None:
                semestergruppe = self._derive_gruppenkuerzel(eintraege)

            for e in eintraege:
                gruppenKuerzel, fach, dozent, raum, woche, wochentag, anfang, ende = e
                result.append((semestergruppe, gruppenKuerzel, fach, dozent, raum, jahr, woche, wochentag, anfang, ende, infoString, version, semester))

        return result

    def header(self, tup, buffer):
        subTree = multiMap(tup[-1],buffer=buffer)
        infoString, version, semester, jahr = dispatchList(self,subTree['ersteZeile'], buffer)[0]
        gruppenKuerzel = ''
        if 'zweiteZeile' in subTree:
            gruppenKuerzel = dispatchList(self,subTree['zweiteZeile'], buffer)[0]
        else:
            gruppenKuerzel = None
        return (infoString, version, semester, jahr, gruppenKuerzel)
    def ersteZeile(self, tup, buffer): 
        subTree = multiMap(tup[-1],buffer=buffer)
        infoString, version, semester, jahr = dispatchList(self,subTree['infoString'], buffer)[0]
        return (infoString, version, semester, jahr)
    def infoString(self, tup, buffer):
        subTree = multiMap(tup[-1],buffer=buffer)
        version = dispatchList(self,subTree['version'], buffer)[0]
        semester, jahr = dispatchList(self,subTree['semester'], buffer)[0]
        infoString = str(getString(tup, buffer))
        return (infoString, version, semester, jahr)
    def version(self, tup, buffer):
        return str(getString(tup, buffer))
    def semester(self, tup, buffer):
        semester = str(getString(tup, buffer))
        subTree = multiMap(tup[-1],buffer=buffer)
        jahr = dispatchList(self,subTree['jahr'], buffer)[0]
        return semester, jahr
    def jahr(self, tup, buffer):
        return str(getString(tup, buffer))
    def zweiteZeile(self, tup, buffer):
        subTree = multiMap(tup[-1],buffer=buffer)
        gruppenKuerzel = dispatchList(self,subTree['gruppenKuerzel'], buffer)[0]
        return gruppenKuerzel
    def gruppenKuerzel(self, tup, buffer):
        return str(getString(tup, buffer))

    def sections(self, tup, buffer):
        subTree = multiMap(tup[-1],buffer=buffer)
        eintraegeList = dispatchList(self,subTree['section'], buffer)
        eintraege = reduce(lambda x,y: x+y, eintraegeList)
        return eintraege
    def section(self, tup, buffer):
        subTree = multiMap(tup[-1],buffer=buffer)
        wochen = dispatchList(self,subTree['wochen'], buffer)[0]
        eintraege = dispatchList(self,subTree['eintrag'], buffer)
        eintraegeMitWoche = []
        for woche in wochen:
            for e in eintraege:
                gruppenKuerzel, fach, dozent, raum, wochentag, anfang, ende = e
                eintraegeMitWoche.append((gruppenKuerzel, fach, dozent, raum, woche, wochentag, anfang, ende))
        return eintraegeMitWoche

    def wochen(self, tup, buffer):
        subTree = multiMap(tup[-1],buffer=buffer)
        wochenList = dispatchList(self,subTree['wocheOrWochenRange'], buffer)
        wochen = [item for sublist in wochenList for item in sublist]
        return wochen
    def wocheOrWochenRange(self,tup,buffer):
        subTree = multiMap(tup[-1],buffer=buffer)
        wochen = []
        if 'woche' in subTree:
            wochen = dispatchList(self,subTree['woche'], buffer)
        if 'wochenRange' in subTree:
            wochen = dispatchList(self,subTree['wochenRange'], buffer)[0]
        return wochen
    def wochenRange(self, tup, buffer):
        subTree = multiMap(tup[-1],buffer=buffer)
        anfangsWoche = dispatchList(self,subTree['anfangsWoche'], buffer)[0]
        endWoche = dispatchList(self,subTree['endWoche'], buffer)[0]
        return map(lambda x: str(x), range(int(anfangsWoche), int(endWoche)+1) )
    def anfangsWoche(self, tup, buffer):
        subTree = multiMap(tup[-1],buffer=buffer)
        anfangsWoche = dispatchList(self,subTree['woche'], buffer)[0]
        return anfangsWoche
    def endWoche(self, tup, buffer):
        subTree = multiMap(tup[-1],buffer=buffer)
        endWoche = dispatchList(self,subTree['woche'], buffer)[0]
        return endWoche
    def woche(self,tup,buffer):
        return str(getString(tup, buffer))
    def eintrag(self, tup, buffer):
        subTree = multiMap(tup[-1],buffer=buffer)
        if 'sixtupel' in subTree:
          result = dispatchList(self,subTree['sixtupel'], buffer)[0]
        else:
          result = dispatchList(self,subTree['septupel'], buffer)[0]
        return result
    def sixtupel(self, tup, buffer):
        subTree = multiMap(tup[-1],buffer=buffer)
        gruppenKuerzel, fach = dispatchList(self,subTree['fach'], buffer)[0]
        dozent = dispatchList(self,subTree['dozent'], buffer)[0]
        raum = dispatchList(self,subTree['raum'], buffer)[0]
        wochentag = dispatchList(self,subTree['wochentag'], buffer)[0]
        anfang = dispatchList(self,subTree['anfang'], buffer)[0]
        ende = dispatchList(self,subTree['ende'], buffer)[0]
        return (gruppenKuerzel, fach, dozent, raum, wochentag, anfang, ende)
    def septupel(self, tup, buffer):
        subTree = multiMap(tup[-1],buffer=buffer)
        gruppenKuerzel, fach = dispatchList(self,subTree['fach'], buffer)[0]
        dozent = dispatchList(self,subTree['dozent'], buffer)[0]
        raum = dispatchList(self,subTree['raum'], buffer)[0]
        raum += " (" + dispatchList(self,subTree['gebaeude'], buffer)[0] + ")"
        wochentag = dispatchList(self,subTree['wochentag'], buffer)[0]
        anfang = dispatchList(self,subTree['anfang'], buffer)[0]
        ende = dispatchList(self,subTree['ende'], buffer)[0]
        return (gruppenKuerzel, fach, dozent, raum, wochentag, anfang, ende)
    def fach(self, tup, buffer):
        subTree = multiMap(tup[-1],buffer=buffer)
        gruppenKuerzel = dispatchList(self, subTree['gruppe'], buffer)[0]
        fach = str(getString(tup, buffer))
        return gruppenKuerzel, fach
    def gruppe(self, tup, buffer):
        return getString(tup, buffer)
    def dozent(self, tup, buffer):
        return str(getString(tup, buffer))
    def gebaeude(self, tup, buffer):
        return str(getString(tup, buffer))
    def raum(self, tup, buffer):
        return str(getString(tup, buffer))
    def wochentag(self, tup, buffer):
        return str(getString(tup, buffer))
    def anfang(self, tup, buffer):
        subTree = multiMap(tup[-1],buffer=buffer)
        h, m = dispatchList(self,subTree['uhrzeit'], buffer)[0]
        return (h,m)
    def ende(self, tup, buffer):
        subTree = multiMap(tup[-1],buffer=buffer)
        h, m = dispatchList(self,subTree['uhrzeit'], buffer)[0]
        return (h,m)
    def uhrzeit(self, tup, buffer):
        subTree = multiMap(tup[-1],buffer=buffer)
        h = dispatchList(self,subTree['h'], buffer)[0]
        m = dispatchList(self,subTree['m'], buffer)[0]
        return (h,m)
    def h(self, tup, buffer):
        return str(getString(tup, buffer))
    def m(self, tup, buffer):
        return str(getString(tup, buffer))

    # Try to derive
    # 1. by semestergruppe
    # 2. "Wahlfächer""
    # 3. Phony
    def _derive_gruppenkuerzel(self, eintraege):

        result = None

        kuerzel_set = set()

        for e in eintraege:
            kuerzel = e[0]
            kuerzel_set.add(kuerzel)

        semestergruppen = [
               'MINF4', 'MINF3', 'MINF2', 'MINF1',
               'BAI6', 'BAI5', 'BAI4', 'BAI3', 'BAI2', 'BAI1',
               'BTI6', 'BTI5', 'BTI4', 'BTI3', 'BTI2', 'BTI1',
               'BWI6', 'BWI5', 'BWI4', 'BWI3', 'BWI2', 'BWI1', 
        ]

        # first hit succeeds
        for gruppe in semestergruppen:
            if gruppe in kuerzel_set:
                result = gruppe
                break

        if result == None:
            wahlfaecher = ['GW', 'INF']
            if not set(wahlfaecher).isdisjoint(kuerzel_set):
                result = "Wahlfächer"
                if self.next_count != "01":
                    result += "_{}".format(self.next_count)
                self.next_count = "{:02d}".format(int(self.next_count) + 1)
            else:
                # fallback to phony identifier
                result = self.next_phony_gruppenkuerzel()

        return result

    def _next_phony_gruppenkuerzel(self):
        prefix = "PHONY_"
        count = self.next_count
        self.next_count = "{:02d}".format(int(self.next_count) + 1)
        return prefix + count
