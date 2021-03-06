
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

import logging
import re

from icalendar import Icalendar

# named indices for eventTupel (used as "tupelKeyIndex")
SEMESTERGRUPPE, GRUPPENKUERZEL, FACH, DOZENT, RAUM, JAHR, WOCHE, WOCHENTAG, ANFANG, ENDE, INFOSTRING = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10

class HawCalendar:
    def __init__(self, eventTupelLists):
        """
        event ~ veranstaltung (but a 'veranstaltung' has several 'events')

        @param eventTupelLists:
        [
          [ 
            (semestergruppe, gruppenKuerzel, fach, dozent, raum, jahr, woche, wochentag, anfang, ende, infoString, version, semester),
            ...
          ],
          ...
        ]

        alias for 'fach': 'veranstaltung'
        """

        # eventTupelList = [eventTupel,
        #                   (semestergruppe, gruppenkuerzel, fach, dozent, raum, jahr, woche, wochentag, anfang, ende, infoString, version, semester),
        #                   (a,b,c,d,e,f,g,h,i,j,k,l,m),
        #                   ...
        #                  ]
        self.eventTupelList = [event for eventTupelList in eventTupelLists for event in eventTupelList] 

    def onlyWithVeranstaltungen(self, veranstaltungen):
        """@param veranstaltungen: List of type String (Veranstaltungskuerzel ~ fach)
           @result: HawCalendar
        """
        return HawCalendar([filter(lambda (a,b, veranstaltung, d,e,f,g,h,i,j,k,l,m): veranstaltung in veranstaltungen, self.eventTupelList)])

    def icalStr(self):
        events = [(fach,dozent,raum,jahr,woche,tag,anfang,ende,infoString)
                   for (a,b, fach,dozent,raum,jahr,woche,tag,anfang,ende,infoString, l, m)
                     in self.eventTupelList]
        events = list(set(events)) # remove duplicates 
        ical = Icalendar(events)
        return ical.icalStr()

    def getKeys(self, tupelKeyIndex):
        return set([eventTupel[tupelKeyIndex] for eventTupel in self.eventTupelList])

    def getVeranstaltungenFromKey(self, key, tupelKeyIndex):
        return set([veranstaltung for a,b, veranstaltung, d,e,f,g,h,i,j,k,l,m in filter(lambda eventTupel: eventTupel[tupelKeyIndex]==key, self.eventTupelList)])


# Input example: WiSe 2014
#
# Return example: 2014-2_Wintersemester 2014/15
# Return example: 2014-1_Sommersemester 2014
#
def semester2lexicographically_ordered_verbose_string(semester):

    kind, year = semester.split(' ', 1)

    year = normalized_year(year)

    full_year = year

    if kind == 'SoSe':

        no = '1'

        full_name = 'Sommersemester'
        full_year = year

    elif kind == 'WiSe':

        no = '2'

        full_name = 'Wintersemester'
        full_year = year + '/' + str(int(year[2:]) + 1)

    else:
        # TODO warn
        return semester

    return '{year}-{no}_{full_name} {full_year}'.format(**locals())


def normalized_year(year):
    year = year.split('/')[0] # '12/13' -> '12', '2014' -> '2014'
    if len(year) == 2:
        year = '20' + year # '12' -> '2012'
    return year


def normalized_ort(ort):
    p = re.compile(r'^(\d\d)(\d\d)(?!\d)')
    return p.sub(r'Rm. \1.\2', ort)


# Arg kuerzel: 'Mo', 'Di', ... , 'So'
# Return: 0, 1, ... ,6
#
def wochentagabk2weekdayno(kuerzel):
    result = None
    if (kuerzel == 'Mo'):
        result = 0
    if (kuerzel == 'Di'):
        result = 1
    if (kuerzel == 'Mi'):
        result = 2
    if (kuerzel == 'Do'):
        result = 3
    if (kuerzel == 'Fr'):
        result = 4
    if (kuerzel == 'Sa'):
        result = 5
    if (kuerzel == 'So'):
        result = 6
    return result
