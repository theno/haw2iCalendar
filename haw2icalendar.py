from hawParser import HawParser
from hawDispatchProcessor import HawDispatchProcessor

if __name__ == "__main__":
    file = open("/home/theno/hawicalendar/masterMin.txt", "r")
    text = file.read()
    file.close()
    
    success, resultList, strIndex = HawParser.parse(text, processor=HawDispatchProcessor())
    eventList = resultList[0]
    
    print "result:"
    for e in eventList:
        print e

    # filtern
    faecher = ["Vorkurs PRG", "BAI1-OE I"]
    newEventList = []
    for e in eventList:
        fach, dozent, raum, jahr, woche, tag, anfang, ende, infoString = e
	if fach in faecher:
	    newEventList.append(e)

    print "after filtering:"
    for e in newEventList:
        print e

    # icalendar erzeugen
    import icalendar
    ical = icalendar.Icalendar(eventList)
#    print ical.icalStr()
    # ausgeben

