#!/usr/bin/python2

# -*- coding: utf-8 -*-

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
from optparse import OptionParser

from src.controller import Controller
from src.commandGui import CommandGui
from src.hawModel.hawCalendar import SEMESTERGRUPPE, GRUPPENKUERZEL, DOZENT

usage = """%prog [-o ICS-FILE] INFILE

Parse a haw calendar text file (Sem_I.txt or Sem_IuE.txt),
select dates, convert the dates to the iCalendar format (rfc5545)
and write them to stdout."""

# (grober) Ablauf:
#  + aus EBNF Parser erzeugen
#  + Quelldatei parsen
#  + mit dispatcher Ereignisse erzeugen
#  + nur gewuenschte Ereignisse herausfiltern
#  + .ics ausgeben: icalendar-head + ereignisse + END:VCALENDAR

def parseArgsAndOpts():
    optParse = OptionParser(usage)
    optParse.add_option("-p", "--prof", action="store_const", dest="keyIndex",
                          const=DOZENT, default=GRUPPENKUERZEL,
                            help="group by lecturers")
    optParse.add_option("-i", "--informatik", action="store_const", dest="keyIndex",
                          const=SEMESTERGRUPPE,
                            help="alternative grouping (by semestergruppe from header)")
    optParse.add_option("-o", dest="outFile", default=None, metavar="ICS-FILE",
                          help="write iCalendar-output to file instead stdout")

    (options, args) = optParse.parse_args()

    if len(args) != 1:
        print >> sys.stderr, "only exactly one argument allowed (use option '--help' for info)"
        sys.exit(0)

    inFile = args[0]

    return (inFile, options.outFile, options.keyIndex)


if __name__ == "__main__":

    # create a logfile only when warnings or errors occur
    logging.basicConfig(level=logging.WARNING)
    handler = logging.FileHandler(filename="haw2iCalendar.log", delay=True)
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logging.getLogger("").addHandler(handler) #add handler to the root logger


    inFile, outFile, keyIndex = parseArgsAndOpts()

    try:
        controller = Controller(inFile, outFile, tupleKeyIndex=keyIndex)
        CommandGui(controller)

    except Exception as e:
        logging.exception(e)
        raise e

