import wx
import datetime
import time
import threading
import random
import os
import subprocess as sp
import wx.lib.plot as plot


class SettingFrame(wx.Frame):
    def __init__(self, parent):
        super(SettingFrame, self).__init__(parent, title="Settings", size=(480, 560))
        self.font = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.panel = wx.Panel(self)
        self.panel.SetFont(self.font)

        self.data = {}
        with open("tmp.prop", "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.find("=") != -1:
                    tmp = line.strip().split("=")
                    self.data[tmp[0]] = tmp[1]

        self.labelAddr = wx.StaticText(self.panel, label="Database Address", pos=(40, 40), size=(380, 40))
        self.textAddr = wx.TextCtrl(self.panel, value=self.data["conn"], pos=(40, 80), size=(380, 40))
        self.labelUser = wx.StaticText(self.panel, label="User", pos=(40, 120), size=(180, 40))
        self.labelPass = wx.StaticText(self.panel, label="Password", pos=(240, 120), size=(180, 40))
        self.textUser = wx.TextCtrl(self.panel, value=self.data["user"], pos=(40, 160), size=(180, 40))
        self.textPass = wx.TextCtrl(self.panel, value=self.data["password"], pos=(240, 160), size=(180, 40))
        self.labelHouse = wx.StaticText(self.panel, label="WareHouse", pos=(40, 200), size=(180, 40))
        self.labelWorker = wx.StaticText(self.panel, label="LoadWorker", pos=(240, 200), size=(180, 40))
        self.textHouse = wx.TextCtrl(self.panel, value=self.data["warehouses"], pos=(40, 240), size=(180, 40))
        self.textWorker = wx.TextCtrl(self.panel, value="loadWorkers", pos=(240, 240), size=(180, 40))
        self.labelTerminal = wx.StaticText(self.panel, label="Terminal", pos=(40, 280), size=(180, 40))
        self.labelTime = wx.StaticText(self.panel, label="RunTime", pos=(240, 280), size=(180, 40))
        self.textTerminal = wx.TextCtrl(self.panel, value=self.data["terminals"], pos=(40, 320), size=(180, 40))
        self.textTime = wx.TextCtrl(self.panel, value=self.data["runMins"], pos=(240, 320), size=(180, 40))
        self.butSave = wx.Button(self.panel, label="Save", pos=(100, 420), size=(120, 40))
        self.butCancel = wx.Button(self.panel, label="Cancel", pos=(240, 420), size=(120, 40))
        self.Bind(wx.EVT_BUTTON, self.actSave, self.butSave)
        self.Bind(wx.EVT_BUTTON, self.actCancel, self.butCancel)

    def actSave(self, event):
        self.data["conn"] = self.textAddr.GetValue()
        self.data["user"] = self.textUser.GetValue()
        self.data["password"] = self.textPass.GetValue()
        self.data["warehouses"] = self.textHouse.GetValue()
        self.data["loadWorkers"] = self.textWorker.GetValue()
        self.data["terminals"] = self.textTerminal.GetValue()
        self.data["runMins"] = self.textTime.GetValue()

        with open("tmp.prop", "w") as f:
            f.writelines([k + "=" + v + "\n" for k, v in self.data.items()])

        self.Destroy()

    def actCancel(self, event):
        self.Destroy()


class MainFrame(wx.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(MainFrame, self).__init__(parent, *args, **kwargs)
        self.font = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.panel = wx.Panel(self)
        self.panel.SetFont(self.font)

        os.chdir("../run")

        self.plotter = plot.PlotCanvas(self.panel)
        self.plotter.SetPosition(pt=(20, 20))
        self.plotter.SetInitialSize(size=(450, 300))
        self.plotter.SetBackgroundColour("white")

        self.textLog = wx.TextCtrl(self.panel, pos=(480, 20), size=(450, 440), style=wx.TE_MULTILINE)
        self.butSet = wx.Button(self.panel, label="Set", pos=(40, 420), size=(120, 40))
        self.butLoad = wx.Button(self.panel, label="Load", pos=(180, 420), size=(120, 40))
        self.butRun = wx.Button(self.panel, label="Run", pos=(320, 420), size=(120, 40))

        self.Bind(wx.EVT_BUTTON, self.actSet, self.butSet)
        self.Bind(wx.EVT_BUTTON, self.actLoad, self.butLoad)
        self.Bind(wx.EVT_BUTTON, self.actRun, self.butRun)

        self.TIMESTACK = 200
        self.queVal = [0 for i in range(self.TIMESTACK)]

    def addValue(self, val):
        self.queVal.append(val)
        del self.queVal[0]
#        print(" ".join([str(i) for i in self.queVal]))
        data = [[i + 1 - self.TIMESTACK, self.queVal[i]] for i in range(self.TIMESTACK)]
        line = plot.PolyLine(data, colour='red', width=2)
        gc = plot.PlotGraphics([line], 'Performance', 'Time', 'Tpm-C')
        self.plotter.Draw(gc)

    def setLock(self, flag):
        self.butSet.Enable(flag)
        self.butRun.Enable(flag)
        self.butLoad.Enable(flag)

    def actSet(self, event):
        settingFrame = SettingFrame(self)
        settingFrame.Show(True)
        self.textLog.SetValue("set")

    def actLoad(self, event):
        self.textLog.SetValue("load")

    def actRun(self, event):
        self.setLock(False)

        cmd = "./runBenchmark.sh tmp.prop"
        p = sp.Popen(cmd, bufsize=0, stdout=sp.PIPE, universal_newlines=True, shell=True)
        while True:
            line = p.stdout.readline().strip()
            if (line != ""):
                cnt = len(line.split(";"))
                if (len == 2):
                    val = float(line.split(";")[0].split(":")[2])
                    self.addValue(val)
                else:
                    print(line)
            if line == "":
                break
        self.textLog.SetValue("run done")
        self.setLock(True)


class App(wx.App):
    def OnInit(self):
        self.frame = MainFrame(None, title="dmbench", size=(960, 560))
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True


if __name__ == "__main__":
    app = App(False)
    app.MainLoop()
