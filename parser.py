from simpleparse.common import numbers
from simpleparse.parser import Parser

declaration = r'''#<token> := <definition>
datei         := (t/lb)*, header, ( (t/lb)*, section)+

header        := ersteZeile, lb, zweiteZeile
ersteZeile    := "Stundenplan", ts, semester, ts, "(Vers.", version, " vom ", versionsDatum, ")"
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
t             := [ \t]
keinTrenner   := -tr
tr            := ','
lb            := "\r\n" / '\n'
'''

parser = Parser(declaration, "datei")

from pprint import pprint
from simpleparse import dispatchprocessor
class HawProcessor( dispatchprocessor.DispatchProcessor ):
	"""Processor sub-class defining processing functions for the productions"""
	# you'd likely provide a "resetBeforeParse" method
	# in a real-world application, but we don't store anything
	# in our parser.
	def header( self, tup, buffer):
	    print "header"
	def ersteZeile( self, tup, buffer): 
	    print "ersteZeile"
	def semester( self, tup, buffer): pass
	def jahr( self, tup, buffer): pass
	def zweiteZeile( self, tup, buffer): pass
	def version( self, tup, buffer): pass
	def versionsDatum( self, tup, buffer): pass

	def section( self, tup, buffer):
	    print "section"
	    sectionTree = dispatchprocessor.multiMap(tup[-1],buffer=buffer)
#            pprint(sectionTree['eintrag'])
            wochen = dispatchprocessor.dispatchList(self,sectionTree['wochen'], buffer)[0]
	    print "wochen: "
	    print(str( wochen))
	    eintraege = dispatchprocessor.dispatchList(self,sectionTree['eintrag'], buffer)
	    print "eintraege: "
	    print(str(eintraege))

	def wochen( self, tup, buffer):
	    subTree = dispatchprocessor.multiMap(tup[-1],buffer=buffer)
	    wochen = dispatchprocessor.dispatchList(self,subTree['woche'], buffer)
	    return wochen
	def woche(self,tup,buffer):
	    return str(dispatchprocessor.getString(tup, buffer))
	def bezeichner( self, tup, buffer):pass
	def eintrag( self, tup, buffer):
	    return "eintrag"
	def fach(self, tup, buffer):
	    return str(dispatchprocessor.getString(tup, buffer))
	def dozent( self, tup, buffer):
	    return str(dispatchprocessor.getString(tup, buffer))
	def raum( self, tup, buffer):
	    return str(dispatchprocessor.getString(tup, buffer))
	def tag( self, tup, buffer):
	    return str(dispatchprocessor.getString(tup, buffer))
	def anfang( self, tup, buffer): pass
	def ende( self, tup, buffer): pass

	def uhrzeit( self, tup, buffer):pass
	def h( self, tup, buffer):
	    return repr(dispatchprocessor.getString(tup, buffer))
	def m( self, tup, buffer):
	    return repr(dispatchprocessor.getString(tup, buffer))
	def ts( self, tup, buffer): pass
	def t( self, tup, buffer): pass
	def keinTrenner( self, tup, buffer): pass
	def tr( self, tup, buffer): pass
	def lb( self, tup, buffer): pass


if __name__ == "__main__":
    file = open("/home/theno/hawicalendar/musterMinimal", "r")
    text = file.read()
    file.close()
    
    result = parser.parse(text, processor=HawProcessor())
#    result = parser.parse(text)
    
    pprint(result)

#    dp = HawProcessor()
#
#    from simpleparse.dispatchprocessor import *
#    dispatch(dp, ["section"] , text)

    # dispatch the tree-results




