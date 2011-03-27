# -*- coding: utf-8 -*-

from simpleparse.common import numbers #for token 'int'
from simpleparse.parser import Parser

declaration = r'''#<token> := <definition>
root          := veranstaltung
veranstaltung := uebung / vorlUebung / vorkurs / orientierungseinheit /
                  wahlpflichtmodul / wpPraktikum / seminar /
                  teamStudienEinstieg / awSeminar / projekt /
                  praktikum / gwKurs / vorlesung / unknown

gwKurs               := "GW", [ub], " ", gwKuerzel
orientierungseinheit := semesterkuerzel, "-", "OE ", (oe2 / oe1)
praktikum            := semesterkuerzel, "-", prakKuerzel, no?, "/", gruppe
projekt              := ("INF-PRO ", gruppe) / ("MINF", int, "-PJ", nummer)
teamStudienEinstieg  := semesterkuerzel, "-TSE/", gruppe
seminar              := semesterkuerzel, "-", ("AIS"/"TIS"), "+", semesterkuerzel, "-", ("AIS"/"TIS")
awSeminar            := semesterkuerzel, "-", "AW", nummer
uebung               := semesterkuerzel, "-", kuerzel, "Ü", no?, "/", gruppe
#vorlesung           := semesterkuerzel, "-", kuerzel, no?
vorlesung            := semesterkuerzel, "-", kuerzel
vorkurs              := "Vorkurs ", fachKuerzel
vorlUebung           := semesterkuerzel, "-", kuerzel, "/", kuerzel, "Ü"
wahlpflichtmodul     := "INF-WP-", alphanumGruppe, no
wpPraktikum          := "INF-WPP-", alphanumGruppe, no, "/", gruppe
#catch all:
unknown              := -[$]+

semesterkuerzel      := -"-"+
>kuerzel<            := fachKuerzel, nummer?
prakKuerzel          := ([A-O,Q-Z]*, "P")+
fachKuerzel          := [A-Z]+
gwKuerzel            := [A-Z_-]+, (" ", [a-zA-Z]+)?
oe1                  := "I"
oe2                  := "II"
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

