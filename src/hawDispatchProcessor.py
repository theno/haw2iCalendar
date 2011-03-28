from simpleparse import dispatchprocessor
from simpleparse.dispatchprocessor import dispatchList, getString, multiMap

class HawDispatchProcessor( dispatchprocessor.DispatchProcessor ):
	def semestergruppe(self,tup,buffer):
            """@result: 
            
            (semestergruppenKuerzel, [(fach, dozent, raum, jahr, woche, wochentag, anfang, ende, infoString),
                                      (eintrag-Tupel),
                                      ...
                                     ]
            )
            """
	    subTree = multiMap(tup[-1],buffer=buffer)
	    infoString, jahr, gruppenKuerzel = dispatchList(self,subTree['header'], buffer)[0]
	    eintraege = dispatchList(self,subTree['sections'], buffer)[0]
	    eintraege2 = []
	    for e in eintraege:
	        fach, dozent, raum, woche, wochentag, anfang, ende = e
		eintraege2.append((fach, dozent, raum, jahr, woche, wochentag, anfang, ende, infoString))
	    return gruppenKuerzel, eintraege2

	def header(self, tup, buffer):
	    subTree = multiMap(tup[-1],buffer=buffer)
	    infoString, jahr = dispatchList(self,subTree['ersteZeile'], buffer)[0]
	    gruppenKuerzel = dispatchList(self,subTree['zweiteZeile'], buffer)[0]
	    return (infoString, jahr, gruppenKuerzel)
	def ersteZeile(self, tup, buffer): 
	    subTree = multiMap(tup[-1],buffer=buffer)
	    infoString, jahr = dispatchList(self,subTree['infoString'], buffer)[0]
	    return (infoString, jahr)
	def infoString(self, tup, buffer):
	    subTree = multiMap(tup[-1],buffer=buffer)
	    jahr = dispatchList(self,subTree['semester'], buffer)[0]
	    infoString = str(getString(tup, buffer))
	    return (infoString, jahr)
	def semester(self, tup, buffer):
	    subTree = multiMap(tup[-1],buffer=buffer)
	    jahr = dispatchList(self,subTree['jahr'], buffer)[0]
	    return jahr
	def jahr(self, tup, buffer):
	    return str(getString(tup, buffer))
	def zweiteZeile(self, tup, buffer):
	    subTree = multiMap(tup[-1],buffer=buffer)
	    gruppenKuerzel = dispatchList(self,subTree['gruppenKuerzel'], buffer)[0]
	    return gruppenKuerzel
	def gruppenKuerzel(self, tup, buffer):
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
		    fach, dozent, raum, wochentag, anfang, ende = e
		    eintraegeMitWoche.append((fach, dozent, raum, woche, wochentag, anfang, ende))
	    return eintraegeMitWoche

	def wochen(self, tup, buffer):
	    subTree = multiMap(tup[-1],buffer=buffer)
	    wochenList = dispatchList(self,subTree['wocheOrWochenRange'], buffer)
	    wochen = [item for sublist in wochenList for item in sublist]
	    return wochen
	def wocheOrWochenRange(self,tup,buffer):
	    subTree = multiMap(tup[-1],buffer=buffer)
	    wochen = []
	    if 'woche' in subTree:
	        wochen = dispatchList(self,subTree['woche'], buffer)
	    if 'wochenRange' in subTree:
 	        wochen = dispatchList(self,subTree['wochenRange'], buffer)[0]
	    return wochen
	def wochenRange(self, tup, buffer):
	    subTree = multiMap(tup[-1],buffer=buffer)
	    anfangsWoche = dispatchList(self,subTree['anfangsWoche'], buffer)[0]
	    endWoche = dispatchList(self,subTree['endWoche'], buffer)[0]
	    return map(lambda x: str(x), range(int(anfangsWoche), int(endWoche)+1) )
	def anfangsWoche(self, tup, buffer):
	    subTree = multiMap(tup[-1],buffer=buffer)
	    anfangsWoche = dispatchList(self,subTree['woche'], buffer)[0]
	    return anfangsWoche
	def endWoche(self, tup, buffer):
	    subTree = multiMap(tup[-1],buffer=buffer)
	    endWoche = dispatchList(self,subTree['woche'], buffer)[0]
	    return endWoche
	def woche(self,tup,buffer):
	    return str(getString(tup, buffer))
	def eintrag(self, tup, buffer):
	    subTree = multiMap(tup[-1],buffer=buffer)
	    fach = dispatchList(self,subTree['fach'], buffer)[0]
	    dozent = dispatchList(self,subTree['dozent'], buffer)[0]
	    raum = dispatchList(self,subTree['raum'], buffer)[0]
	    wochentag = dispatchList(self,subTree['wochentag'], buffer)[0]
	    anfang = dispatchList(self,subTree['anfang'], buffer)[0]
	    ende = dispatchList(self,subTree['ende'], buffer)[0]
	    return (fach, dozent, raum, wochentag, anfang, ende)
	def fach(self, tup, buffer):
	    return str(getString(tup, buffer))
	def dozent(self, tup, buffer):
	    return str(getString(tup, buffer))
	def raum(self, tup, buffer):
	    return str(getString(tup, buffer))
	def wochentag(self, tup, buffer):
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
