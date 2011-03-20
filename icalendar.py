import time
import logging

from veranstaltungen import fullNames

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
    def __init__(self, events):
        self.header = HEADER
	self.events = []
	for e in events:
	    self.events.append(IcalEvent(e))

    def icalStr(self):
        result = HEADER + "\n"
	for event in self.events:
	    result += event.icalStr() + "\n"
	result += "END:VCALENDAR"
	return str(result)
    
class IcalEvent:
    def __init__(self, (fach,dozent,raum,jahr,woche,tag,anfang,ende,infoString)):
        self.fach = fach
	self.dozent = dozent
	self.raum = raum
	self.anfangsDatum = createDateTimeString(dateTime(jahr,woche,tag,anfang))
	self.endDatum = createDateTimeString(dateTime(jahr,woche,tag,ende))
	self.dateTimeStamp = createDateTimeString(time.gmtime())
	self.infoString = infoString
    
    def icalStr(self):
	summary = "SUMMARY:"
	description = "DESCRIPTION:"

	# SUMMARY
        r  = "BEGIN:VEVENT" + "\r\n"
	if self.fach in fullNames:
	    summary += fullNames[self.fach]
	    description += self.fach + "\\n"
	else:
	    logging.info("No full name found for '" + self.fach + "' in 'veranstaltungen.py'")
	    summary += self.fach
	r += summary + "\r\n"

        # DESCRIPTION
	if self.dozent != "":
	    description += "Prof.: " + self.dozent + "\\n\\n" + "\r\n " 
	else:
	    description += "\\n"
	r += description + self.infoString + "\r\n"

        # DATETIME
        r += "DTSTART;TZID=Europe/Berlin:" + self.anfangsDatum + "\r\n"
	r += "DTEND;TZID=Europe/Berlin:" + self.endDatum + "\r\n"
	r += "DTSTAMP:" + self.dateTimeStamp + "\r\n"

	# LOCATION
	raum = ""
	if self.raum != "":
	    raum = "Rm. " + self.raum
	r += "LOCATION:" + raum + "\r\n"

	r += "UID:" + createUid(self.dateTimeStamp) + "\r\n"
	r += "END:VEVENT"
	return r

def dateTime(jahrKuerzel, wochennummer, wochentag, uhrzeit):
    """@return: time.struct_time"""

    jahr = "20" + jahrKuerzel

    wochentage = {"mo": "1", "di": "2", "mi": "3", "do": "4", "fr": "5", "sa": "6", "so": "0"}
    wochentag = wochentage[wochentag.lower()]

    stunde, minute = uhrzeit

    struct_time = time.strptime(jahr + " " + wochennummer + " " + wochentag + " " + stunde + " " + minute,
                                "%Y %W %w %H %M")
    return struct_time

def createDateTimeString(struct_time):
    """result: date string with (non-utc) time"""
    t = struct_time

    yyyy = "%.4d" % t.tm_year
    mm = "%.2d" % int(t.tm_mon)
    dd = "%.2d" % int(t.tm_mday)

    HH = "%.2d" % int(t.tm_hour)
    MM = "%.2d" % int(t.tm_min)
    SS = "%.2d" % int(t.tm_sec)

    return yyyy + mm + dd + "T" + HH + MM + SS

def monthAndDay(jahr, woche, tag):
    return (woche, tag)

def createUid(dateTime):
    import random
    rand = reduce(lambda x,y : str(x) + str(random.randint(0,9)), [random.randint(0,9)] + range(9))
    return dateTime + " Atomkraft? Nein Danke! " + rand + "@theno.eu"

def test():
    dateTimeString = createDateTimeString(time.localtime())
    print dateTimeString
    print createUid(dateTimeString)


if __name__ == "__main__":
    test()

# validator: http://severinghaus.org/projects/icv/
