import sys

from hawCalendar import HawCalendar
from hawDispatchProcessor import HawDispatchProcessor
from hawParser import HawParser
from veranstaltungenParser import tryGetFullName

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
	#FIXME: very dirty (needed because HawCalendar is mutable)
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

