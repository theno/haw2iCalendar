
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

class HawCalendar:
    def __init__(self, eventTupelLists):
        """
        @param eventTupelLists:
        [
          [ 
            (gruppenKuerzel, fach, dozent, raum, jahr, woche, wochentag, anfang, ende, infoString),
            ...
          ],
          ...
        ]
        """

        # data = {gruppenKuerzel : [(fach, dozent, raum, jahr, woche, wochentag, anfang, ende, infoString),
        #                          ...
        #                          ],
	#         gruppenKuerzel : veranstaltungenList,
        #         ...
        #        }
        self.data = {}
        eventTupelList = [event for eventTupelList in eventTupelLists for event in eventTupelList] 
        for gruppenKuerzel, fach, dozent, raum, jahr, woche, wochentag, anfang, ende, infoString in eventTupelList:
            eventTupel = (fach, dozent, raum, jahr, woche, wochentag, anfang, ende, infoString)
            if not gruppenKuerzel in self.data:
                self.data[gruppenKuerzel] = [eventTupel]
            else:
                l = self.data[gruppenKuerzel]
                if not eventTupel in l:
                    l.append((fach, dozent, raum, jahr, woche, wochentag, anfang, ende, infoString))
                else:
	            logging.info("HawCalendar(__init__): redundant event rejected: " + str(eventTupel))

    def keepOnly(self, veranstaltungen):
        """@param veranstaltungen: String (Veranstaltungskuerzel)
           @result: void
        """
	for key in self.data:
	    l = self.data[key]
	    newL = []
	    for eventTupel in l:
	        veranstaltung, b,c,d,e,f,g,h,i = eventTupel
	        if veranstaltung in veranstaltungen:
		    newL.append(eventTupel)
            self.data[key] = newL

    def keepOnlyBySemestergruppen(self, semestergruppen):
        for key in filter(lambda x: x not in semestergruppen, self.data.keys()):
	    self.data.pop(key)

    def icalStr(self):
	eventTupelList = [eventTupel for l in self.data.values() for eventTupel in l]
        ical = Icalendar(eventTupelList)
	return ical.icalStr()

    def getSemestergruppen(self):
        return self.data.keys()

    def getVeranstaltungen(self):
        return set([veranstaltung for l in self.data.values() for veranstaltung, b,c,d,e,f,g,h,i in l])

    def getVeranstaltungenFromSemestergruppe(self, semestergruppe):
        veranstaltungen = self.data[semestergruppe]
	return set(map(lambda (veranstaltung, b,c,d,e,f,g,h,i): veranstaltung, veranstaltungen))

