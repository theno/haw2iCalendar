# -*- coding: utf-8 -*-

from simpleparse import dispatchprocessor
from simpleparse.dispatchprocessor import dispatch, dispatchList, getString, multiMap

from veranstaltungen import VeranstaltungParser

class VeranstaltungDispatchProcessor( dispatchprocessor.DispatchProcessor ):
    def veranstaltung(self, tup, buffer):
        subTree = multiMap(tup[-1], buffer=buffer)
        def get(veranstaltung):
            return dispatchList(self, subTree[veranstaltung], buffer)[0]
        if "gwKurs" in subTree:
            result = get("gwKurs")
        elif "orientierungseinheit" in subTree:
            result = get("orientierungseinheit")
        elif "praktikum" in subTree:
            result = get("praktikum")
        elif "projekt" in subTree:
            result = get("projekt")
        elif "seminar" in subTree:
            result = get("seminar")
        elif "uebung" in subTree:
            result = get("uebung")
        elif "vorlesung" in subTree:
            result = get("vorlesung")
        elif "vorkurs" in subTree:
            result = get("vorkurs")
        elif "vorlUebung" in subTree:
            result = get("vorlUebung")
        elif "wahlpflichtmodul" in subTree:
            result = get("wahlpflichtmodul")
        elif "wpPraktikum" in subTree:
            result = get("wpPraktikum")
        elif "unknown" in subTree:
            result = buffer # no mappings found
        else:
            raise Exception("wrong control flow! Veranstaltungskuerzel = " + buffer)
        return result

    def gwKurs(self, tup, buffer):
        subTree = multiMap(tup[-1],buffer=buffer)
        gwKuerzel = dispatchList(self, subTree['gwKuerzel'], buffer)[0]
        return gwKurs2FullName(gwKuerzel)

    def orientierungseinheit(self, tup, buffer):
        subTree = multiMap(tup[-1],buffer=buffer)
        roemNr = ""
        if "oe1" in subTree:
            roemNr = dispatchList(self, subTree["oe1"], buffer)[0]
        elif "oe2" in subTree:
            roemNr = dispatchList(self, subTree["oe2"], buffer)[0]
        else:
            raise Exception("wrong control flow! Veranstaltungskuerzel = " + buffer)
        return orientierungseinheit2FullName(roemNr)

    def praktikum(self, tup, buffer):
        subTree = multiMap(tup[-1],buffer=buffer)

        prakKuerzel = dispatchList(self, subTree['prakKuerzel'], buffer)[0]
        fachKuerzel = prakKuerzel[0:len(prakKuerzel)-1]

        nummer = ""
        if "no" in subTree:
            nummer = dispatchList(self, subTree['no'], buffer)[0]

        gruppe = dispatchList(self, subTree['gruppe'], buffer)[0]

        return praktikum2FullName(fachKuerzel, nummer, gruppe)

    def projekt(self, tup, buffer):
        subTree = multiMap(tup[-1],buffer=buffer)
        gruppe = dispatchList(self, subTree['gruppe'], buffer)[0]
        return projekt2FullName(gruppe)

    def seminar(self, tup, buffer):
        return seminar2FullName()

    def uebung(self, tup, buffer):
        subTree = multiMap(tup[-1],buffer=buffer)

        fachKuerzel = dispatchList(self, subTree['fachKuerzel'], buffer)[0]

        nummer = ""
        if "no" in subTree:
            nummer = dispatchList(self, subTree['no'], buffer)[0]

        gruppe = dispatchList(self, subTree['gruppe'], buffer)[0]

        return uebung2FullName(fachKuerzel, nummer, gruppe)

    def vorlesung(self, tup, buffer):
        subTree = multiMap(tup[-1],buffer=buffer)
        
        fachKuerzel = dispatchList(self, subTree['fachKuerzel'], buffer)[0]

        nummer = ""
        if "nummer" in subTree:
            nummer = dispatchList(self, subTree['nummer'], buffer)[0]

        return vorlesung2FullName(fachKuerzel, nummer)

    def vorkurs(self, tup, buffer):
        subTree = multiMap(tup[-1],buffer=buffer)

        fachKuerzel = dispatchList(self, subTree['fachKuerzel'], buffer)[0]

        nummer = ""
        if "nummer" in subTree:
            nummer = dispatchList(self, subTree['nummer'], buffer)[0]

        return vorkurs2FullName(fachKuerzel, nummer)

    def vorlUebung(self, tup, buffer):
        subTree = multiMap(tup[-1],buffer=buffer)

        fachKuerzel = dispatchList(self, subTree['fachKuerzel'], buffer)[0]

        nummer = ""
        if "nummer" in subTree:
            nummer = dispatchList(self, subTree['nummer'], buffer)[0]

        return vorlUebung2FullName(fachKuerzel, nummer)

    def wahlpflichtmodul(self, tup, buffer):
        subTree = multiMap(tup[-1],buffer=buffer)
        
        alphanumGruppe = dispatchList(self, subTree['alphanumGruppe'], buffer)[0]
        no = dispatchList(self, subTree['no'], buffer)[0]

        return wahlpflichtmodul2FullName(alphanumGruppe, no)

    def wpPraktikum(self, tup, buffer):
        subTree = multiMap(tup[-1],buffer=buffer)
        
        alphanumGruppe = dispatchList(self, subTree['alphanumGruppe'], buffer)[0]
        no = dispatchList(self, subTree['no'], buffer)[0]
        gruppe = dispatchList(self, subTree['gruppe'], buffer)[0]
        
        return wpPraktikum2FullName(alphanumGruppe, no, gruppe)

    def semesterkuerzel(self, tup, buffer):
        return getString(tup, buffer)
    def prakKuerzel(self, tup, buffer):
        return getString(tup, buffer)
    def fachKuerzel(self, tup, buffer):
        return getString(tup, buffer)
    def gwKuerzel(self, tup, buffer):
        return getString(tup, buffer)
    def nummer(self, tup, buffer):
        return getString(tup, buffer)
    def no(self, tup, buffer):
        return getString(tup, buffer)
    def gruppe(self, tup, buffer):
        return str(int(getString(tup, buffer)))
    def alphanumGruppe(self, tup, buffer):
        return getString(tup, buffer)
    def oe1(self, tup, buffer):
        return getString(tup, buffer)
    def oe2(self, tup, buffer):
        return getString(tup, buffer)

from Faecher import faecher

def gwKurs2FullName(gwKuerzel):
    return "GW-Kurs " + gwKuerzel

def orientierungseinheit2FullName(roemNr):
    return "Orientierungseinheit " + roemNr

# helper
def fachOrFachKuerzel(fachKuerzel):
    fach = fachKuerzel
    if fachKuerzel in faecher:
        fach = faecher[fachKuerzel]
    return fach

# helper
def veranstaltung2FullName(veranstaltung, fachKuerzel, nummer="", gruppe=""):
    fach = fachOrFachKuerzel(fachKuerzel)
    result = veranstaltung + " " + fach
    if nummer != "":
        result += " " + nummer
    if gruppe != "":
        result += " (Gruppe " + gruppe + ")"
    return result

def praktikum2FullName(fachKuerzel, nummer, gruppe):
    return veranstaltung2FullName("Praktikum", fachKuerzel, nummer, gruppe)

def projekt2FullName(gruppe):
    return "Projekt (Gruppe" + gruppe + ")"

def seminar2FullName():
    return "Seminar"

def uebung2FullName(fachKuerzel, nummer, gruppe):
    return veranstaltung2FullName("Übung", fachKuerzel, nummer, gruppe)
     
def vorlesung2FullName(fachKuerzel, nummer):
    return veranstaltung2FullName("Vorlesung", fachKuerzel, nummer)
    
def vorkurs2FullName(fachKuerzel, nummer):
    return veranstaltung2FullName("Vorkurs", fachKuerzel, nummer)

def vorlUebung2FullName(fachKuerzel, nummer):
    return veranstaltung2FullName("Vorl./Übung", fachKuerzel, nummer)

def wahlpflichtmodul2FullName(alphanumGruppe, no):
    return "Wahlpflichtmodul " + alphanumGruppe + no

def wpPraktikum2FullName(alphanumGruppe, no, gruppe):
    result = "Praktikum Wahlpflichtmodul " + alphanumGruppe + no
    if gruppe != "":
        result += " (Gruppe " + gruppe + ")"
    return result


def miniTest():
    """unit test in veranstaltungenDispatchProcessorTest.py"""

    success, children, nextcharacter = VeranstaltungParser.parse("BAI1-PR1", processor=VeranstaltungDispatchProcessor())

    from pprint import pprint
    pprint(children)
    print
    pprint((success, children, nextcharacter))

    success, children, nextcharacter = VeranstaltungParser.parse("MINF1-TT1", processor=VeranstaltungDispatchProcessor())

    from pprint import pprint
    pprint(children)
    print
    pprint((success, children, nextcharacter))


if __name__ == "__main__":
    miniTest()

