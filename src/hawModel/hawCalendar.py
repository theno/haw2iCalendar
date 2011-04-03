
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

from icalendar import Icalendar

# named indices for eventTupel ("tupelKeyIndices")
SEMESTERGRUPPE, GRUPPENKUERZEL, FACH, DOZENT, RAUM, JAHR, WOCHE, WOCHENTAG, ANFANG, ENDE, INFOSTRING = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10

class HawCalendar:
    def __init__(self, eventTupelLists):
        """
        event ~ veranstaltung

        @param eventTupelLists:
        [
          [ 
            (semestergruppe, gruppenKuerzel, fach, dozent, raum, jahr, woche, wochentag, anfang, ende, infoString),
            ...
          ],
          ...
        ]
        @param keyIndex: Index (int) of the eventTupelLists (sub-) element which will be the key in the data dict
        """

        # eventTupelList = [eventTupel,
        #                   (semestergruppe, gruppenkuerzel, fach, dozent, raum, jahr, woche, wochentag, anfang, ende, infoString),
        #                   (a,b,c,d,e,f,g,h,i,j,k),
        #                   ...
        #                  ],
        self.eventTupelList = [event for eventTupelList in eventTupelLists for event in eventTupelList] 

    def onlyWithVeranstaltungen(self, veranstaltungen):
        """@param veranstaltungen: List of type String (Veranstaltungskuerzel ~ fach)
           @result: HawCalendar
        """
        return HawCalendar([filter(lambda (a,b, veranstaltung, d,e,f,g,h,i,j,k): veranstaltung in veranstaltungen,
                                    self.eventTupelList)])

#    def onlyWithSemestergruppen(self, semestergruppen):
#        """@param semestergruppen: List of type String (Semestergruppenkuerzel ~ gruppenkuerzel)
#           @result: HawCalendar
#        """
#        return HawCalendar([filter(lambda (a, gruppenkuerzel, c,d,e,f,g,h,i,j,k): gruppenkuerzel in semestergruppen,
#                                    self.eventTupelList)])

    def icalStr(self):
        events = [(fach,dozent,raum,jahr,woche,tag,anfang,ende,infoString)
                   for (a,b, fach,dozent,raum,jahr,woche,tag,anfang,ende,infoString)
                     in self.eventTupelList]
        ical = Icalendar(events)
        return ical.icalStr()

#    def getSemestergruppen(self):
#        return set([gruppenKuerzel for (a, gruppenKuerzel, c,d,e,f,g,h,i,j,k) in self.eventTupelList])

#    def getVeranstaltungen(self):
#        return set([veranstaltung for (a,b, veranstaltung, d,e,f,g,h,i,j,k) in self.eventTupelList])

#    def getVeranstaltungenFromSemestergruppe(self, semestergruppe):
#        return set([veranstaltung for a,b, veranstaltung, d,e,f,g,h,i,j,k
#                    in filter(lambda (a, gruppe, c,d,e,f,g,h,i,j,k): gruppe==semestergruppe, self.eventTupelList)])

    def getKeys(self, tupelKeyIndex):
        return set([eventTupel[tupelKeyIndex] for eventTupel in self.eventTupelList])

    def getVeranstaltungenFromKey(self, key, tupelKeyIndex):
        return set([veranstaltung for a,b, veranstaltung, d,e,f,g,h,i,j,k
                    in filter(lambda eventTupel: eventTupel[tupelKeyIndex]==key, self.eventTupelList)])
