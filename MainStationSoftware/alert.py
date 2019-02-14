class Alert:
    def _init_(self):
        self.id = 0
        self.deviceID = 0
        self.beaconID = 0
        self.severity = 0
        self.status = 0 #1 is active, 0 is inactive
        self.MSNote = 0
        self.timeSent = 0
        self.timeAckd = 0
        self.lat = 0
        self.lon = 0

    #call this function when the main station first receives an alert
    def setAlertInfo(self, id1, deviceID1, beacon1, severity1, status1, time1, lat1, lon1):
        self.id = id1
        self.deviceID = deviceID1
        self.beaconID = beacon1
        self.severity = severity1
        self.status = status1 #automatically set status to active
        self.timeSent = time1
        self.lat = lat1
        self.lon = lon1

    #set the status to active or inactive
    def setAlertStatus(self, status1):
        self.status = status1

    #update for the ack sent
    def ackAlert(self, note1, time1):
        self.MSNote = note1
        self.timeAckd = time1
