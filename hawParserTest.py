import unittest

from hawParser import HawParser

sectionTestDatum = r"""15, 18, 21
Name,Dozent,Raum,Tag,Anfang,Ende
BTI3-SEP1/02,DAI,0709,Mi,8:15,11:30
BTI3-DTP/03,CNZ/[Vol],0801,Mi,12:30,15:45
BTI3-BSP/01,FHL/[Loh],0701,Mi,12:30,15:45
BTI3-ADP/02,PRG/[Nmn],1105,Mi,8:15,11:30
BTI3-SE1,DAI,0460,Fr,8:15,11:30
BTI3-DT,CNZ,1065,Do,8:15,11:30
BTI3-BS,FHL,1001,Di,12:30,15:45
BTI3-AD,PRG/SCHM,1260,Do,12:30,15:45
BTI3-AA/AAU,BRN,0360,Mo,8:15,13:30"""

semestergruppeTestDatum = r"""Stundenplan  SoSe 11 (Vers.0.9 vom 1.3.11)
Semestergruppe  B-AI1


10
Name,Dozent,Raum,Tag,Anfang,Ende
BAI1-OE I,,1260,Do,9:00,17:00
BAI1-OE I,,1260,Fr,9:00,17:00

11, 12, 14
Name,Dozent,Raum,Tag,Anfang,Ende
Vorkurs PRG,,1101a,Do,8:15,14:35
Vorkurs PRG,,1101b,Fr,8:15,14:35
Vorkurs PRG,,1102,Do,8:15,14:35
BAI1-OE I,,1260,Mo,9:00,17:00
BAI1-OE I,,1260,Di,9:00,17:00
BAI1-OE I,,1260,Mi,9:00,17:00"""

semestergruppeTestDatum2 = r"""Stundenplan  SoSe 11 (Vers.0.9 vom 1.3.11)
Semestergruppe  M-INF2


12-14, 16, 23
Name,Dozent,Raum,Tag,Anfang,Ende
MINF2-TH1/ue,HFFM,0480,Di,12:30,15:45
MINF2-TH1,HFFM,0480,Di,12:30,15:45"""


dateiTestDatum = semestergruppeTestDatum
dateiTestDatum2 = semestergruppeTestDatum + "\n" + semestergruppeTestDatum2
dateiTestDatum3 = """Stundenplan  SoSe 11 (Vers.0.9 vom 1.3.11)
Semestergruppe  M-AI1


10-11
Name,Dozent,Raum,Tag,Anfang,Ende
BAI1-OE I,,1260,Do,9:00,17:00
BAI1-OE I,,1260,Fr,9:00,17:00
Stundenplan  SoSe 11 (Vers.0.9 vom 1.3.11)
Semestergruppe  M-INF2


12-14, 16, 23
Name,Dozent,Raum,Tag,Anfang,Ende
MINF2-TH1/ue,HFFM,0480,Di,12:30,15:45
MINF2-TH1,HFFM,0480,Di,12:30,15:45"""

f = open("Sem_I.txt", 'r')
dateiTestDatum4 = f.read()
f.close()

class TestParser(unittest.TestCase):
    def testDeclaration(self):
        
        tokenTestData = {
            "uhrzeit" : ["17:00", "9:00", "8:15", "24:66"],
	    "wochentag" : ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So", "mo", "mO", "MO"],
	    "raum" : ["1260", "1101b", "1101a", "irgendwasOhneKomma"],
	    "dozent" : ["SRS", "WND/[Oel]"],
	    "wochen" : ["11", "12, 18, 21"],
	    "bezeichner" : ["Name, Dozent, Raum, Tag, Anfang, Ende"],
	    "section" : [ sectionTestDatum ],

	    "versionsDatum" : ["1.3.11"],
	    "semester" : ["SoSe 11", "WiSe 10"],
	    "ersteZeile" : ["Stundenplan  SoSe 11 (Vers.0.9 vom 1.3.11)",
	                    "Stundenplan  SoSe 11 (Vers.0.9 vom 1.3.11)"],
	    "zweiteZeile" : ["Semestergruppe  M-AI1"],
	    "header" : ["Stundenplan  SoSe 11 (Vers.0.9 vom 1.3.11)\nSemestergruppe  M-AI1"],
	    "semestergruppe" : [semestergruppeTestDatum, semestergruppeTestDatum2],
	    "datei" : [dateiTestDatum, dateiTestDatum2, dateiTestDatum3, dateiTestDatum4]
	}

	for token in tokenTestData:
	    production = token
	    testData = tokenTestData[token]
	    for testDatum in testData:
	        success, children, nextcharacter = HawParser.parse(testDatum, production)
		from pprint import pformat
		def errStr():
		    from pprint import pprint
		    r =  """Could not parse %s\nas a\n\n%s\t(%s chars parsed of %s)"""%(
		             repr(testDatum), production, nextcharacter, len(testDatum))
	            r += "\n\nreturned value was:\n\n" + pformat((success, children, nextcharacter))
	            r += "\n\nparsed:\n+++\n" + str(testDatum)[0:nextcharacter] + "\n+++"
	            r += "\n\nNOT parsed:\n+++\n" + str(testDatum)[nextcharacter:len(testDatum)] + "\n+++"
		    return r
		assert success and nextcharacter==len(testDatum), errStr()


if __name__ == "__main__":
    unittest.main()

