import os
import wx
import sys
import numpy as np
from numpy import interp
import csv
import alert

import time

class AlertList(wx.Panel):
    def __init__(self, parent,alerts=[]):
        wx.Panel.__init__(self, parent)
        self.frame = parent
        self.alerts = alerts

    def initMap(self):

        #self.createAlerts()
        self.createWidgets(self)
        self.onView(self)
        self.frame.Show()
    def refresh(self):
        self.onView(self)
        self.frame.Show()

    def displayAlerts(self):
        st = []
        for alert in self.alerts:
            st.append(wx.StaticText(self,str(alert.id,alert.deviceID,alert.beaconID,alert.severity,alert.status,alert.MSNote,alert.timeSent,alert.timeAckd,alert.lat,alert.long),pos=(25,25)))


    def createWidgets(self, panel):
        img = wx.Image(1178,1056)
        self.imageCtrl = wx.StaticBitmap(panel, wx.ID_ANY,
                                         wx.Bitmap(img))

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.mainSizer.Add(self.imageCtrl, 0, wx.ALL, 5)
        self.mainSizer.Add(self.sizer, 0, wx.ALL, 5)

        self.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self.frame)

        self.Layout()

    def onKey(self, event):
        """
        Check for ESC key press and exit if ESC is pressed
        """
        key_code = event.GetKeyCode()
        if key_code == wx.WXK_ESCAPE:
            sys.exit(0)
        else:
            event.Skip()

    def onView(self, panel):
        filepath = self.photoTxt
        img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        # scale the image, preserving the aspect ratio
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = self.PhotoMaxSize
            NewH = self.PhotoMaxSize * H / W
        else:
            NewH = self.PhotoMaxSize
            NewW = self.PhotoMaxSize * W / H
        img = img.Scale(NewW,NewH)

        self.bitmap = wx.Bitmap(img)
        #print(type(self.x1+self.x2))
        #print(type(self.x1))


        self.displayAlerts();
        self.imageCtrl.SetBitmap(self.bitmap)
        panel.Refresh()

    def drawPosition(self, alertNum, lat, lon,angle):
        #print(lat,":",self.y1,self.y2,":","0",self.bitmap.GetHeight())
        #print(lon,":",self.x1,self.x2,":","0",self.bitmap.GetWidth())
        tmpimg = wx.Image("favicon.ico", wx.BITMAP_TYPE_ANY)

        img_centre = wx.Point( tmpimg.GetWidth()/2, tmpimg.GetHeight()/2 )
        tmpimg = tmpimg.Rotate( angle, img_centre )

        y = interp(lat,[self.y2,self.y1],[self.bitmap.GetHeight(),0])
        x = interp(lon,[self.x1,self.x2],[0,self.bitmap.GetWidth()])
        tmpimg = wx.Bitmap(tmpimg)

        #print(x,y)
        #print(self.bitmap.GetWidth(), self.bitmap.GetHeight())

        dc = wx.MemoryDC(self.bitmap)

        y -= tmpimg.GetHeight()/2
        x -= tmpimg.GetWidth()/2
        dc.DrawBitmap(tmpimg, x, y)
        # pen=wx.Pen('blue',4)
        # dc.SetPen(pen)
        # dc.DrawCircle(x+ tmpimg.GetWidth()/2,y+tmpimg.GetHeight()/2,2)
        # pen=wx.Pen('red',4)
        # dc.SetPen(pen)
        # dc.DrawCircle(x,y,2)
        dc.SelectObject(wx.NullBitmap)

def createAlerts():
    alert1 = alert.Alert()
    alert2 = alert.Alert()
    alert3 = alert.Alert()
    alert1.setGps(0,32.250327, -110.935402,0)
    alert2.setGps(1,32.232162, -110.951885,45)
    alert3.setGps(2,32.226696, -110.960383,90)
    return [alert1,alert2,alert3]

if __name__ == '__main__':
    # app = PhotoCtrl()
    # app.MainLoop()
    alerts = createAlerts()
    app = wx.App()
    frame = wx.Frame(None, title='Photo Control')
    #self.frame.ShowFullScreen(True)
    frame.Maximize(True)
    panel = Map(frame)
    panel.alerts = alerts
    panel.refresh()
    time.sleep(1)
    panel.alerts = [alerts[0], alerts[1]]
    panel.refresh()
    frame.Show()
    app.MainLoop()
