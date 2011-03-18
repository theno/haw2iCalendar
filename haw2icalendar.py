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

#    semestergruppen = ["M-INF2", "B-AI1"]
    semestergruppen = ["M-INF2"]
#    semestergruppen = ["B-AI1"]
    hawCal.keepOnlyBySemestergruppen(semestergruppen)
#    hawCal.keepOnly(["MINF2-TH1", "MINF2-TH1UE"])

#    print str(hawCal.getSemestergruppen())
#    print str(hawCal.getVeranstaltungen())
#    print str(len(hawCal.getVeranstaltungen()))

    print(hawCal.icalStr())

