import os
import wx
import sys
import numpy as np
from numpy import interp
import csv
import beacon

import time

class BeaconList(wx.Panel):
    def __init__(self, parent,beacons=[]):
        wx.Panel.__init__(self, parent)
        self.frame = parent
        self.beacons = beacons

    def initMap(self):

        #self.createBeacons()
        self.createWidgets(self)
        self.onView(self)
        self.frame.Show()
    def refresh(self):
        self.onView(self)
        self.frame.Show()

    def displayBeacons(self):
        st = []
        for beacon in self.beacons:
            st.append(wx.StaticText(self,str(beacon.id,beacon.lat,beacon.long,beacon.time,beacon.missedPings), pos=(25,25)))


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


        self.displayBeacons();
        self.imageCtrl.SetBitmap(self.bitmap)
        panel.Refresh()

    def drawPosition(self, beaconNum, lat, lon,angle):
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

def createBeacons():
    beacon1 = beacon.Beacon()
    beacon2 = beacon.Beacon()
    beacon3 = beacon.Beacon()
    beacon1.setGPS(0,32.250327, -110.935402,0)
    beacon2.setGPS(1,32.232162, -110.951885,45)
    beacon3.setGPS(2,32.226696, -110.960383,90)
    return [beacon1,beacon2,beacon3]

if __name__ == '__main__':
    # app = PhotoCtrl()
    # app.MainLoop()
    beacons = createBeacons()
    app = wx.App()
    frame = wx.Frame(None, title='Photo Control')
    #self.frame.ShowFullScreen(True)
    frame.Maximize(True)
    panel = Map(frame)
    panel.beacons = beacons
    panel.refresh()
    time.sleep(1)
    panel.beacons = [beacons[0], beacons[1]]
    panel.refresh()
    frame.Show()
    app.MainLoop()
