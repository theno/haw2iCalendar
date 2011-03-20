# -*- coding: utf-8 -*-

from hawCalendar import HawCalendar
from hawDispatchProcessor import HawDispatchProcessor
from hawParser import HawParser

if __name__ == "__main__":
    file = open("/home/theno/hawicalendar/Sem_I.txt", "r")
    text_cp1252 = file.read()
    file.close()
    text_unicode = text_cp1252.decode("cp1252")
    text_utf8 = text_unicode.encode("utf-8")
    
    success, resultList, strIndex = HawParser.parse(text_utf8, processor=HawDispatchProcessor())

    hawCal = HawCalendar(resultList)

    semestergruppen = ["M-INF2"]
    hawCal.keepOnlyBySemestergruppen(semestergruppen)

#    hawCal.keepOnly(["MINF2-TH1", "MINF2-AW2", "MINF2-TT2", "MINF2-PJ1"])
#    hawCal.keepOnly(["MINF2-TH1", "MINF2-AW2", "MINF2-TT2"])

#    hawCal.keepOnly(["MINF2-TH\xc3\x9c1/01"])
    hawCal.keepOnly(["MINF2-TH\xc3\x9c1/02"])
#
#    hawCal.keepOnly(["MINF2-TTP2/01"])
#    hawCal.keepOnly(["MINF2-TTP2/02"])

#    print str(hawCal.getSemestergruppen())
#    print str(hawCal.getVeranstaltungen())
#    print str(len(hawCal.getVeranstaltungen()))

    print(hawCal.icalStr())

