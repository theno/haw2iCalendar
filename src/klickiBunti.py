#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
import os
import os.path
import sys
import threading
import urllib
import webbrowser

import wx
from wx import xrc

from controller import Controller
from hawModel.hawCalendar import DOZENT, SEMESTERGRUPPE, GRUPPENKUERZEL

def iterChildren(treeCtrl, itemId):
    curId, curItem = treeCtrl.GetFirstChild(itemId)
    while curId.IsOk(): 
        yield curId
        curId, curItem = treeCtrl.GetNextChild(itemId, curItem)

class ScrollableDialog(wx.Dialog):
    def __init__(self, parent, text, title):
        wx.Dialog.__init__(self, parent, title=title)
       
        textCtrl = wx.TextCtrl(self, -1, text, size=(810,400), style=wx.TE_MULTILINE | wx.TE_READONLY)
        font = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Courier New')
        textCtrl.SetFont(font)
        textCtrl.SetInsertionPoint(0)
       
        sizer = wx.BoxSizer(wx.VERTICAL)
       
        btnsizer = wx.BoxSizer()

        btn = wx.Button(self, wx.ID_OK)
        btnsizer.Add(btn, 0, wx.ALL, 5)
        btnsizer.Add((5,-1), 0, wx.ALL, 5)

        sizer.Add(textCtrl, 0, wx.EXPAND|wx.ALL, 5)   
        sizer.Add(btnsizer, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)   
        self.SetSizerAndFit(sizer)

EVT_BATCH_ID = wx.NewId()

def EVT_BATCH(win, func):
    win.Connect(-1, -1, EVT_BATCH_ID, func)

class BatchEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_BATCH_ID)
        self.data = data

EVT_BATCH_FINISHED_ID = wx.NewId()

def EVT_BATCH_FINISHED(win, func):
    win.Connect(-1, -1, EVT_BATCH_FINISHED_ID, func)

class BatchFinishedEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_BATCH_FINISHED_ID)
        self.data = data

class BatchExportWorkerThread(threading.Thread):
    def __init__(self, notifyWindow, ctrl, path):
        threading.Thread.__init__(self)

        self.notifyWindow = notifyWindow
        self.ctrl = ctrl
        self.path = path

        self.wantAbort = False

        self.start()

    def run(self):

        def writeIcals(subfolder):
            for key in sorted(self.ctrl.getKeys()):

                self.ctrl.selectedVeranstaltungen = set()
                veranstaltungen = self.ctrl.getVeranstaltungen(key)
                self.ctrl.selectVeranstaltungen(veranstaltungen)

                fileName = key.replace('/','_').replace('[','(').replace(']',')').replace('ß','_et_') + ".ics"
                if fileName==".ics": fileName = "aaa_noName.ics"

                try: os.mkdir(subfolder)
                except OSError as e: pass

                self.ctrl.setOutfile(subfolder + fileName)
                sumEvents = self.ctrl.writeIcalendar()

                text = key + ": iCalendar '" + fileName + "' created (" + str(sumEvents) + " Events)\n"
                
                #TODO: this is sooo dirty (well, I don't like wxpython)
                try:
                    wx.PostEvent(self.notifyWindow, BatchEvent(text))
                except TypeError as e:
                    return True
                #if (self.wantAbort): return True

            return False

# TODO: does file separator "/" also work on windows?
        self.ctrl.tupleKeyIndex = self.ctrl.optimalGruppenKeyIndex()
        subfolder = self.path + "/" + "Studentensicht" + "/"
#        subfolder = os.path.join(path, "Studentensicht")
        wantAbort = writeIcals(subfolder)

        if wantAbort:
            return
        
        self.ctrl.tupleKeyIndex = DOZENT
        subfolder = self.path + "/" + "Dozentensicht" + "/"
#        subfolder = os.path.join(path, "Dozentensicht")
        writeIcals(subfolder)

        wx.PostEvent(self.notifyWindow, BatchFinishedEvent(None))

    def abort(self):
        self.wantAbort = True
       
class RunningBatchExportDialog(wx.Dialog):
    def __init__(self, parent, text, title, ctrl, path):
        wx.Dialog.__init__(self, parent, title=title)
        
        EVT_BATCH(self, self.onResult)
        EVT_BATCH_FINISHED(self, self.onBatchFinished)
        workerThread = BatchExportWorkerThread(self, ctrl, path)
       
        self.textCtrl = wx.TextCtrl(self, -1, text, size=(810,400), style=wx.TE_MULTILINE | wx.TE_READONLY)
        font = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Courier New')
        self.textCtrl.SetFont(font)
        self.textCtrl.SetInsertionPoint(0)
       
        sizer = wx.BoxSizer(wx.VERTICAL)

        btnsizer = wx.BoxSizer()

        self.btnCancel = wx.Button(self, wx.ID_CANCEL)
        btnsizer.Add(self.btnCancel, 0, wx.ALL, 5)

        self.btnOk = wx.Button(self, wx.ID_OK)
        self.btnOk.Disable()
        btnsizer.Add(self.btnOk, 0, wx.ALL, 5)

        btnsizer.Add((5,-1), 0, wx.ALL, 5)

        sizer.Add(self.textCtrl, 0, wx.EXPAND|wx.ALL, 5)   
        sizer.Add(btnsizer, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)   
        self.SetSizerAndFit(sizer)

    def onResult(self, batchEvent):
        text = batchEvent.data
        self.textCtrl.AppendText(text)

    def onBatchFinished(self, event):
        self.btnOk.Enable()
        self.btnCancel.Disable()

class KlickiBunti(wx.App):
    def OnInit(self):

        self.res = xrc.XmlResource('klickiBunti.xrc')
        self.frame = self.res.LoadFrame(parent=None, name='frame')

        self.initFrame()
        self.initMenu()

        self.frame.SetSize(wx.Size(900,800))
        self.frame.Show()

        return True

    def initFrame(self):
        self.button_Load = xrc.XRCCTRL(self.frame, 'button_Load')
        self.button_Load.Bind(wx.EVT_BUTTON, self.onButton_Load)

        self.button_Export = xrc.XRCCTRL(self.frame, 'button_Export')
        self.button_Export.Bind(wx.EVT_BUTTON, self.onButton_Export)
        self.button_Export.Disable()

        self.infoString = xrc.XRCCTRL(self.frame, 'staticText_infoString')
        self.space = "      "

        self.treeCtrl_Stud = xrc.XRCCTRL(self.frame, 'tree_Stud')
        self.treeCtrl_Stud.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.onDoubleClick_Stud)

        self.treeCtrl_Doz = xrc.XRCCTRL(self.frame, 'tree_Doz')
        self.treeCtrl_Doz.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.onDoubleClick_Doz)

    def initMenu(self):
        self.menuBar = self.res.LoadMenuBar('menubar')
        self.frame.SetMenuBar(self.menuBar)

        self.frame.Bind(wx.EVT_MENU, self.onMenuItem_BatchStudUndDoz, id=xrc.XRCID("menuItem_BatchExport"))
        self.menuItem_AlleSemUndDoz = self.menuBar.FindItemById(xrc.XRCID("menuItem_BatchExport"))
        self.menuItem_AlleSemUndDoz.Enable(False)

        self.frame.Bind(wx.EVT_MENU, self.onMenuItem_EuI, id=xrc.XRCID("menuItem_EuI"))
        self.frame.Bind(wx.EVT_MENU, self.onMenuItem_EuI_load, id=xrc.XRCID("menuItem_EuI_load"))
        self.frame.Bind(wx.EVT_MENU, self.onMenuItem_Inf, id=xrc.XRCID("menuItem_Inf"))
        self.frame.Bind(wx.EVT_MENU, self.onMenuItem_Inf_load, id=xrc.XRCID("menuItem_Inf_load"))
        self.frame.Bind(wx.EVT_MENU, self.onMenuItem_GoogleCalendar, id=xrc.XRCID("menuItem_GoogleCalendar"))
        self.frame.Bind(wx.EVT_MENU, self.onMenuItem_rfc5545, id=xrc.XRCID("menuItem_rfc5545"))

        self.frame.Bind(wx.EVT_MENU, self.onMenuItem_Anleitung, id=xrc.XRCID("menuItem_Anleitung"))
        self.frame.Bind(wx.EVT_MENU, self.onMenuItem_GPL, id=xrc.XRCID("menuItem_GPL"))
        self.frame.Bind(wx.EVT_MENU, self.onMenuItem_About, id=xrc.XRCID("menuItem_About"))

    def onButton_Load(self, event):
        dlg = wx.FileDialog(self.frame, "txt-Version des Semesterplans auswählen")
        dlg.SetWildcard("nur Textdateien (*.txt)|*.txt|alle Dateien|*")

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.ctrl = Controller(inFileName=path, outFileName=None)
            self.infoString.SetLabel(self.space + self.ctrl.getInfoString())

            self.fillTrees()

        dlg.Destroy()

        self.updateExportButton()
        self.menuItem_AlleSemUndDoz.Enable()

    def fillTrees(self):

        def fillTree(treeCtrl):
            font = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Courier New')
            treeCtrl.SetFont(font)

            groups = sorted(self.ctrl.getKeys())
            treeCtrl.DeleteAllItems()
            root = treeCtrl.AddRoot('root')
            for key in groups:
                parent = treeCtrl.AppendItem(root, key)
                veranstaltungen = sorted(self.ctrl.getVeranstaltungen(key))

                maxLen = len(reduce(lambda x,y: max(x,y, key=len), veranstaltungen))
                formatter = "{0:<" + str(maxLen+3) + "}"

                for veranstaltung in veranstaltungen:
                    leftAlignedVeranstaltung = formatter.format(veranstaltung)
                    #FIXME: dirty hack (a 'Ü' is represented in utf-8 by 2 byte)
                    if 'Ü' in leftAlignedVeranstaltung:
                        leftAlignedVeranstaltung += " "
                    s = leftAlignedVeranstaltung + self.ctrl.tryGetFullName(veranstaltung)
                    treeCtrl.AppendItem(parent, s)

        self.ctrl.tupleKeyIndex = DOZENT
        fillTree(self.treeCtrl_Doz)

        self.ctrl.tupleKeyIndex = self.ctrl.optimalGruppenKeyIndex()
        fillTree(self.treeCtrl_Stud)

    def onButton_Export(self, event):
        style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        dlg = wx.FileDialog(self.frame, message="iCalendar (.ics) speichern unter", style=style)
        dlg.SetWildcard("iCalendar-Dateien (*.ics)|*.ics")

        if dlg.ShowModal() == wx.ID_OK:

            path = dlg.GetPath()
            if not path.endswith(".ics"):
                path = path + ".ics"

            self.ctrl.setOutFileName(path)
            self.ctrl.writeIcalendar()

        dlg.Destroy()

    def onDoubleClick_Stud(self, wxTreeEvent):
        self.ctrl.tupleKeyIndex = self.ctrl.optimalGruppenKeyIndex()
        self.onDoubleClick(wxTreeEvent, self.treeCtrl_Stud)

    def onDoubleClick_Doz(self, wxTreeEvent):
        self.ctrl.tupleKeyIndex = DOZENT
        self.onDoubleClick(wxTreeEvent, self.treeCtrl_Doz)
        
    def onDoubleClick(self, wxTreeEvent, treeCtrl):
        itemId = wxTreeEvent.GetItem()

        text_unicode = treeCtrl.GetItemText(itemId)
        text_utf8 = text_unicode.encode("utf-8")

        parentId = treeCtrl.GetItemParent(itemId)
        parent_text = treeCtrl.GetItemText(parentId)

        isVeranstaltung = not (parent_text == "root")

        if not isVeranstaltung:
            keyItemId = itemId
            key = text_utf8
            veranstaltungen = self.ctrl.getVeranstaltungen(key)
            if self.groupFullSelected(key):
                self.ctrl.unselectVeranstaltungen(veranstaltungen)
            else:
                self.ctrl.selectVeranstaltungen(veranstaltungen)
        else:
            veranstaltung = text_utf8.split("   ")[0] #FIXME: dirty
            if veranstaltung in self.ctrl.selectedVeranstaltungen:
                    self.ctrl.selectedVeranstaltungen.remove(veranstaltung)
            else: 
                self.ctrl.selectedVeranstaltungen.add(veranstaltung)

        self.updateTrees()
        self.updateExportButton()

    def updateTrees(self):
        def updateTree(treeCtrl):
            for keyItemId in iterChildren(treeCtrl, treeCtrl.GetRootItem()):

                allSelected = True
                for veranstItemId in iterChildren(treeCtrl, keyItemId):

                    text_unicode = treeCtrl.GetItemText(veranstItemId)
                    veranstaltung = text_unicode.encode("utf-8").split("   ")[0] #FIXME: dirty

                    if not veranstaltung in self.ctrl.selectedVeranstaltungen:
                        treeCtrl.SetItemBold(veranstItemId, False)
                        allSelected = False
                    else:
                        treeCtrl.SetItemBold(veranstItemId)

                treeCtrl.SetItemBold(keyItemId, allSelected)

            treeCtrl.Refresh()

        updateTree(self.treeCtrl_Stud)
        updateTree(self.treeCtrl_Doz)

    def updateExportButton(self):
        if len(self.ctrl.selectedVeranstaltungen) > 0:
            self.button_Export.Enable()
        else:
            self.button_Export.Disable()

    def groupFullSelected(self, key):
        return (self.ctrl.selectedVeranstaltungen &
                  set(self.ctrl.getVeranstaltungen(key)) ==
                set(self.ctrl.getVeranstaltungen(key)))

    def onMenuItem_BatchStudUndDoz(self, event):

        dlg = wx.DirDialog(self.frame, "Verzeichnis für Batch-Export auswählen")

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            dlg.Destroy()

            batchCtrl = copy.deepcopy(self.ctrl)

            dlg = RunningBatchExportDialog(parent=self.frame,
                                           text="Batch-Export gestartet:\n\n",
                                           title="Batch-Export",
                                           ctrl=batchCtrl,
                                           path=path)
            dlg.ShowModal() 
            dlg.Destroy()

    def onMenuItem_EuI(self, event):
        webbrowser.open("http://www.etech.haw-hamburg.de/Stundenplan/", autoraise=True)

    def onMenuItem_EuI_load(self, event):
        try:
            sys.stdin = urllib.urlopen("http://www.etech.haw-hamburg.de/Stundenplan/Sem_IuE.txt")
            self.ctrl = Controller(inFileName=None, outFileName=None)
            self.infoString.SetLabel(self.space + self.ctrl.getInfoString())
            self.fillTrees()

            self.updateExportButton()

            self.menuItem_AlleSemUndDoz.Enable()

        except IOError as e:
            print "Could not open EuI-url: " + str(e)

    def onMenuItem_Inf(self, event):
        webbrowser.open("http://www.informatik.haw-hamburg.de/veranstaltungsplaene.html", autoraise=True)

    def onMenuItem_Inf_load(self, event):
        try:
            sys.stdin = urllib.urlopen("http://www.informatik.haw-hamburg.de/fileadmin/Homepages/ProfPadberg/stundenplaene/Sem_I.txt")
            self.ctrl = Controller(inFileName=None, outFileName=None)
            self.infoString.SetLabel(self.space + self.ctrl.getInfoString())
            self.fillTrees()

            self.updateExportButton()

            self.menuItem_AlleSemUndDoz.Enable()

        except IOError as e:
            print "Couldn't open Inf-url: " + str(e)

    def onMenuItem_GoogleCalendar(self, event):
        webbrowser.open("http://www.google.com/calendar", autoraise=True)

    def onMenuItem_rfc5545(self, event):
        webbrowser.open("http://tools.ietf.org/html/rfc5545/", autoraise=True)

    def onMenuItem_Anleitung(self, event):

        file = open("Anleitung", "r")
        text = file.read()
        file.close()

        dlg = ScrollableDialog(None, text, title="Anleitung")
        dlg.ShowModal()
        dlg.Destroy()

    def onMenuItem_GPL(self, event):

        file = open("COPYING", "r")
        text = file.read()
        file.close()

        text = " " + text.replace("\n", "\n ")

        dlg = ScrollableDialog(self.frame, text, title="GPL")
        dlg.ShowModal()
        dlg.Destroy()

    def onMenuItem_About(self, event):

        file = open("About", "r")
        text = file.read()
        file.close()

        dlg = wx.MessageDialog(self.frame, text, caption="About", style=wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

if __name__ == '__main__':
    app = KlickiBunti()
    app.MainLoop()

