from simpleparse.common import numbers
from simpleparse.parser import Parser

declaration = r'''#<token> := <definition>
datei         := (t/lb)*, header, sections
sections      := ((t/lb)*, section)+

header        := ersteZeile, lb, zweiteZeile
ersteZeile    := "Stundenplan", ts, infoString
infoString    := semester, ts, "(Vers.", version, " vom ", versionsDatum, ")"
semester      := "WiSe"/"SoSe", ts, jahr
jahr          := int
zweiteZeile   := -lb+
version       := -ts+
versionsDatum := -')'+

section       := wochen, lb, bezeichner, (lb, eintrag)+
wochen        := woche, (", ", woche)*
woche         := int
bezeichner    := -lb+
eintrag       := fach, tr, dozent, tr, raum, tr, tag, tr, anfang, tr, ende
fach          := keinTrenner+
dozent        := keinTrenner*
raum          := keinTrenner+
tag           := c"Mo"/c"Di"/c"Mi"/c"Do"/c"Fr"/c"Sa"/c"So"
anfang        := uhrzeit
ende          := uhrzeit

uhrzeit       := h, ':', m
h             := int
m             := int
ts            := t*
<t>             := [ \t]
keinTrenner   := -tr
tr            := ','
<lb>           := "\r\n" / '\n'
'''

parser = Parser(declaration, "datei")

from pprint import pprint
from simpleparse import dispatchprocessor
class HawProcessor( dispatchprocessor.DispatchProcessor ):
        def init(self):
	    self.general = None
	    self.events = None
	"""Processor sub-class defining processing functions for the productions"""
	# you'd likely provide a "resetBeforeParse" method
	# in a real-world application, but we don't store anything
	# in our parser.
	def header(self, tup, buffer):
	    subTree = dispatchprocessor.multiMap(tup[-1],buffer=buffer)
	    infoString = dispatchprocessor.dispatchList(self,subTree['ersteZeile'], buffer)[0]
	    #print "infoString:"
	    #print infoString
	    return infoString
	def ersteZeile(self, tup, buffer): 
	    subTree = dispatchprocessor.multiMap(tup[-1],buffer=buffer)
	    infoString = dispatchprocessor.dispatchList(self,subTree['infoString'], buffer)[0]
	    return infoString
	def infoString(self, tup, buffer):
	    return str(dispatchprocessor.getString(tup, buffer))
	def semester(self, tup, buffer): pass
	def jahr(self, tup, buffer): pass
	def zweiteZeile(self, tup, buffer): pass
	def version(self, tup, buffer): pass
	def versionsDatum(self, tup, buffer): pass

        def sections(self, tup, buffer):
	    subTree = dispatchprocessor.multiMap(tup[-1],buffer=buffer)
            eintraegeList = dispatchprocessor.dispatchList(self,subTree['section'], buffer)
	    eintraege = reduce(lambda x,y: x+y, eintraegeList)
#	    for faecher2 in faecherList:
#	        for fach in faecher2:
#		    if fach in faecher:
#		        faecher[fach].append(faecher2[fach])
#	            else:
#		        faecher[fach] = faecher2[fach]
	    return eintraege
	def section(self, tup, buffer):
	    #print "section"
	    subTree = dispatchprocessor.multiMap(tup[-1],buffer=buffer)
            #pprint(sectionTree['eintrag'])
            wochen = dispatchprocessor.dispatchList(self,subTree['wochen'], buffer)[0]
	    #print "wochen: "
	    #print(str( wochen))
	    eintraege = dispatchprocessor.dispatchList(self,subTree['eintrag'], buffer)
	    #print "eintraege: "
	    #print(str(eintraege))
	    eintraegeMitWoche = []
	    for woche in wochen:
	        for e in eintraege:
		    fach, dozent, raum, tag, anfang, ende = e
		    eintraegeMitWoche.append((fach, dozent, raum, woche, tag, anfang, ende))
	    return eintraegeMitWoche

	def wochen(self, tup, buffer):
	    subTree = dispatchprocessor.multiMap(tup[-1],buffer=buffer)
	    wochen = dispatchprocessor.dispatchList(self,subTree['woche'], buffer)
	    return wochen
	def woche(self,tup,buffer):
	    return str(dispatchprocessor.getString(tup, buffer))
	def bezeichner(self, tup, buffer):pass
	def eintrag(self, tup, buffer):
	    subTree = dispatchprocessor.multiMap(tup[-1],buffer=buffer)
	    fach = dispatchprocessor.dispatchList(self,subTree['fach'], buffer)[0]
	    dozent = dispatchprocessor.dispatchList(self,subTree['dozent'], buffer)[0]
	    raum = dispatchprocessor.dispatchList(self,subTree['raum'], buffer)[0]
	    tag = dispatchprocessor.dispatchList(self,subTree['tag'], buffer)[0]
	    anfang = dispatchprocessor.dispatchList(self,subTree['anfang'], buffer)[0]
	    ende = dispatchprocessor.dispatchList(self,subTree['ende'], buffer)[0]
	    return (fach, dozent, raum, tag, anfang, ende)
	def fach(self, tup, buffer):
	    return str(dispatchprocessor.getString(tup, buffer))
	def dozent(self, tup, buffer):
	    return str(dispatchprocessor.getString(tup, buffer))
	def raum(self, tup, buffer):
	    return str(dispatchprocessor.getString(tup, buffer))
	def tag(self, tup, buffer):
	    return str(dispatchprocessor.getString(tup, buffer))
	def anfang(self, tup, buffer):
	    subTree = dispatchprocessor.multiMap(tup[-1],buffer=buffer)
	    h, m = dispatchprocessor.dispatchList(self,subTree['uhrzeit'], buffer)[0]
	    return (h,m)
	def ende(self, tup, buffer):
	    subTree = dispatchprocessor.multiMap(tup[-1],buffer=buffer)
	    h, m = dispatchprocessor.dispatchList(self,subTree['uhrzeit'], buffer)[0]
	    return (h,m)
	def uhrzeit(self, tup, buffer):
	    subTree = dispatchprocessor.multiMap(tup[-1],buffer=buffer)
	    h = dispatchprocessor.dispatchList(self,subTree['h'], buffer)[0]
	    m = dispatchprocessor.dispatchList(self,subTree['m'], buffer)[0]
	    return (h,m)
	def h(self, tup, buffer):
	    return str(dispatchprocessor.getString(tup, buffer))
	def m(self, tup, buffer):
	    return str(dispatchprocessor.getString(tup, buffer))
	def ts(self, tup, buffer): pass
	def t(self, tup, buffer): pass
	def keinTrenner(self, tup, buffer): pass
	def tr(self, tup, buffer): pass
	def lb(self, tup, buffer): pass


if __name__ == "__main__":
    file = open("/home/theno/hawicalendar/muster.txt", "r")
    text = file.read()
    file.close()
    
    success, result, strPtr = parser.parse(text, processor=HawProcessor())
#    result = parser.parse(text)
    
    print "result:"
    pprint(result)

#    dp = HawProcessor()
#
#    from simpleparse.dispatchprocessor import *
#    dispatch(dp, ["section"] , text)

    # dispatch the tree-results




