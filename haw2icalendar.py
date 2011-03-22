#!/usr/bin/python

# -*- coding: utf-8 -*-
from optparse import OptionParser

from commandGui import *
from controller import Controller
#from hawCalendar import HawCalendar
#from hawDispatchProcessor import HawDispatchProcessor
#from hawParser import HawParser

usage = """%prog [-o FILE] Sem_I.txt

Parse a haw calendar text file (Sem_I.txt),
convert the dates to icalendar (rfcXXXX)
and write them to stdout."""# > hawVeranstaltungen.ics"""
def parseOpts():
    optParse = OptionParser(usage)
#    optParse.add_option("-i", dest="inFile", default=None, metavar="FILE",
#                       help="read (Sem_I.txt format) data from inputfile instead from stdin")
    optParse.add_option("-o", dest="outFile", default=None, metavar="FILE",
                       help="write ics-output to file instead to stdout")
#    optParse.add_option("-k", "--gui", action="store_true", dest="gui", default=False,
#                       help='"klickibunti"')
    (options, args) = optParse.parse_args()
    if len(args) != 1:
        print "only one argument allowed (use option '--help' for info)"
	sys.exit()
    inFile = args[0]
    return (inFile, options.outFile)

if __name__ == "__main__":
    inFile, outFile = parseOpts()

    controller = Controller(inFile, outFile)
    CommandGui(controller)

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
#    semestergruppen = ["M-INF2"]
#    hawCal.keepOnlyBySemestergruppen(semestergruppen)

#    hawCal.keepOnly(["MINF2-TH1", "MINF2-AW2", "MINF2-TT2", "MINF2-PJ1"])
#    hawCal.keepOnly(["MINF2-TH1", "MINF2-AW2", "MINF2-TT2"])

#    hawCal.keepOnly(["MINF2-TH\xc3\x9c1/01"])
#    hawCal.keepOnly(["MINF2-TH\xc3\x9c1/02"])
#
#    hawCal.keepOnly(["MINF2-TTP2/01"])
#    hawCal.keepOnly(["MINF2-TTP2/02"])

#    print str(hawCal.getSemestergruppen())
#    print str(hawCal.getVeranstaltungen())
#    print str(len(hawCal.getVeranstaltungen()))

#    print(hawCal.icalStr())

