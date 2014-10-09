
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
import sys

from hawModel.hawCalendar import HawCalendar, GRUPPENKUERZEL, SEMESTERGRUPPE
from hawModel.hawDispatchProcessor import HawDispatchProcessor
from hawModel.hawParser import HawParser, prepared_Sem_I_txt
from hawModel.veranstaltungen.veranstaltungenParser import tryGetFullName

class Controller:

    def __init__(self, inFileName, outFileName, tupleKeyIndex=GRUPPENKUERZEL):

        self.__inFileName = inFileName
        self.__outFileName = outFileName

        self.tupleKeyIndex = tupleKeyIndex

        text = self.__fetchInputText(inFileName)
        text = prepared_Sem_I_txt(text)
        success, resultList, strIndex = HawParser.parse(text, processor=HawDispatchProcessor())
        self.__hawCal = HawCalendar(resultList)

        if (not success or not strIndex==len(text)):
            s = "Could not parse correctly haw-calendar text file: "
            s +="hawParser.py needs to be adjusted to a new text file format"
            logging.error(s)

        self.selectedVeranstaltungen = set()

    def __fetchInputText(self, inFileName):
        text_cp1252 = ""

        if inFileName != None:
            f = open(inFileName, "r")
            text_cp1252 = f.read()
            f.close()
        else:
            text_cp1252 = sys.stdin.read()

        text_unicode = text_cp1252.decode("cp1252")
        text_utf8 = text_unicode.encode("utf-8")
        return text_utf8

    def setOutFileName(self, name):
        self.__outFileName = name

    def writeIcalendar(self):
        """@return: sum of written iCalendar events"""

        cal = self.__hawCal.onlyWithVeranstaltungen(self.selectedVeranstaltungen)
        icalStr = cal.icalStr()
        sumEvents = icalStr.count("BEGIN:VEVENT\r\n")

        if self.__outFileName != None:
            f = open(self.__outFileName, "w")
            f.write(icalStr)
            f.close()
            logging.info("Written iCalendar file '" + self.__outFileName + "' with " + str(sumEvents) + " events")
        else:
            sys.stdout.write(icalStr)
            logging.info("Printed iCalendar with " + str(sumEvents) + " events to stdout")

        return sumEvents

    def getKeys(self):
        return self.__hawCal.getKeys(self.tupleKeyIndex)

    def getVeranstaltungen(self, key):
        return self.__hawCal.getVeranstaltungenFromKey(key, self.tupleKeyIndex)

    def selectVeranstaltungen(self, veranstaltungen):
        self.selectedVeranstaltungen |= veranstaltungen

    def unselectVeranstaltungen(self, veranstaltungen):
        self.selectedVeranstaltungen -= veranstaltungen

    def tryGetFullName(self, veranstaltung):
        return tryGetFullName(veranstaltung)

    def setOutfile(self, outFileName):
        self.__outFileName = outFileName

    def getInfoString(self):
        a,b,c,d,e,f,g,h,i,j,infoString = self.__hawCal.eventTupelList[0]
        return infoString

    def optimalGruppenKeyIndex(self):
        keyIndex = SEMESTERGRUPPE

        sumOfGroupsInGroup = len(sorted(self.getKeys())[0].split())
        if sumOfGroupsInGroup > 10:
            keyIndex = GRUPPENKUERZEL

        return keyIndex

    def data_tuples(self):
        #TODO version statt infostring als version zurueckliefern
        return [(semestergruppe, gruppenkuerzel, fach, dozent, ort, jahr, woche, wochentag, anfang, ende, infoString, infoString, tryGetFullName(fach))
                for (semestergruppe, gruppenkuerzel, fach, dozent, ort, jahr, woche, wochentag, anfang, ende, infoString)
                in self.__hawCal.eventTupelList]
