
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

import time
import logging

from veranstaltungen.veranstaltungenParser import tryGetFullName

# iCalendar validator:  http://icalvalid.cloudapp.net/

CRLF = "\r\n"

HEADER =  "BEGIN:VCALENDAR" + CRLF
HEADER += "VERSION:2.0" + CRLF
HEADER += "PRODID:-//haw2icalendar//de" + CRLF 
HEADER += "BEGIN:VTIMEZONE" + CRLF
HEADER += "TZID:Europe/Berlin" + CRLF
HEADER += "X-LIC-LOCATION:Europe/Berlin" + CRLF
HEADER += "BEGIN:DAYLIGHT" + CRLF
HEADER += "TZOFFSETFROM:+0100" + CRLF
HEADER += "TZOFFSETTO:+0200" + CRLF
HEADER += "TZNAME:CEST" + CRLF
HEADER += "DTSTART:19700329T020000" + CRLF
HEADER += "RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU" + CRLF
HEADER += "END:DAYLIGHT" + CRLF
HEADER += "BEGIN:STANDARD" + CRLF
HEADER += "TZOFFSETFROM:+0200" + CRLF
HEADER += "TZOFFSETTO:+0100" + CRLF
HEADER += "TZNAME:CET" + CRLF
HEADER += "DTSTART:19701025T030000" + CRLF
HEADER += "RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU" + CRLF
HEADER += "END:STANDARD" + CRLF
HEADER += "END:VTIMEZONE"+ CRLF

class Icalendar:
    def __init__(self, events):
        """@param events:
               [ (fach,dozent,raum,jahr,woche,tag,anfang,ende,infoString), ... ]
        """
        self.header = HEADER
	self.events = []
	for e in events:
	    self.events.append(IcalEvent(e))

    def icalStr(self):
        result = HEADER
	for event in self.events:
	    result += event.icalStr()
	result += "END:VCALENDAR" + CRLF
	return result
    
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
        r  = "BEGIN:VEVENT" + CRLF

        fullName = tryGetFullName(self.fach)
        if fullName != "":
            summary += fullName
	    description += self.fach + "\\n"
        else:
            summary += self.fach
	    logging.warning("No full name found for '" + self.fach + "' in 'veranstaltungen.py'")
	r += summary + CRLF

        # DESCRIPTION
	if self.dozent != "":
	    description += "Prof.: " + self.dozent + "\\n\\n" + CRLF + " " 
	else:
	    description += "\\n"
	r += description + self.infoString + CRLF

        # DATETIME
        r += "DTSTART;TZID=Europe/Berlin:" + self.anfangsDatum + CRLF
	r += "DTEND;TZID=Europe/Berlin:" + self.endDatum + CRLF
	r += "DTSTAMP:" + self.dateTimeStamp + CRLF

	# LOCATION
	raum = ""
	if self.raum != "":
	    raum = "Rm. "
            if len(self.raum) == 4 and self.raum.isdigit():
                raum += self.raum[0:2] + "." + self.raum[2:4]
            else:
                raum += self.raum
	r += "LOCATION:" + raum + CRLF

	r += "UID:" + createUid(self.dateTimeStamp) + CRLF
	r += "END:VEVENT" + CRLF
	return r

def dateTime(jahrKuerzel, wochennummer, wochentag, uhrzeit):
    """@return: time.struct_time"""

    # remove the second year from a wintersemester
    jahrKuerzel = jahrKuerzel.split("/")[0]

    if (len(jahrKuerzel) == 2):
        jahr = "20" + jahrKuerzel
    else:
        jahr = jahrKuerzel

    if (int(wochennummer) > 52):
      wochennummer = str(int(wochennummer) - 52)
      jahr = "%.4d" % (int(jahr) + 1)

    wochentage = {"mo": "1", "di": "2", "mi": "3", "do": "4", "fr": "5", "sa": "6", "so": "0"}
    wochentag = wochentage[wochentag.lower()]

    stunde, minute = uhrzeit

    struct_time = time.strptime(jahr + " " + wochennummer + " " + wochentag + " " + stunde + " " + minute, "%Y %W %w %H %M")
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

    import socket
    #FIXME: Does not handle with ipv6
    try:
      ip = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]
              if not ip.startswith("127.")][0]
    except Exception as e:
      ip = ""

    return dateTime + " Atomkraft? Nein Danke! " + rand + "@" + ip

def test():
    dateTimeString = createDateTimeString(time.localtime())
    print dateTimeString
    print createUid(dateTimeString)


if __name__ == "__main__":
    test()

