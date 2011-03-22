# -*- coding: utf-8 -*-
import re
import sys

import controller

def pd(str):
    """(global) Dialog printer;
       prints NOT to stdout, instead to stderr
    """
    print >> sys.stderr, str

class CommandGui:
    def __init__(self, controller):
	self.controller = controller
        self.keineAuswahlState = KeineAuswahlState(self)

	self.curState = self.setState(self.keineAuswahlState)

    def setState(self, state):
        self.curState = state
	self.curState.onEntry()

class State:
    def __init__(self, fsm):
        self.fsm = fsm

    #common used helper

    def write(self):
	if self.fsm.controller.selectedVeranstaltungen != set([]):
	    self.fsm.controller.writeIcalendar()
	    pd("Icalendar written")
	else:
	    pd("no events selected -> no icalendar written")

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

class KeineAuswahlState(State):
    def __init__(self, fsm):
        State.__init__(self, fsm)

        self.semestergruppen = sorted(self.fsm.controller.getSemestergruppen())

    def onEntry(self):
	self.printLegend()
        self.printSemestergruppen()
	self.printGruppenauswahlDialog()

	result = sys.stdin.readline()
        
	#navigate
	m = re.match(r"n([0-9]+)", result)
	if m != None:
	    number = int(m.group(1))
	    pd(str(number))
	    semestergruppe = self.semestergruppen[number]

	    self.fsm.setState(VeranstaltungenState(self.fsm, semestergruppe))

	else:
	    # toggle selection
	    m = re.match("([0-9]+)", result)
	    if m != None:
	        number = int(m.group(1))
	        semestergruppe = self.semestergruppen[number]

		if self.gruppePartialOrFullSelected(semestergruppe):
	            pd("unselect all in " + semestergruppe)
		    for veranstaltung in self.fsm.controller.getVeranstaltungen(semestergruppe):
		        self.unselectVeranstaltung(veranstaltung)
		else:
	            pd("select all in " + semestergruppe)
		    for veranstaltung in self.fsm.controller.getVeranstaltungen(semestergruppe):
		        self.selectVeranstaltung(veranstaltung)
		self.fsm.setState(self)
	    # write and quit
	    elif re.match("wq", result) != None:
		self.write()
	    else:
	        pd("invalid input")
	        self.fsm.setState(self)

    # state specific behavior

    def printSemestergruppen(self):
        for i in range(0, len(self.semestergruppen)):
	    semestergruppe = self.semestergruppen[i]
	    selected = "  "
	    if self.gruppeFullSelected(semestergruppe):
	        selected = " *"
	    elif self.gruppePartialOrFullSelected(semestergruppe):
	        selected = " +"
    	    pd("%.2d" % i + selected + semestergruppe)

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
	        number = int(m.group(1))
	        pd("toggle selection")
		pd(self.veranstaltungen[number])
		self.toggleVeranstaltung(self.veranstaltungen[number])
		self.fsm.setState(self)
	    # write and quit
	    elif re.match("wq", result) != None:
		self.write()
	    else:
	        pd("invalid input")
	        self.fsm.setState(self)

    # state specific behavior

    def printVeranstaltungen(self):
        for i in range(0, len(self.veranstaltungen)):
	    selected = "  "
	    if self.veranstaltungSelected(self.veranstaltungen[i]):
	        selected = " *"
    	    pd("%.2d" % i + selected + self.veranstaltungen[i])

    def printVeranstaltungenAuswahlDialog(self):
        pd("back: b, toggle selection: <number>, write&quit: wq")

    def printLegend(self):
        pd("\nlegend: * selected, ' ' unselected")

    # helper

    def veranstaltungSelected(self, veranstaltung):
	return (self.fsm.controller.selectedVeranstaltungen &
	         set([veranstaltung]) != set([]))

