# -*- coding: utf-8 -*-

from simpleparse.common import numbers #for token 'int'
from simpleparse.parser import Parser

declaration = r'''#<token> := <definition>
root          := veranstaltung
veranstaltung := uebung / vorlUebung / vorkurs / orientierungseinheit /
                  wahlpflichtmodul / wpPraktikum / seminar / projekt /
                  praktikum / gwKurs / vorlesung / unknown

gwKurs               := "GW", [ub], " ", gwKuerzel
orientierungseinheit := semesterkuerzel, "-", "OE ", (oe2 / oe1)
praktikum            := semesterkuerzel, "-", prakKuerzel, no?, "/", gruppe
projekt              := "INF-PRO ", gruppe
seminar              := semesterkuerzel, "-", ("AIS"/"TIS"), "+", semesterkuerzel, "-", ("AIS"/"TIS")
uebung               := semesterkuerzel, "-", kuerzel, "Ü", no?, "/", gruppe
#vorlesung            := semesterkuerzel, "-", kuerzel, no?
vorlesung            := semesterkuerzel, "-", kuerzel
vorkurs              := "Vorkurs ", fachKuerzel
vorlUebung           := semesterkuerzel, "-", kuerzel, "/", kuerzel, "Ü"
wahlpflichtmodul     := "INF-WP-", alphanumGruppe, no
wpPraktikum          := "INF-WPP-", alphanumGruppe, no, "/", gruppe
unknown              := -[$]+

semesterkuerzel      := -"-"+
>kuerzel<            := fachKuerzel, nummer?
prakKuerzel          := ([A-O,Q-Z]*, "P")+
fachKuerzel          := [A-Z]+
gwKuerzel            := [A-Z_-]+
oe1                  := "I"
oe2                  := "II"
nummer               := int
no                   := int
gruppe               := int
alphanumGruppe       := [A-Z]
'''
VeranstaltungParser = Parser(declaration, root="root")

def test2():
    from simpleparse import dispatchprocessor
    from simpleparse.dispatchprocessor import dispatchList, getString, multiMap
    
    from veranstaltungenDispatchProcessor import VeranstaltungDispatchProcessor
    #success, children, nextcharacter = VeranstaltungParser.parse("BAI1-PR1")
    from pprint import pprint
    pprint(VeranstaltungParser.parse("BAI1-PR1", processor=VeranstaltungDispatchProcessor()))
#    pprint(VeranstaltungParser.parse("fooBarBaz", processor=VeranstaltungDispatchProcessor()))


############################################################
fullNames = {

# Master Informatik

"MINF1-AW1"     : "Seminar Anwendungen 1",
"MINF1-TT1"     : "Vorl. Technik und Technologie 1",
"MINF1-MT"      : "Vorl. Modellierung Technischer Systeme",
"MINF1-MI"      : "Vorl. Modellierung von Informationssystemen",

"MINF2-TH1"      : "Vorl. Theoretische Informatik",
"MINF2-THÜ/01"  : "Übung Theoretische Informatik (Gruppe 1)",
"MINF2-THÜ/02"  : "Übung Theoretische Informatik (Gruppe 2)",
"MINF2-AW2"     : "Seminar Anwendungen 2",
"MINF2-TT2"     : "Vorl. Technik und Technologie 2",
"MINF2-TTP2/01" : "Praktikum Technik und Technologie (Gruppe 1)",
"MINF2-TTP2/02" : "Praktikum Technik und Technologie (Gruppe 2)",
"MINF2-PJ1"     : "Projekt I",

"MINF3-SEM"     : "Seminar",
"MINF3-TH2"     : "Vorl. Theoretische Informatik 2",
"MINF3-THÜ1/01" : "Übung Theoretische Informatik 3 (Gruppe 1)",
"MINF3-THÜ1/02" : "Übung Theoretische Informatik 3 (Gruppe 2)",
"MINF3-PJ2"     : "Projekt II",
"MINF3-UO"      : "Vorlesung Unternehmensorientierung",
"MINF3-UOÜ/01"  : "Übung Unternehmensorientierung (Gruppe 1)",
"MINF3-UOÜ/02"  : "Übung Unternehmensorientierung (Gruppe 2)",

"MINF4-MA"      : "Masterthesis",
"MINF4-MAK"     : "Kolloquium"
}

def tryGetFullName(veranstaltung):
    from veranstaltungenDispatchProcessor import VeranstaltungDispatchProcessor

    fullName = ""
    success, result, nextcharacter = VeranstaltungParser.parse(veranstaltung, processor=VeranstaltungDispatchProcessor())
    if success:
        fullName = result[0]
    return fullName

def test():
    from pprint import pprint
    pprint(fullNames)
    
if __name__ == "__main__":
    test2()

