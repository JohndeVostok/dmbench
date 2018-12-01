import wx
import datetime
import benchconn


class MainFrame(wx.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(MainFrame, self).__init__(parent, *args, **kwargs)
        self.panel = wx.Panel(self)

        self.labelAddr = wx.StaticText(self.panel, label="Database Address", pos=(20, 20), size=(200, 20))
        self.textAddr = wx.TextCtrl(self.panel, value="127.0.0.1:5326/tpcc", pos=(20, 40), size=(200, 20))
        self.textAddr.Enable(True)

        self.labelUser = wx.StaticText(self.panel, label="User", pos=(20, 60), size=(90, 20))
        self.labelPass = wx.StaticText(self.panel, label="Password", pos=(130, 60), size=(90, 20))
        self.textUser = wx.TextCtrl(self.panel, value="SYSDBA", pos=(20, 80), size=(90, 20))
        self.textPass = wx.TextCtrl(self.panel, value="SYSDBA", pos=(130, 80), size=(90, 20))
        self.textUser.Enable(True)
        self.textPass.Enable(True)

        self.labelHouse = wx.StaticText(self.panel, label="WareHouse", pos=(20, 100), size=(90, 20))
        self.labelWorker = wx.StaticText(self.panel, label="LoadWorker", pos=(130, 100), size=(90, 20))
        self.textHouse = wx.TextCtrl(self.panel, value="10", pos=(20, 120), size=(90, 20))
        self.textWorker = wx.TextCtrl(self.panel, value="4", pos=(130, 120), size=(90, 20))
        self.textHouse.Enable(True)
        self.textWorker.Enable(True)

        self.labelTerminal = wx.StaticText(self.panel, label="Terminal", pos=(20, 140), size=(90, 20))
        self.labelTime = wx.StaticText(self.panel, label="RunTime", pos=(130, 140), size=(90, 20))
        self.textTerminal = wx.TextCtrl(self.panel, value="10", pos=(20, 160), size=(90, 20))
        self.textTime = wx.TextCtrl(self.panel, value="10", pos=(130, 160), size=(90, 20))
        self.textTerminal.Enable(True)
        self.textTime.Enable(True)

        self.butLock = wx.Button(self.panel, label="Lock", pos=(20, 200), size=(60, 20))
        self.butLoad = wx.Button(self.panel, label="Load", pos=(90, 200), size=(60, 20))
        self.butRun = wx.Button(self.panel, label="Run", pos=(160, 200), size=(60, 20))
        self.butLock.Enable(True)
        self.butLoad.Enable(False)
        self.butRun.Enable(False)

        self.textLog = wx.TextCtrl(self.panel, pos=(240, 20), size=(210, 220), style=wx.TE_MULTILINE)

        self.addr = "127.0.0.1:5326/tpcc"
        self.user = "SYSDBA"
        self.password = "SYSDBA"
        self.house = 10
        self.worker = 4
        self.terminal = 10
        self.time = 10
        self.lockStatus = False
        self.logInfo = []

        self.Bind(wx.EVT_BUTTON, self.lock, self.butLock)
        self.Bind(wx.EVT_BUTTON, self.loadData, self.butLoad)
        self.Bind(wx.EVT_BUTTON, self.runBench, self.butRun)

    def log(self, strLog):
        nowTime = datetime.datetime.now().strftime("%H:%M:%S")
        self.logInfo.append(nowTime + ":" + strLog)
        strTmp = "\r\n".join(self.logInfo)
        self.textLog.SetValue(strTmp)

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
            props = benchconn.genprop(self.addr, self.user, self.password, self.house, self.worker, self.terminal, self.time)
            self.log("tmp.props updated.")
            self.setLock(False)
            self.butLock.SetLabel("Unlock")

    def loadData(self, event):
        self.log("load data!")
        self.setLockBut(False)
        benchconn.load()
        self.setLockBut(True)
        self.log("load finish!")

    def runBench(self, event):
        self.log("run bench!")
        self.setLockBut(False)
        benchconn.run()
        self.setLockBut(True)
        self.log("run finish!")


class App(wx.App):
    def OnInit(self):
        self.frame = MainFrame(None, title="dmbench", size=(480, 300))
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True


if __name__ == "__main__":
    app = App(False)
    app.MainLoop()
