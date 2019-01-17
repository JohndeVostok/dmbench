import wx
import datetime
import benchconn
import time
import threading
import random
import subprocess as sp
import wx.lib.plot as plot


class SettingFrame(wx.Frame):
    def __init__(self, parent):
        super(SettingFrame, self).__init__(parent, title="Settings", size=(480, 560))
        self.font = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.panel = wx.Panel(self)
        self.panel.SetFont(self.font)

        self.labelAddr = wx.StaticText(self.panel, label="Database Address", pos=(40, 40), size=(380, 40))
        self.textAddr = wx.TextCtrl(self.panel, value="127.0.0.1:5326/tpcc", pos=(40, 80), size=(380, 40))
        self.textAddr.Enable(True)
        self.labelUser = wx.StaticText(self.panel, label="User", pos=(40, 120), size=(180, 40))
        self.labelPass = wx.StaticText(self.panel, label="Password", pos=(240, 120), size=(180, 40))
        self.textUser = wx.TextCtrl(self.panel, value="SYSDBA", pos=(40, 160), size=(180, 40))
        self.textPass = wx.TextCtrl(self.panel, value="SYSDBA", pos=(240, 160), size=(180, 40))
        self.textUser.Enable(True)
        self.textPass.Enable(True)
        self.labelHouse = wx.StaticText(self.panel, label="WareHouse", pos=(40, 200), size=(180, 40))
        self.labelWorker = wx.StaticText(self.panel, label="LoadWorker", pos=(240, 200), size=(180, 40))
        self.textHouse = wx.TextCtrl(self.panel, value="10", pos=(40, 240), size=(180, 40))
        self.textWorker = wx.TextCtrl(self.panel, value="4", pos=(240, 240), size=(180, 40))
        self.textHouse.Enable(True)
        self.textWorker.Enable(True)
        self.labelTerminal = wx.StaticText(self.panel, label="Terminal", pos=(40, 280), size=(180, 40))
        self.labelTime = wx.StaticText(self.panel, label="RunTime", pos=(240, 280), size=(180, 40))
        self.textTerminal = wx.TextCtrl(self.panel, value="10", pos=(40, 320), size=(180, 40))
        self.textTime = wx.TextCtrl(self.panel, value="10", pos=(240, 320), size=(180, 40))
        self.textTerminal.Enable(True)
        self.textTime.Enable(True)
        self.butSave = wx.Button(self.panel, label="Save", pos=(100, 420), size=(120, 40))
        self.butCancel = wx.Button(self.panel, label="Cancel", pos=(240, 420), size=(120, 40))
        self.Bind(wx.EVT_BUTTON, self.actSave, self.butSave)
        self.Bind(wx.EVT_BUTTON, self.actCancel, self.butCancel)

    def actSave(self, event):
        self.Destroy()

    def actCancel(self, event):
        self.Destroy()


class MainFrame(wx.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(MainFrame, self).__init__(parent, *args, **kwargs)
        self.font = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.panel = wx.Panel(self)
        self.panel.SetFont(self.font)

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
        self.textLog.SetValue("set")

    def actLoad(self, event):
        settingFrame = SettingFrame(self)
        settingFrame.Show(True)
        self.textLog.SetValue("load")

    def actRun(self, event):
        self.setLock(False)

        cmd = "./runBenchmark.sh dm.prop"
        p = sp.Popen(cmd, bufsize=0, stdout=sp.PIPE, universal_newlines=True, shell=True)
        while True:
            l = p.stdout.readline()
            if (l != ""):
                val = float(l.strip().split(";")[0].split(":")[2]) 
                self.addValue(val)
            if l == "done":
                break
        self.textLog.SetValue("run done")
        self.setLock(True)

#        self.labelAddr = wx.StaticText(self.panel, label="Database Address", pos=(40, 40), size=(400, 40))
#        self.textAddr = wx.TextCtrl(self.panel, value="127.0.0.1:5326/tpcc", pos=(40, 80), size=(400, 40))
#        self.textAddr.Enable(True)
#        self.labelUser = wx.StaticText(self.panel, label="User", pos=(40, 120), size=(180, 40))
#        self.labelPass = wx.StaticText(self.panel, label="Password", pos=(260, 120), size=(180, 40))
#        self.textUser = wx.TextCtrl(self.panel, value="SYSDBA", pos=(40, 160), size=(180, 40))
#        self.textPass = wx.TextCtrl(self.panel, value="SYSDBA", pos=(260, 160), size=(180, 40))
#        self.textUser.Enable(True)
#        self.textPass.Enable(True)
#        self.labelHouse = wx.StaticText(self.panel, label="WareHouse", pos=(40, 200), size=(180, 40))
#        self.labelWorker = wx.StaticText(self.panel, label="LoadWorker", pos=(260, 200), size=(180, 40))
#        self.textHouse = wx.TextCtrl(self.panel, value="10", pos=(40, 240), size=(180, 40))
#        self.textWorker = wx.TextCtrl(self.panel, value="4", pos=(260, 240), size=(180, 40))
#        self.textHouse.Enable(True)
#        self.textWorker.Enable(True)#
#        self.labelTerminal = wx.StaticText(self.panel, label="Terminal", pos=(40, 280), size=(180, 40))
#        self.labelTime = wx.StaticText(self.panel, label="RunTime", pos=(260, 280), size=(180, 40))
#        self.textTerminal = wx.TextCtrl(self.panel, value="10", pos=(40, 320), size=(180, 40))
#        self.textTime = wx.TextCtrl(self.panel, value="10", pos=(260, 320), size=(180, 40))
#        self.textTerminal.Enable(True)
#        self.textTime.Enable(True)
#        self.butLock.Enable(True)
#        self.butLoad.Enable(False)
#        self.butRun.Enable(False)

#        self.addr = "127.0.0.1:5326/tpcc"
#        self.user = "SYSDBA"
#        self.password = "SYSDBA"
#        self.house = 10
#        self.worker = 4
#        self.terminal = 10
#        self.time = 10
#        self.lockStatus = False
#        self.logInfo = []

#        self.Bind(wx.EVT_BUTTON, self.lock, self.butLock)
#        self.Bind(wx.EVT_BUTTON, self.loadData, self.butLoad)

#    def log(self, strLog):
#        nowTime = datetime.datetime.now().strftime("%H:%M:%S")
#        self.logInfo.append(nowTime + ":" + strLog)
#        strTmp = "\r\n".join(self.logInfo)
#        self.textLog.SetValue(strTmp)


'''
    def setLock(self, flag):
        self.lockStatus = not flag
        self.textAddr.Enable(flag)
        self.textUser.Enable(flag)
        self.textPass.Enable(flag)
        self.textHouse.Enable(flag)
        self.textWorker.Enable(flag)
        self.textTerminal.Enable(flag)
        self.textTime.Enable(flag)
        self.butLoad.Enable(not flag)
        self.butRun.Enable(not flag)

    def setLockBut(self, flag):
        self.butLock.Enable(flag)
        self.butLoad.Enable(flag)
        self.butRun.Enable(flag)

    def lock(self, event):
        if self.lockStatus:
            self.setLock(True)
            self.butLock.SetLabel("Lock")
        else:
            self.addr = self.textAddr.GetValue()
            self.user = self.textUser.GetValue()
            self.password = self.textPass.GetValue()
            self.house = int(self.textHouse.GetValue())
            self.worker = int(self.textWorker.GetValue())
            self.terminal = int(self.textTerminal.GetValue())
            self.time = int(self.textTime.GetValue())
            props = self.genprop(self.addr, self.user, self.password, self.house, self.worker, self.terminal, self.time)
            self.log("tmp.props updated.")
            self.setLock(False)
            self.butLock.SetLabel("Unlock")

    def loadData(self, event):
        self.log("load data!")
        self.setLockBut(False)
        s = benchconn.load()
        self.log(s)
        self.setLockBut(True)
        self.log("load finish!")

    def runBench(self, event):
        self.log("run bench!")
        self.setLockBut(False)
        s = benchconn.run()
        self.log(s)
        self.setLockBut(True)
        self.log("run finish!")
'''


class App(wx.App):
    def OnInit(self):
        self.frame = MainFrame(None, title="dmbench", size=(960, 560))
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True


if __name__ == "__main__":
    app = App(False)
    app.MainLoop()
