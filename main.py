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

        # UI line 2

        self.labelHouse = wx.StaticText(self.panel, label="WareHouse", pos=(20, 80), size=(60, 20))
        self.labelWorker = wx.StaticText(self.panel, label="Worker", pos=(90, 80), size=(60, 20))
        self.labelTerminal = wx.StaticText(self.panel, label="Terminal", pos=(160, 80), size=(60, 20))
        self.textHouse = wx.TextCtrl(self.panel, value="10", pos=(20, 100), size=(60, 20))
        self.textWorker = wx.TextCtrl(self.panel, value="4", pos=(90, 100), size=(60, 20))
        self.textTerminal = wx.TextCtrl(self.panel, value="10", pos=(160, 100), size=(60, 20))

#        self.butCreate = wx.Button(self.panel, label="create", pos=(20, 80), size=(55, 20))
#        self.butDrop = wx.Button(self.panel, label="drop", pos=(85, 80), size=(55, 20))
        self.textLog = wx.TextCtrl(self.panel, pos=(240, 20), size=(210, 200), style=wx.TE_MULTILINE)

        self.strIp = ""
        self.strPort = ""
        self.logInfo = []

#        self.Bind(wx.EVT_BUTTON, self.createTable, self.butCreate)
#        self.Bind(wx.EVT_BUTTON, self.dropTable, self.butDrop)

    def log(self, strLog):
        nowTime = datetime.datetime.now().strftime("%H:%M:%S")
        self.logInfo.append(nowTime + ": " + strLog)
        strTmp = "\r\n".join(self.logInfo)
        self.textLog.SetValue(strTmp)

    def refresh(self):
        self.strIp = self.textIp.GetValue()
        self.strPort = self.textPort.GetValue()

    def createTable(self, event):
        self.refresh()
        strTmp = "create: " + self.strIp + ":" + self.strPort
        self.log(strTmp)

    def dropTable(self, event):
        self.refresh()
        strTmp = "drop: " + self.strIp + ":" + self.strPort
        self.log(strTmp)


class App(wx.App):
    def OnInit(self):
        self.frame = MainFrame(None, title="dmbench", size=(480, 270))
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True


if __name__ == "__main__":
    app = App(False)
    app.MainLoop()
