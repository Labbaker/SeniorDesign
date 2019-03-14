#!/bin/python

import wx;
import beacon;
import GPSMap as Map
import beaconPanel as BeaconList
import time
import sys
import serial

class HelloFrame(wx.Frame):
    """
    A frame that says Hello World
    """

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(HelloFrame, self).__init__(*args, **kw)

        #print("Created Frame\n")

        #create a top panel, all of the other panels will render inside this.
        topPanel = wx.Panel(self)

        # create a panel in the Frame
        #self.createBeacons()
        panel1 = wx.Panel(topPanel)
        panel1.SetBackgroundColour('#ffffff')
        # and put some text with a larger bold font on it
        st = wx.StaticText(panel1, label="Hit [SPACE] to begin:", pos=(25,25))
        font = st.GetFont()
        font.PointSize += 10
        font = font.Bold()
        #font.SetFac("dyslexie")
        st.SetFont(font)

        # Make another Panel
        self.beacons=[]

        # Open the Serial Port
        self.ser = serial.Serial(port = "COM6", baudrate=9600, parity=serial.PARITY_EVEN)
        self.outFile = open("log_out.csv","w")

        #beacons = Map.createBeacons()
        self.mapPanel = Map.Map(topPanel)
        self.mapPanel.SetBackgroundColour('#ffffff')
        self.mapPanel.initMap(height = 800)
        self.mapPanel.Bind(wx.EVT_KEY_DOWN, self.onKey)

        #beacon panel
        beaconPanel = BeaconList.BeaconList(topPanel);
        beaconPanel.SetBackgroundColour('#ccccff')
        beaconText = wx.StaticText(beaconPanel, label="Beacons", pos=(10,20))
        #
        alertPanel = wx.Panel(topPanel);
        alertPanel.SetBackgroundColour('#ffcccc')
        alertText = wx.StaticText(alertPanel, label="Alerts", pos=(10,20))
        # Create a sizer (layout manager)
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Add the other panels to the sizer
        sizer.Add(panel1,0,wx.EXPAND|wx.ALL)
        sizer.Add(self.mapPanel,0,wx.EXPAND|wx.ALL)
        sizer.Add(beaconPanel,0,wx.EXPAND|wx.ALL)
        sizer.Add(alertPanel,0,wx.EXPAND|wx.ALL)
        topPanel.SetSizer(sizer)

        # create a menu bar
        self.makeMenuBar()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("GUIx 127.0.0.1")
        self.itter = 0
        # Start in fullscreen
        self.ShowFullScreen(True, style= wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE | wx.FULLSCREEN_NOBORDER)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)

#beacon response message format:
#PG,ID,0,LT,0,LN,0,TS,0
#Alert, concat'd id, deviceid, beaconid, severity, time sent
#AT,ID,0,DI,0,BI,0,SV,0,ST,0,TS,0,LT,0,LN,0

    def update(self, event):
        #pin acking
        i = 0
        ID = None
        LAT = None
        LON = None
        TIMEST = None
        DEVID = None
        BEAID = None
        SEV = None
        STAT = None

        if (self.ser.in_waiting > 0):
            while (self.ser.in_waiting > 0):
                """
                # Read a line from the serial buffer,
                # decode it using utf-8 and
                # split it into chunks at each comma
                """
                line = self.ser.readline().decode("utf-8")
                self.outFile.write(line)
                #print(line)
                line = line.split(',')
                for i in range(len(line)):
                    if line[i] == 'PG':
                        for i in range(len(line)):
                            if line[i] == 'ID':
                                ID = int(line[i+1])
                            elif line[i] == 'LT':
                                LAT = float(line[i+1])/1000000
                            elif line[i] == 'LN':
                                LON = float(line[i+1])/1000000
                            elif line[i] == 'TS':
                                TIMEST = float(line[i+1])
                        inList = False
                        for beaconTmp in self.beacons:
                            if beaconTmp.id == ID:
                                beaconTmp.setGPS(ID, LAT, LON, TIMEST)
                                inList = True
                            else:
                                beaconTmp = beacon.Beacon()
                                beaconTmp.setGPS(ID, LAT, LON, TIMEST)
                                self.beacons.append(beaconTmp)
                    #AT,ID,0,DI,0,BI,0,SV,0,TS,0,LT,0,LN,0
                    elif line[i] == 'AT':
                        for i in range(len(line)):
                            if line[i] == 'ID':
                                ID = int(line[i+1])
                            elif line[i] == 'DI':
                                DEVID = float(line[i+1])
                            elif line[i] == 'BI':
                                BEAID = float(line[i+1])
                            elif line[i] == 'SV':
                                SEV = float(line[i+1])
                            elif line[i] == 'ST':
                                STAT = float(line[i+1])
                            elif line[i] == 'TS':
                                TIMEST = float(line[i+1])
                            elif line[i] == 'LT':
                                LAT = float(line[i+1])
                            elif line[i] == 'LN':
                                LON = float(line[i+1])
                            inList = False
                            for alertTmp in self.alerts:
                                if alertTmp.id == ID:
                                    alertTmp.setAlertInfo(ID, DEVID, BEAID, SEV, STAT, TIMEST, LAT, LON)
                                    inList = True
                                else:
                                    alertTmp = alert.Alert()
                                    alertTmp.setAlertInfo(ID, DEVID, BEAID, SEV, STAT, TIMEST, LAT, LON)
                                    self.alerts.append(AlertTmp)
                #print("ID:",ID,"\t","LAT:",LAT,"\t","LON:",LON,"\t","HEAD:",HEAD)
            #print("render")
            self.mapPanel.beacons = self.beacons
            self.beaconPanel.beacons = self.beacons
            self.alertPanel.alerts = self.alerts
            self.mapPanel.refresh()
            self.beaconPanel.refresh()
            self.alertPanel.refresh()
            self.Show()

    def onKey(self, event):
        """
        Check for ESC key press and exit is ESC is pressed
        """
        key_code = event.GetKeyCode()
        if key_code == wx.WXK_ESCAPE:
            sys.exit(0)
        elif key_code == wx.WXK_SPACE:
            self.timer.Start(1)
        else:
            event.Skip()
    def changeBS(self):
        if self.itter == 0:
            self.mapPanel.beacons = [self.mapPanel.beacons[0], self.mapPanel.beacons[1]]
            self.itter = 1
        else:
            self.mapPanel.beacons = Map.createBeacons()
            self.itter = 0
        self.mapPanel.refresh()
    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called when teh menu item is selected.
        """

        # Make a file menu with hello and Exit items
        fileMenu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        helloItem = fileMenu.Append(-1, "&Hello...\tCtrl-H",
            "Help string shown in status ar for this menu item")
        fileMenu.AppendSeparator()
        # When using a stock ID, we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(wx.ID_EXIT)

        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the Frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)


    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.outFile.close()
        self.Close(True)


    def OnHello(self, event):
        """Say hello to the user."""
        wx.MessageBox("Hello again from wxPython")


    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("This is a wxPython Hello World sample",
                    "About Hello World 2",
                    wx.OK|wx.ICON_INFORMATION)

    def createBeacons(self):
        self.beacon1 = beacon.Beacon()
        self.beacon1.setGPS(0,32.250327, -110.935402,0)
        self.beacons = [self.beacon1]


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # fram, show it, and start the event loop.
    app = wx.App()
    frm = HelloFrame(None, title='HelloWorld 2')
    frm.Show()
    app.MainLoop()
