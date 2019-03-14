class Beacon:
    def __init__(self):
        self.id = 0
        self.lat = 0
        self.lon = 0
        self.time = 0
        self.missedPings = 0

    def setGPS(self, id1, lat, lon, heading, time1):
        self.id = id1
        self.lat = lat
        self.lon = lon
        self.time = time1

    def pingIncrement(self):
        self.missedPings += 1
