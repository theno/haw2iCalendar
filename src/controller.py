
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

import sys

from hawModel.hawCalendar import HawCalendar
from hawModel.hawDispatchProcessor import HawDispatchProcessor
from hawModel.hawParser import HawParser
from hawModel.veranstaltungen.veranstaltungenParser import tryGetFullName

class Controller:

    def __init__(self, inFileName, outFileName):

	self.__inFileName = inFileName
	self.__outFileName = outFileName

	text = self.__fetchInputText(inFileName)
	success, resultList, strIndex = HawParser.parse(text, processor=HawDispatchProcessor())
	self.__hawCal = HawCalendar(resultList)

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

    def writeIcalendar(self):
        """@return: sum of written iCalendar events"""

	self.__hawCal.keepOnly(self.selectedVeranstaltungen)
        icalStr = self.__hawCal.icalStr()
        if self.__outFileName != None:
	    f = open(self.__outFileName, "w")
	    f.write(icalStr)
	    f.close()
	else:
	    sys.stdout.write(icalStr)

        sumEvents = icalStr.count("BEGIN:VEVENT\r\n")

        #"reset" mutable HawCalendar object self.__hawCal to contain all
        #events again which was removed after the 'keepOnly()' call
	#FIXME: this is very dirty (needed because HawCalendar is mutable)
	text = self.__fetchInputText(self.__inFileName)
	success, resultList, strIndex = HawParser.parse(text, processor=HawDispatchProcessor())
	self.__hawCal = HawCalendar(resultList)

        return sumEvents

    def getSemestergruppen(self):
        return self.__hawCal.getSemestergruppen()

    def getVeranstaltungen(self, semestergruppe):
        return self.__hawCal.getVeranstaltungenFromSemestergruppe(semestergruppe)

    def selectVeranstaltungen(self, veranstaltungen):
        self.selectedVeranstaltungen |= veranstaltungen

    def unselectVeranstaltungen(self, veranstaltungen):
        self.selectedVeranstaltungen -= veranstaltungen

    def tryGetFullName(self, veranstaltung):
        return tryGetFullName(veranstaltung)

    def setOutfile(self, outFileName):
	self.__outFileName = outFileName

