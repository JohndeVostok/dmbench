import wx
import datetime


class MainFrame(wx.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(MainFrame, self).__init__(parent, *args, **kwargs)
        self.panel = wx.Panel(self)

        # UI line 1

        self.labelIp = wx.StaticText(self.panel, label="Database IP Address", pos=(20, 20), size=(120, 20))
        self.labelPort = wx.StaticText(self.panel, label="Port", pos=(160, 20), size=(60, 20))
        self.textIp = wx.TextCtrl(self.panel, value="127.0.0.1", pos=(20, 40), size=(120, 20))
        self.textPort = wx.TextCtrl(self.panel, value="5326", pos=(160, 40), size=(60, 20))
        self.textIp.Enable(True)
        self.textPort.Enable(True)

        # UI line 2

        self.labelHouse = wx.StaticText(self.panel, label="WareHouse", pos=(20, 80), size=(60, 20))
        self.labelWorker = wx.StaticText(self.panel, label="Worker", pos=(90, 80), size=(60, 20))
        self.labelTerminal = wx.StaticText(self.panel, label="Terminal", pos=(160, 80), size=(60, 20))
        self.textHouse = wx.TextCtrl(self.panel, value="10", pos=(20, 100), size=(60, 20))
        self.textWorker = wx.TextCtrl(self.panel, value="4", pos=(90, 100), size=(60, 20))
        self.textTerminal = wx.TextCtrl(self.panel, value="10", pos=(160, 100), size=(60, 20))
        self.textHouse.Enable(True)
        self.textWorker.Enable(True)
        self.textTerminal.Enable(True)

        # UI line 3

        self.butLock = wx.Button(self.panel, label="Lock", pos=(20, 140), size=(60, 20))
        self.butLoad = wx.Button(self.panel, label="Load", pos=(90, 140), size=(60, 20))
        self.butRun = wx.Button(self.panel, label="Run", pos=(160, 140), size=(60, 20))
        self.butLock.Enable(True)
        self.butLoad.Enable(False)
        self.butRun.Enable(False)

        self.textLog = wx.TextCtrl(self.panel, pos=(240, 20), size=(210, 200), style=wx.TE_MULTILINE)

        self.ip = "127.0.0.1"
        self.port = 5326
        self.house = 10
        self.worker = 4
        self.terminal = 10
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
        self.textIp.Enable(flag)
        self.textPort.Enable(flag)
        self.textHouse.Enable(flag)
        self.textWorker.Enable(flag)
        self.textTerminal.Enable(flag)
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
            self.ip = self.textIp.GetValue()
            self.port = int(self.textPort.GetValue())
            self.house = int(self.textHouse.GetValue())
            self.worker = int(self.textWorker.GetValue())
            self.terminal = int(self.textTerminal.GetValue())
            strTmp = "Locked,Database:" + self.ip + ":" + str(self.port) + ",Warehouse:" + str(self.house) + ",LoadWorker:" + str(self.worker) + ",Terminal:" + str(self.terminal)
            self.log(strTmp)
            self.setLock(False)
            self.butLock.SetLabel("Unlock")

    def loadData(self, event):
        self.log("load data!")
        self.setLockBut(False)
        self.setLockBut(True)
        self.log("load finish!")

    def runBench(self, event):
        self.log("run bench!")
        self.setLockBut(False)
        self.setLockBut(True)
        self.log("run finish!")


class App(wx.App):
    def OnInit(self):
        self.frame = MainFrame(None, title="dmbench", size=(480, 270))
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True


if __name__ == "__main__":
    app = App(False)
    app.MainLoop()
