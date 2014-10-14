
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

from hawModel.hawCalendar import HawCalendar, GRUPPENKUERZEL, SEMESTERGRUPPE, semester2lexicographically_ordered_verbose_string, wochentagabk2weekdayno
from hawModel.hawDispatchProcessor import HawDispatchProcessor
from hawModel.hawParser import HawParser, prepared_Sem_I_txt
from hawModel.icalendar import IcalEvent, HEADER, ENDING
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

    def data_dict(self):

        # data_dict structure with example values
        #
        # data_dict = {
        #
        #     DataImport: {
        #         # department: 'EuI'
        #         infostring: 'WiSe 2014 Vers. 1.00  vom 3.10.2014',
        #         version_text_datei: '1.00',
        #         # comment: 'imported automatically by script',
        #         semester: 'WiSe 2014',
        #         ical_header: 'BEGIN:VCALENDAR...'
        #         ical_ending: '...END:VCALENDAR''
        #     },
        #
        #     Veranstaltungen: [
        #         {
        #             semestergruppen: ['B-EE2','B-EE3',...] (for EuI)  or [] (for Inf)
        #             gruppenkuerzel: 'BTI2',
        #             veranstaltungskuerzel: 'BTI2-GS',
        #             veranstaltungsname: 'Grundlagen Systemprogrammierung',
        #
        #             Events: [
        #                 {
        #                     #veranstaltung: Fremdschluessel,
        #                     #data_import: Fremdschluessel,
        #
        #                     dozent: 'Friedrich Esser',
        #                     ort: 'Rm. 12.83',
        #                     wochen: '41, 42, ...',
        #                     wochentag: 'Di'
        #                     anfang: ('10','00'),
        #                     ende: ('13',15'),
        #                     icalevent: 'BEGIN:VEVENT...',
        #                 },
        #                 ...
        #             ],
        #         },
        #         ...
        #     ],
        #
        # }

        # create data_import

        first_event = self.__hawCal.eventTupelList[0]
        (semestergruppe, gruppenkuerzel, fach, dozent, ort, jahr, woche, wochentag, anfang, ende, infoString, version, semester) = first_event

        data_import = {
            'infostring': infoString,
            'version_text_datei': version,
            'semester': semester,
            'ical_header': HEADER,
            'ical_ending': ENDING,
        }

        # create veranstaltungen

        semester = semester2lexicographically_ordered_verbose_string(semester)

        faecher = set([(gruppenkuerzel, fach) for a,gruppenkuerzel,fach,d,e,f,g,h,i,j,k,l,m in self.__hawCal.eventTupelList])

        veranstaltungen_dicts = {}
        for (gruppenkuerzel, fach) in faecher:
            veranstaltungen_dicts[fach] = {
                    'semestergruppen': [],
                    'gruppenkuerzel': gruppenkuerzel,
                    'veranstaltungskuerzel': fach,
                    'veranstaltungsname': tryGetFullName(fach),
                    'Events': []
            }

        for event in self.__hawCal.eventTupelList:
            (semestergruppe, gruppenkuerzel, fach, dozent, ort, jahr, woche, wochentag, anfang, ende, infoString, version, semester) = event

            veranstaltung = veranstaltungen_dicts[fach]

            if semestergruppe != '' and semestergruppe not in veranstaltung['semestergruppen']:
                veranstaltung['semestergruppen'].append(semestergruppe)

            veranstaltung['Events'].append(
                    {
                        'dozent': dozent,
                        'ort': ort,
                        'jahr': jahr,
                        'wochen': woche,
                        'wochentag': wochentagabk2weekdayno(wochentag),
                        'anfang': anfang[0] + ':' + anfang[1],
                        'ende': ende[0] + ':' + ende[1],
                        'icalevent': IcalEvent((fach,dozent,ort,jahr,woche,wochentag,anfang,ende,infoString)).icalStr(),
                    }
            )

        veranstaltungen = veranstaltungen_dicts.values()

        return {'DataImport': data_import, 'Veranstaltungen': veranstaltungen}
