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

import sys

from controller import Controller

if len(sys.argv) != 2:
    print "usage: allGroups2iCalendar HAW_TEXT_FILE"
    sys.exit(1)

inFile = sys.argv[1]
outFile = None

controller = Controller(inFile, outFile)

for semestergruppe in controller.getSemestergruppen():
    controller.selectVeranstaltungen(set(controller.getVeranstaltungen(semestergruppe)))
    fileName = semestergruppe + ".ics"
    controller.setOutfile(fileName)
    sumEvents = controller.writeIcalendar()
    print semestergruppe + ": iCalendar '" + fileName + "' created (" + str(sumEvents) + " Events)"

