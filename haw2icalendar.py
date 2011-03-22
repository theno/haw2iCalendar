#!/usr/bin/python

# -*- coding: utf-8 -*-

from optparse import OptionParser

from commandGui import *
from controller import Controller

usage = """%prog [-o FILE] Sem_I.txt

Parse a haw calendar text file (Sem_I.txt),
select dates, convert the dates to icalendar format (rfc5545)
and write them to stdout."""

def parseOpts():
    optParse = OptionParser(usage)
    optParse.add_option("-o", dest="outFile", default=None, metavar="FILE",
                       help="write ics-output to file instead stdout")
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

