#!/usr/bin/python

# -*- coding: utf-8 -*-

from optparse import OptionParser

from commandGui import *
from controller import Controller

usage = """%prog [-o ICS-FILE] INFILE

Parse a haw calendar text file (Sem_I.txt or Sem_IuE.txt),
select dates, convert the dates to icalendar format (rfc5545)
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
                       help="write ics-output to file instead stdout")

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

