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

import re
import sys

class CommandGui:
    def __init__(self, controller):
        self.controller = controller
        self.keineAuswahlState = KeineAuswahlState(self)

        self.curState = self.setState(self.keineAuswahlState)

    def setState(self, state):
        self.curState = state
        self.curState.onEntry()

def pd(str):
    """(global) dialog printer;
       prints NOT to stdout, instead to stderr
    """
    print >> sys.stderr, str

class State:
    def __init__(self, fsm):
        self.fsm = fsm

    #common used helper

    def write(self):
        if self.fsm.controller.selectedVeranstaltungen != set([]):
            sum = self.fsm.controller.writeIcalendar()
            pd("\niCalendar with %i events written" % sum)
        else:
            pd("\nno events selected -> no icalendar written")

    def toggleVeranstaltung(self, veranstaltung):
        if veranstaltung in self.fsm.controller.selectedVeranstaltungen:
            self.unselectVeranstaltung(veranstaltung)
        else:
            self.selectVeranstaltung(veranstaltung)

    def unselectVeranstaltung(self, veranstaltung):
        if veranstaltung in self.fsm.controller.selectedVeranstaltungen:
            self.fsm.controller.selectedVeranstaltungen.remove(veranstaltung)

    def selectVeranstaltung(self, veranstaltung):
        if veranstaltung not in self.fsm.controller.selectedVeranstaltungen:
            self.fsm.controller.selectedVeranstaltungen.add(veranstaltung)

    def handleInvalidInput(self):
        pd("invalid input")
        self.fsm.setState(self)

class KeineAuswahlState(State):
    def __init__(self, fsm):
        State.__init__(self, fsm)

        self.groups = sorted(self.fsm.controller.getKeys())

    def onEntry(self):
        self.printLegend()
        self.printGroups()
        self.printGruppenauswahlDialog()

        input = sys.stdin.readline()
        
        if self.couldNavigate(input): pass
        elif self.couldToggleSelection(input): pass
        elif self.couldWriteAndQuit(input): pass
        else:
            self.handleInvalidInput()

    # handle with input and change state

    def couldNavigate(self, input):
        result = False

        m = re.match(r"n([0-9]+)", input)
        if m != None:
            number = int(m.group(1)) -1
            if 0 <= number and number < len(self.groups):
                # navigate
                semestergruppe = self.groups[number]
                self.fsm.setState(VeranstaltungenState(self.fsm, semestergruppe))
                result = True
            else:
                # wrong index number
                self.handleInvalidInput()
                result = True

        return result

    def couldToggleSelection(self, input):
        result = False

        m = re.match("([0-9]+)", input)
        if m != None:
            number = int(m.group(1)) -1
            if 0 <= number and number < len(self.groups):
                semestergruppe = self.groups[number]

                if self.gruppePartialOrFullSelected(semestergruppe):
                    pd("unselect all in " + semestergruppe)
                    for veranstaltung in self.fsm.controller.getVeranstaltungen(semestergruppe):
                        self.unselectVeranstaltung(veranstaltung)
                else:
                    pd("select all in " + semestergruppe)
                    for veranstaltung in self.fsm.controller.getVeranstaltungen(semestergruppe):
                        self.selectVeranstaltung(veranstaltung)

                self.fsm.setState(self)
            else:
                self.handleInvalidInput()

            result = True

        return result

    def couldWriteAndQuit(self, input):
        result = False

        if re.match("wq", input) != None:
            self.write()
            result = True

        return result
                    
    # state specific behavior

    def printGroups(self):
        for i in range(0, len(self.groups)):
            formatter = "{0:>" + str(len(str(len(self.groups)))) + "}"
            lineNumber = formatter.format(i+1)

            semestergruppe = self.groups[i]

            selected = "  "
            if self.gruppeFullSelected(semestergruppe):
                selected = " *"
            elif self.gruppePartialOrFullSelected(semestergruppe):
                selected = " +"

            pd(lineNumber + selected + semestergruppe)

    def printGruppenauswahlDialog(self):
        pd("navigate: n<number>, select/unselect all: <number>, write&quit: wq")

    def printLegend(self):
        pd("\nlegend: * all selected, + partial selected, ' ' unselected")

    # helper

    def gruppeFullSelected(self, semestergruppe):
        return (self.fsm.controller.selectedVeranstaltungen &
                  set(self.fsm.controller.getVeranstaltungen(semestergruppe)) == 
                set(self.fsm.controller.getVeranstaltungen(semestergruppe)))

    def gruppePartialOrFullSelected(self, semestergruppe):
        return (self.fsm.controller.selectedVeranstaltungen &
                 set(self.fsm.controller.getVeranstaltungen(semestergruppe)) != set([]))

class VeranstaltungenState(State):
    def __init__(self, fsm, semestergruppe):
       State.__init__(self, fsm)

       self.semestergruppe = semestergruppe
       self.veranstaltungen = sorted(self.fsm.controller.getVeranstaltungen(semestergruppe))

    def onEntry(self):
        self.printLegend()
        self.printVeranstaltungen()
        self.printVeranstaltungenAuswahlDialog()

        result = sys.stdin.readline()
        
        #navigate
        m = re.match(r"(b).*", result)
        if m != None:
            self.fsm.setState(self.fsm.keineAuswahlState)
        else:
            # toggle selection
            m = re.match("([0-9]+)", result)
            if m != None:
                number = int(m.group(1)) -1
                if 0 <= number and number < len(self.veranstaltungen):
                    pd("toggle selection")
                    pd(self.veranstaltungen[number])
                    self.toggleVeranstaltung(self.veranstaltungen[number])
                    self.fsm.setState(self)
                else:
                    # wrong input
                    pd("invalid input")
                    self.fsm.setState(self)
            # write and quit
            elif re.match("wq", result) != None:
                self.write()
            else:
                pd("invalid input")
                self.fsm.setState(self)

    # state specific behavior

    def printVeranstaltungen(self):
        maxLen = len(reduce(lambda x,y: max(x,y, key=len), self.veranstaltungen))

        for i in range(0, len(self.veranstaltungen)):
            veranstaltung = self.veranstaltungen[i]

            formatter = "{0:>" + str(len(str(len(self.veranstaltungen)))) + "}"
            lineNumber = formatter.format(i+1)

            selected = "  "
            if self.veranstaltungSelected(veranstaltung):
                selected = " *"

            fullName = self.fsm.controller.tryGetFullName(veranstaltung)

            formatter = "{0:<" + str(maxLen+2) + "}"
            leftAlignedVeranstaltung = formatter.format(veranstaltung)
            #FIXME: dirty hack (a 'Ü' is represented in utf-8 by 2 byte)
            if 'Ü' in leftAlignedVeranstaltung:
                leftAlignedVeranstaltung += " "

            pd(lineNumber + selected + leftAlignedVeranstaltung + fullName)

    def printVeranstaltungenAuswahlDialog(self):
        pd("back: b, toggle selection: <number>, write&quit: wq")

    def printLegend(self):
        pd("\nlegend: * selected, ' ' unselected")

    # helper

    def veranstaltungSelected(self, veranstaltung):
        return (self.fsm.controller.selectedVeranstaltungen &
                 set([veranstaltung]) != set([]))

