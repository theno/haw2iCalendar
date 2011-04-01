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

from simpleparse import dispatchprocessor
from simpleparse.dispatchprocessor import dispatch, dispatchList, getString, multiMap

from veranstaltungenParser import VeranstaltungParser

class VeranstaltungDispatchProcessor( dispatchprocessor.DispatchProcessor ):
    def veranstaltung(self, tup, buffer):
        subTree = multiMap(tup[-1], buffer=buffer)

        def get(veranstaltung):
            return dispatchList(self, subTree[veranstaltung], buffer)[0]

        if "awSeminar" in subTree:
            result = get("awSeminar")
        elif "gwKurs" in subTree:
            result = get("gwKurs")
        elif "orientierungseinheit" in subTree:
            result = get("orientierungseinheit")
        elif "praktikum" in subTree:
            result = get("praktikum")
        elif "projekt" in subTree:
            result = get("projekt")
        elif "seminar" in subTree:
            result = get("seminar")
        elif "teamStudienEinstieg" in subTree:
            result = get("teamStudienEinstieg")
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

        gruppe = ""
        if "gruppe" in subTree:
            gruppe = dispatchList(self, subTree['gruppe'], buffer)[0]

        nummer = ""
        if "nummer" in subTree:
            nummer = dispatchList(self, subTree['nummer'], buffer)[0]

        return veranstaltung2FullName("PJ", nummer=nummer, gruppe=gruppe)

    def seminar(self, tup, buffer):
        return seminar2FullName()

    def awSeminar(self, tup, buffer):
        subTree = multiMap(tup[-1],buffer=buffer)

        fachKuerzel = "AW"

        if "nummer" in subTree:
            nummer = dispatchList(self, subTree['nummer'], buffer)[0]
            return seminar2FullName(fachKuerzel, nummer)

        return seminar2FullName(fachKuerzel)

    def teamStudienEinstieg(self, tup, buffer):
        subTree = multiMap(tup[-1],buffer=buffer)

        gruppe = dispatchList(self, subTree['gruppe'], buffer)[0]

        return veranstaltung2FullName("TSE", gruppe=gruppe)

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


def gwKurs2FullName(gwKuerzel):
    return "GW-Kurs " + gwKuerzel

def orientierungseinheit2FullName(roemNr):
    return "Orientierungseinheit " + roemNr

# helper
def fachOrFachKuerzel(fachKuerzel):
    fach = fachKuerzel

    from faecher import faecher
    if fachKuerzel in faecher:
        fach = faecher[fachKuerzel]

    return fach

# helper
def veranstaltung2FullName(fachKuerzel, veranstaltung="", nummer="", gruppe=""):
    fach = fachOrFachKuerzel(fachKuerzel)
    result = fach

    if veranstaltung != "":
        result = veranstaltung + " " + result
    if nummer != "":
        result += " " + nummer
    if gruppe != "":
        result += " (Gruppe " + gruppe + ")"

    return result

def praktikum2FullName(fachKuerzel, nummer, gruppe):
    return veranstaltung2FullName(fachKuerzel, "Praktikum", nummer, gruppe)

def seminar2FullName(fachKuerzel="", nummer=""):
    return veranstaltung2FullName(fachKuerzel, "Seminar", nummer)

def uebung2FullName(fachKuerzel, nummer, gruppe):
    return veranstaltung2FullName(fachKuerzel, "Übung", nummer, gruppe)
     
def vorlesung2FullName(fachKuerzel, nummer):
    return veranstaltung2FullName(fachKuerzel, "Vorlesung", nummer)
    
def vorkurs2FullName(fachKuerzel, nummer):
    return veranstaltung2FullName(fachKuerzel, "Vorkurs", nummer)

def vorlUebung2FullName(fachKuerzel, nummer):
    return veranstaltung2FullName(fachKuerzel, "Vorl./Übung", nummer)

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

