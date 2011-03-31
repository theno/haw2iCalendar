# -*- coding: utf-8 -*-

import unittest

from veranstaltungenParser import VeranstaltungParser

tokenTestData = {
    # low level token
    "semesterkuerzel" : ["BTI5", "BAI5", "BAI1", "MINF2"],
    "kuerzel" : ["PJ1", "AW2", "DB"],
    "fachKuerzel" : ["PJ", "AW", "DB"],
    "gwKuerzel" : ["DANN", "ZOEL", "STFF_Z", "SRHF_TK"],

    # mid level token
    "gwKurs" : ["GWb SRHF_TK", "GWu STFF_Z", "GWu ZOEL", "GWu DANN"],
    "orientierungseinheit" : ["BTI1-OE I", "BTI2-OE II"],
    "praktikum" : ["BAI1-PRP1/02", "BTI1-GTP/02"],
    "projekt" : ["INF-PRO 8", "INF-PRO 4"],
    "teamStudienEinstieg" :["BTI1-TSE/02", "BTI1-TSE/01", "BAI1-TSE/02"],
    "seminar" : ["BAI5-AIS+BTI5-TIS"],
    "awSeminar" : ["MINF1-AW1", "MINF2-AW2"],
    "uebung" : ["MINF2-THÜ/01"],
    "vorlesung" : ["BAI1-PR1"],
    "vorkurs" : ["Vorkurs PRG"],
    "vorlUebung" : ["BAI1-GI/GIÜ"],
    "wahlpflichtmodul" : ["INF-WP-C1"],
    "wpPraktikum" : ["INF-WPP-B4/01", "INF-WPP-A1/01"],

    # high level token
    "veranstaltung" : ["INF-WPP-B4/01", "INF-WPP-A1/01",
                       "GWb SRHF_TK", "GWu STFF_Z",
                       "GWu ZOEL", "GWu DANN",
                       "BTI1-OE I", "BTI2-OE II",
                       "BAI1-PRP1/02", "BTI1-GTP/02",
                       "INF-PRO 8", "INF-PRO 4",
                       "BAI5-AIS+BTI5-TIS",
                       "MINF2-THÜ/01",
                       "BAI1-PR1",
                       "Vorkurs PRG",
                       "BAI1-GI/GIÜ",
                       "INF-WP-C1",
                       "MINF1-AW1", "MINF2-AW2"]
}

class TestParser(unittest.TestCase):
    def testDeclaration(self):
        
	for token in tokenTestData:
	    production = token
	    testData = tokenTestData[token]
	    for testDatum in testData:
	        success, children, nextcharacter = VeranstaltungParser.parse(testDatum, production)
		def errStr():
		    from pprint import pformat
		    r =  """Could not parse %s\nas a\n\n%s\t(%s chars parsed of %s)"""%(
		             repr(testDatum), production, nextcharacter, len(testDatum))
	            r += "\n\nreturned value was:\n\n" + pformat((success, children, nextcharacter))
	            r += "\n\nparsed:\n+++\n" + str(testDatum)[0:nextcharacter] + "\n+++"
	            r += "\n\nNOT parsed:\n+++\n" + str(testDatum)[nextcharacter:len(testDatum)] + "\n+++"
		    return r
		assert success and nextcharacter==len(testDatum), errStr()


if __name__ == "__main__":
    unittest.main()

