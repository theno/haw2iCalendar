
HEADER = """BEGIN:VCALENDAR
BEGIN:VTIMEZONE
TZID:Europe/Berlin
X-LIC-LOCATION:Europe/Berlin
BEGIN:DAYLIGHT
TZOFFSETFROM:+0100
TZOFFSETTO:+0200
TZNAME:CEST
DTSTART:19700329T020000
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU
END:DAYLIGHT
BEGIN:STANDARD
TZOFFSETFROM:+0200
TZOFFSETTO:+0100
TZNAME:CET
DTSTART:19701025T030000
RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU
END:STANDARD
END:VTIMEZONE"""

class Icalendar:
    def __init__(events):
        self.header = HEADER
	self.events = []
	for e in events:
	    self.events.append(IcalEvent(e))

    def __str__():
        result = HEADER + "\n"
	for event in events:
	    result += str(event) + "\n"
	result += "END:VCALENDAR"
	return result
    
class IcalEvent:
    def __init__(fach,dozent,raum,jahr,woche,tag,anfang,ende,infoString):
        self.fach = fach
	self.dozent = dozent
	self.raum = raum
	self.anfangsDatum = dateTimeString(jahr,woche,tag,anfang)
	self.endDatum = dateTimeString(jahr,woche,tag,ende)
	self.dateTimeStamp = dateTimeString(jetzt)
	self.infoString = infoString
    
    def __str__():
        r  = "BEGIN:VEVENT" + "\n"
	r += "DESCRIPTION:" + "Prof.: " + self.dozent + "\n" + self.infoString + "\n"
        r += "DTSTART;TZID=Europe/Berlin:" + self.anfangsDatum + "\n"
	r += "DTEND;TZID:Europe/Berlin:" + self.endDatum + "\n"
	r += "DTSTAMP;TZID=Europe/Berlin:" + self.dateTimeStamp + "\n"
	r += "LOCATION:" + "Rm. " + self.raum + "\n"
	r += "SUMMARY:" + self.fach + "\n"
	r += "UID:" + createUid(self.dateTimeStamp) + "\n"
	r += "END:VEVENT"

def dateTimeString(jahr, woche, tag, uhrzeit):
    yyyy = "20" + jahr
    mm, dd = monthAndDay(yyyy, woche, tag)

    stunde, minute = uhrzeit
    HH = "%.2d" % int(stunde)
    MM = "%.2d" % int(minute)

    return yyyy + mm + dd + "T" + HH + MM + "00" + "Z"

def monthAndDay(jahr, woche, tag):
    return ("mm", "dd")

def createUid(dateTime):
    import random
    rand = reduce(lambda x,y : str(x) + str(random.randint(0,9)), [random.randint(0,9)] + range(9))
    return dateTime + " Atomkraft? Nein Danke! " + rand + "@informatik.haw-hamburg.de"

def test():
    print dateTimeString("80", "5", "Freitag", ("12", "30"))

if __name__ == "__main__":
    test()
