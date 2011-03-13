from simpleparse import dispatchprocessor
from simpleparse.dispatchprocessor import dispatchList, getString, multiMap

class HawDispatchProcessor( dispatchprocessor.DispatchProcessor ):
#        def init(self):
#	    self.general = None
#	    self.events = None
	"""Processor sub-class defining processing functions for the productions"""
	# you'd likely provide a "resetBeforeParse" method
	# in a real-world application, but we don't store anything
	# in our parser.
	def datei(self,tup,buffer):
	    subTree = multiMap(tup[-1],buffer=buffer)
	    infoString = dispatchList(self,subTree['header'], buffer)[0]
	    eintraege = dispatchList(self,subTree['sections'], buffer)[0]
	    eintraege2 = []
	    for e in eintraege:
	        fach, dozent, raum, woche, tag, anfang, ende = e
		eintraege2.append((fach, dozent, raum, woche, tag, anfang, ende, infoString))
	    return eintraege2

	def header(self, tup, buffer):
	    subTree = multiMap(tup[-1],buffer=buffer)
	    infoString = dispatchList(self,subTree['ersteZeile'], buffer)[0]
	    return infoString
	def ersteZeile(self, tup, buffer): 
	    subTree = multiMap(tup[-1],buffer=buffer)
	    infoString = dispatchList(self,subTree['infoString'], buffer)[0]
	    return infoString
	def infoString(self, tup, buffer):
	    return str(getString(tup, buffer))

        def sections(self, tup, buffer):
	    subTree = multiMap(tup[-1],buffer=buffer)
            eintraegeList = dispatchList(self,subTree['section'], buffer)
	    eintraege = reduce(lambda x,y: x+y, eintraegeList)
	    return eintraege
	def section(self, tup, buffer):
	    subTree = multiMap(tup[-1],buffer=buffer)
            wochen = dispatchList(self,subTree['wochen'], buffer)[0]
	    eintraege = dispatchList(self,subTree['eintrag'], buffer)
	    eintraegeMitWoche = []
	    for woche in wochen:
	        for e in eintraege:
		    fach, dozent, raum, tag, anfang, ende = e
		    eintraegeMitWoche.append((fach, dozent, raum, woche, tag, anfang, ende))
	    return eintraegeMitWoche

	def wochen(self, tup, buffer):
	    subTree = multiMap(tup[-1],buffer=buffer)
	    wochen = dispatchList(self,subTree['woche'], buffer)
	    return wochen
	def woche(self,tup,buffer):
	    return str(getString(tup, buffer))
	def eintrag(self, tup, buffer):
	    subTree = multiMap(tup[-1],buffer=buffer)
	    fach = dispatchList(self,subTree['fach'], buffer)[0]
	    dozent = dispatchList(self,subTree['dozent'], buffer)[0]
	    raum = dispatchList(self,subTree['raum'], buffer)[0]
	    tag = dispatchList(self,subTree['tag'], buffer)[0]
	    anfang = dispatchList(self,subTree['anfang'], buffer)[0]
	    ende = dispatchList(self,subTree['ende'], buffer)[0]
	    return (fach, dozent, raum, tag, anfang, ende)
	def fach(self, tup, buffer):
	    return str(getString(tup, buffer))
	def dozent(self, tup, buffer):
	    return str(getString(tup, buffer))
	def raum(self, tup, buffer):
	    return str(getString(tup, buffer))
	def tag(self, tup, buffer):
	    return str(getString(tup, buffer))
	def anfang(self, tup, buffer):
	    subTree = multiMap(tup[-1],buffer=buffer)
	    h, m = dispatchList(self,subTree['uhrzeit'], buffer)[0]
	    return (h,m)
	def ende(self, tup, buffer):
	    subTree = multiMap(tup[-1],buffer=buffer)
	    h, m = dispatchList(self,subTree['uhrzeit'], buffer)[0]
	    return (h,m)
	def uhrzeit(self, tup, buffer):
	    subTree = multiMap(tup[-1],buffer=buffer)
	    h = dispatchList(self,subTree['h'], buffer)[0]
	    m = dispatchList(self,subTree['m'], buffer)[0]
	    return (h,m)
	def h(self, tup, buffer):
	    return str(getString(tup, buffer))
	def m(self, tup, buffer):
	    return str(getString(tup, buffer))
