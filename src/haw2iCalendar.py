#!/usr/bin/python

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

from optparse import OptionParser

from commandGui import *
from controller import Controller

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

def parseOpts():
    optParse = OptionParser(usage)
    optParse.add_option("-o", dest="outFile", default=None, metavar="ICS-FILE",
                       help="write iCalendar-output to file instead stdout")

    (options, args) = optParse.parse_args()

    if len(args) != 1:
        print >> sys.stderr, "only exactly one argument allowed (use option '--help' for info)"
	sys.exit(0)
    inFile = args[0]

    return (inFile, options.outFile)

if __name__ == "__main__":
    inFile, outFile = parseOpts()

    controller = Controller(inFile, outFile)
    CommandGui(controller)

#    from hawCalendar import HawCalendar
#    from hawDispatchProcessor import HawDispatchProcessor
#    from hawParser import HawParser
#
#    file = open("/home/theno/hawicalendar/Sem_I.txt", "r")
#    text_cp1252 = file.read()
#    file.close()
#    text_unicode = text_cp1252.decode("cp1252")
#    text_utf8 = text_unicode.encode("utf-8")
#    
#    success, resultList, strIndex = HawParser.parse(text_utf8, processor=HawDispatchProcessor())
#
#    hawCal = HawCalendar(resultList)
#
#    semestergruppen = ["B-AI4"]
#    hawCal.keepOnlyBySemestergruppen(semestergruppen)
#
#    hawCal.keepOnly(["MINF2-TH1", "MINF2-AW2", "MINF2-TT2", "MINF2-PJ1"])
#    hawCal.keepOnly(["MINF2-TH1", "MINF2-AW2", "MINF2-TT2"])

#    hawCal.keepOnly(["MINF2-TH\xc3\x9c1/01"])
#    hawCal.keepOnly(["MINF2-TH\xc3\x9c1/02"])
#
#    hawCal.keepOnly(["B-AI1"])
#    hawCal.keepOnly(["MINF2-TTP2/02"])

#    print str(hawCal.getSemestergruppen())
#    import pprint
#    print(sorted(hawCal.getVeranstaltungen()))
#    print str(len(hawCal.getVeranstaltungen()))

#    print(hawCal.icalStr())

