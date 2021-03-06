#!/usr/bin/python

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

import os
import sys

from controller import Controller
from hawModel.hawCalendar import SEMESTERGRUPPE, GRUPPENKUERZEL, DOZENT

if len(sys.argv) != 2:
    print "usage: allGroups2iCalendar HAW_CALENDAR_TEXT_FILE"
    sys.exit(1)

inFile = sys.argv[1]
outFile = None

def writeIcals(subfolder):
    for key in sorted(controller.getKeys()):
        veranstaltungen = controller.getVeranstaltungen(key)
        controller.selectVeranstaltungen(veranstaltungen)

        fileName = key.replace(' ', '_').replace('/','_').replace('[','(')
        fileName = fileName.replace(']',')').replace('ß','_et_')
        fileName = fileName.replace('A', 'AE').replace('ä', 'ae')
        fileName = fileName.replace('Ö', 'OE').replace('ö', 'oe')
        fileName = fileName.replace('Ü', 'UE').replace('ü', 'ue')
        fileName += ".ics"
        if fileName==".ics": fileName = "aaa_noName.ics"

        try: os.mkdir(subfolder)
        except OSError: pass

        controller.setOutfile(subfolder + fileName)
        sumEvents = controller.writeIcalendar()

        print key + ": iCalendar '" + fileName + "' created (" + str(sumEvents) + " Events)"

        controller.selectedVeranstaltungen = set()

controller = Controller(inFile, outFile, tupleKeyIndex=SEMESTERGRUPPE)
writeIcals(subfolder="Studentensicht/")

controller.tupleKeyIndex = DOZENT
writeIcals(subfolder="Dozentensicht/")

