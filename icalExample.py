from icalendar import Calendar, Event, Timezone
cal = Calendar()
from datetime import datetime
from icalendar import UTC # timezone
#cal.add('prodid', 'prodid text')
#cal.add('version', '2.0')

#test for timezones
from icalendar.prop import LocalTimezone, DSTOFFSET, STDOFFSET
print datetime(2011,3,26,8,0,0,tzinfo=LocalTimezone())
print datetime(2011,3,27,8,0,0,tzinfo=LocalTimezone())
print 
#print DSTOFFSET
#print STDOFFSET
#
#tz = Timezone()
#tz.add('tzid', "Europe/Berlin")
#tz.add('standardc', "CET")
#tz.add('daylightc', "CEST")
#tz.add('dtstart', datetime(1970,3,29,02,0,0))
#tz.add('tzoffsetTo', DSTOFFSET)
#tz.add('tzoffsettFrom', STDOFFSET)
#cal.add_component(tz)

event = Event()
event['uid'] = 'fooBarBaz03'
event.add('dtstart', datetime(2011,3,26,8,0,0,tzinfo=LocalTimezone())) #start: 8 Uhr, Sommerzeit
event.add('dtend', datetime(2011,3,26,10,0,0,tzinfo=LocalTimezone()))
event.add('dtstamp', datetime(2010,3,4,0,10,0,tzinfo=LocalTimezone()))
event.add('summary', 'Summary Text')
event.add('description', 'This is the description text')
event.add('location', 'Rm. 580')
cal.add_component(event)

event = Event()
event['uid'] = 'fooBarBaz04'
event.add('dtstart', datetime(2011,3,27,8,0,0,tzinfo=LocalTimezone())) #start: 8 Uhr, Sommerzeit
event.add('dtend', datetime(2011,3,27,10,0,0,tzinfo=LocalTimezone()))
event.add('dtstamp', datetime(2010,3,4,0,10,0,tzinfo=LocalTimezone()))
event.add('summary', 'Summary Text')
event.add('description', 'This is the description text')
event.add('location', 'Rm. 580')
cal.add_component(event)

# FIXME: workaround
calStr = cal.as_string().replace(";VALUE=DATE", "")

f = open('example.ics', 'wb')
f.write(calStr)
f.close()

print calStr
#validator: http://severinghaus.org/projects/icv/
