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

from simpleparse.common import numbers #for token 'int'
from simpleparse.parser import Parser

declaration = r'''#<token> := <definition>
root          := veranstaltung
veranstaltung := uebung / vorlUebung / vorkurs / orientierungseinheit /
                  wahlpflichtmodul / wpPraktikum / seminar / verbundprojekt /
                  teamStudienEinstieg / awSeminar / projekt / labor / tutorium /
                  praktikum / gwKurs / vorlesung / unknown

awSeminar            := semesterkuerzel, "-", "AW", nummer
gwKurs               := "GW", [ub]?, " ", gwKuerzel
labor                := semesterkuerzel, "-", labKuerzel, no?, ("/", gruppe)?
orientierungseinheit := semesterkuerzel, [- ], "OE", (" ", oe2 / oe1 )?
praktikum            := semesterkuerzel, ("- " / "-" / " "), prakKuerzel, no?, ("/", gruppe)?
projekt              := ("INF-PRO ", gruppe) / ("MINF", int, "-PJ", nummer)
seminar              := semesterkuerzel, "-", ("AIS"/"TIS"), "+", semesterkuerzel, "-", ("AIS"/"TIS")
teamStudienEinstieg  := semesterkuerzel, [- ], "TSE", ("/", gruppe)?
tutorium             := (semesterkuerzel, "-") / ("E4a/b "), kuerzel, " Tutor"
uebung               := semesterkuerzel, "-", kuerzel, " "?, ("Ü"/"U"), no?, "/", gruppe
verbundprojekt       := semesterkuerzel, "-", verbKuerzel, no?, ("/", gruppe)?
vorkurs              := "Vorkurs ", fachKuerzel
vorlesung            := semesterkuerzel, ("- " / "-" / " "), kuerzel, ("/", gruppe)?
vorlUebung           := semesterkuerzel, "-", kuerzel, "/", kuerzel, "Ü"
wahlpflichtmodul     := "INF-WP-", alphanumGruppe, no
wpPraktikum          := "INF-WPP-", alphanumGruppe, no, "/", gruppe
#catch all:
unknown              := -[$]+

semesterkuerzel      := ("A-M", [0-9]) / ("IK-M", [0-9]) / ("BWI", [0-9]) / "MINF1" / "BMT5" / "BTI1" / -"-"+
>kuerzel<            := fachKuerzel, nummer?
prakKuerzel          := (?-"RMP", [A-Z], [A-Z], "P") / ([A-Z], [A-Z], [A-Z], "P")
verbKuerzel          := [A-Z], [A-Z], "J"
labKuerzel           := ([A-Z], [A-Z], "L") / (fachKuerzel, " L")
gwKuerzel            := [A-Z_-]+, (" ", [a-zA-Z]+)?
oe1                  := "I"
oe2                  := "II"
fachKuerzel          := [a-zA-Z]+
nummer               := int
no                   := int
gruppe               := int
alphanumGruppe       := [A-Z]
'''
VeranstaltungParser = Parser(declaration, root="root")

def tryGetFullName(veranstaltung):
    from veranstaltungenDispatchProcessor import VeranstaltungDispatchProcessor

    fullName = ""
    success, result, nextcharacter = VeranstaltungParser.parse(veranstaltung, processor=VeranstaltungDispatchProcessor())
    if success:
        fullName = result[0]
    return fullName

def test():
    from simpleparse import dispatchprocessor
    from simpleparse.dispatchprocessor import dispatchList, getString, multiMap
    
    from veranstaltungenDispatchProcessor import VeranstaltungDispatchProcessor
    #success, children, nextcharacter = VeranstaltungParser.parse("BAI1-PR1")
    from pprint import pprint
    pprint(VeranstaltungParser.parse("BAI1-PR1", processor=VeranstaltungDispatchProcessor()))
#    pprint(VeranstaltungParser.parse("fooBarBaz", processor=VeranstaltungDispatchProcessor()))

if __name__ == "__main__":
    test()

