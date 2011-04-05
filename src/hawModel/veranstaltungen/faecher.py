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

infFaecher = {
    "AA"  : "Analysis und Lineare Algebra",
    "AD"  : "Algorithmen und Datenstrukturen",
    "AF"  : "Automatentheorie und Formale Sprachen",
    "AI"  : "Architektur von Informationssystemen",
    "AW"  : "Anwendungen",
    "BS"  : "Betriebssysteme",
    "BW"  : "Betriebswirtschaftslehre",
    "CE"  : "Computer Engineering",
    "CI"  : "Compiler und Interpreter",
    "DB"  : "Datenbanken",
    "DT"  : "Digitaltechnik",
    "GE"  : "Grundlagen Elektrotechnik",
    "GI"  : "Grundlagen der Informatik",
    "GS"  : "Grundlagen Systemnahes Programmieren",
    "GT"  : "Grundlagen Technische Informatik",
    "GKA" : "Graphentheoretische Konzepte und Algorithmen",
    "IS"  : "Intelligente Systeme",
    "LB"  : "Logik und Berechenbarkeit",
    "MA"  : "Mathematik",
    "MG"  : "Mathematische Grundlagen",
    "MI"  : "Modellierung von Informationssystemen",
    "MT"  : "Modellierung Technischer Systeme",
    "NS"  : "Numerik und Stochastik",
    "PJ"  : "Projekt",
    "PL"  : "Prozesslenkung",
    "PR"  : "Programmieren",
    "PRG" : "Grundlagen Programmieren",
    "RMP" : "Rechnerstrukturen und Maschinennahe Programmierung",
    "RN"  : "Rechnernetze",
    "RS"  : "Rechnerstrukturen",
    "SE"  : "Software Engineering",
    "SP"  : "Sprachen",
    "SY"  : "System- und Echtzeitprogrammierung",
    "TH"  : "Theoretische Informatik",
    "TSE" : "Team Studien Einstieg",
    "TT"  : "Technik und Technologie",
    "UO"  : "Unternehmensorientierung",
    "VS"  : "Verteilte Systeme",
    "WP"  : "Wahlpflichtmodul"
}

etechFaecher = {
    "AL"  : "Algebra",
    "AN"  : "Analysis",
    "AR"  : "Angewandte Regelungstechnik",
    "AS"  : "Antriebstechnik Mobiler Systeme",
    "ASS" : "Seminar Autonome Systeme",
    "AÜ"  : "Analoge Übertragungstechnik",
    "BA"  : "Bachelorreport",
    "BK"  : "Kolloquium",
    "BM"  : "Bildverarbeitung und Mustererkennung",
    "BS"  : "Betriebssysteme",
    "BU"  : "Bussysteme und Sensorik",
    "BW"  : "Projektmanagement",
    "CA"  : "Calculus",
    "CO"  : "Codierung",
    "CR"  : "Communication and Presentation",
    "CT"  : "Computertechnik",
    "DB"  : "Datenbanken",
    "DE"  : "Dezentrale Energieversorgung",
    "DI"  : "Digitaltechnik",
    #clash: "DI" : "Digital Circuits",
    "DN"  : "Dynamische Systeme",
    "DS"  : "Digitale Hardwaresysteme",
    "DÜ"  : "Digitale Übertragungstechnik",
    "DV"  : "Digitale Signalverarbeitung",
    "DY"  : "Digitale Systeme",
    "EB"  : "Echtzeitbetriebssysteme",
    "EE"  : "Introduction Electrical Engineering",
    "EL"  : "Elektronik",
    "EN"  : "Energietechnik",
    "EP"  : "Betriebssysteme und Echtzeitprogrammierung",
    "ES"  : "Embedded Systems",
    "ET"  : "Grundlagen Elektrotechnik",
    #clash: "ET" : "Electronics",
    "FT"  : "Funktechnik",
    "GE"  : "Grundlagen Energietechnik",
    #clash: "GE" : "German",
    "GN"  : "Grundlagen Nachrichtentechnik",
    "GR"  : "Grundlagen Regelungstechnik",
    "IT"  : "Informationstheorie",
    "KN"  : "Kommunikationsnetze",
    "LE"  : "Antriebe und Leistungselektronik",
    "LS"  : "Lern- und Studiermethodik",
    #clash: "LS"  : "Learning and Study Methods",
    "MC"  : "Mikrocontrollertechnik",
    "MF"  : "Mobilfunk",
    "MS"  : "Methodisches Systemdesign",
    "MT"  : "Mikrotechnologie",
    "NS"  : "Numerik und Stochastik",
    "NV"  : "Numerische Verfahren",
    "OP"  : "Objektorientierte Programmierung",
    "PA"  : "Prozessautomatisierung",
    "PB"  : "Prozessleittechnik und Bussysteme",
    "PH"  : "Physik",
    "PO"  : "Wahlpflichtprojekt",
    "PR"  : "Programmieren",
    "PS"  : "Projektmanagement und Systemengineering",
    "RE"  : "Regenerative Energietechnik",
    "RY"  : "Reglersynthese",
    "SE"  : "Software Engineering",
    "SO"  : "Stochastik dynamischer Systeme",
    #clash: "SO" : "Software Construction",
    "SP"  : "Digitale Signalverarbeitung auf Signalprozessoren",
    "SS"  : "Signal- und Systemtheorie",
    #clash: "SS" : "Entwurf schneller Schaltungen",
    "ST"  : "Steuerungstechnik",
    "SV"  : "Signalverarbeitung",
    "TE"  : "Technisches Englisch",
    #clash: "TE"  : "Technical Englisch",
    "TI"  : "Theoretische Informatik",
    "TK"  : "Telekommunikation",
    "VD"  : "Besondere Verfahren Digitaler Signalverarbeitung",
    "VP"  : "Verbundprojekt Autonome Systeme",
    "WA"  : "Wissenschaftliches Arbeiten",
    "WP"  : "Wahlpflichtmodul",
    "ZR"  : "Zustandsregelung"
}

faecher = dict(etechFaecher, **infFaecher) # when keys overlapping: inf overwrites etech

