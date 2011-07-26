# -*- coding: utf-8 -*-

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

import unittest

from veranstaltungenParser import VeranstaltungParser

tokenTestData = {
    # low level token
    "fachKuerzel" : ["PJ", "AW", "DB"],
    "gwKuerzel" : ["DANN", "ZOEL", "STFF_Z", "SRHF_TK"],
    "kuerzel" : ["PJ1", "AW2", "DB"],
    "semesterkuerzel" : ["BTI5", "BAI5", "BAI1", "MINF2", "A-M2"],

    # mid level token
    "awSeminar" : ["MINF1-AW1", "MINF2-AW2"],
    "gwKurs" : ["GWb SRHF_TK", "GWu STFF_Z", "GWu ZOEL", "GWu DANN", "GW MATT", "GW RDTK SL", "GW SRHF_TK"],
    "labor" : ["IE2-EEL2/01", "BMT6-Robot L"],
    "orientierungseinheit" : ["BTI1-OE I", "BTI2-OE II"],
    "praktikum" : ["BAI1-PRP1/02", "BTI1-GTP/02", "A-M2-PSP"],
    "projekt" : ["INF-PRO 8", "INF-PRO 4"],
    "seminar" : ["BAI5-AIS+BTI5-TIS"],
    "teamStudienEinstieg" : ["BTI1-TSE/02", "BTI1-TSE/01", "BAI1-TSE/02", "E1a-TSE"],
    "tutorium" : ["E1a-ET1 Tutor", "E1b-PH1 Tutor", "E4a/b GR Tutor"],
    "uebung" : ["MINF2-THÜ/01", "BMT2-TM2 Ü/01"],
    "verbundprojekt" : ["A-M2-VPJ"],
    "vorkurs" : ["Vorkurs PRG"],
    "vorlesung" : ["BAI1-PR1"],
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
                       "MINF2-THÜ/01", "BMT2-TM2 Ü/01",
                       "BAI1-PR1", "E1a-TSE",
                       "IE2-EEL2/01", "BMT6-Robot L",
                       "E1a-ET1 Tutor", "E1b-PH1 Tutor",
                       "Vorkurs PRG",
                       "A-M2-VPJ",
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

