# SeniorDesign
Checklist of things to do:

Main Station Software:
main page: beacon map, view emergency alerts, sidebar w/ new alerts (all pages have back to main menu option)
Map view of beacons - map of the tucson area with icons for each beacon, (gps coords on mouseover?) displays if alert triggered or repair needed.
Emergency alerts page: new displayed, resolved on different page
-resolved page: data abt alert
when viewing new alert, text box for message + ack
yes/no for resolving alert

backend stuff: 
Xbee connection - receive GPS data from beacons
XBee connection - get alerts from beacons after the beacons get them from the app
XBee - send ack + message to alert device
Interface with MySQL database?!?! PHP database!?!?!?

Mobile Application:
Main page: buttons for emergencies options, map, "about app" and (about me") - each of these pages has a link back to the main page
About app: just text
map view: pre downloaded map of tucson that will get the user's GPS location and display their location on the map, 
or text that says "outside bounds" if their location ins't on the map. If the phones gps isn't working, get the gpd coords of the nearet
beacon and draw a circle of 20m around that point that says "you're within this circle"
Emergency options: 3 buttons for 3 levels of emergency, yes/no confirm after. 
- these have 4 states: no yes/no (fine), yes, no, no yes/no (not fine) (if rest is finished, add optional text box)
ack screen: "sending" (after hitting button) "sending..." (ack from beacon). (send) ack from main station (text), reset button 
(display note from main station)
About me: (optional) ICE info (medical conditions, contact info)

Beacon Software:
GPS connection: get the beacon's gps, save it. get new coords once every 24 hours, gps should sleep
bluetooth/mobile app: 
(according to adafruit tutorial) broadcasts a char string that mobile app bluetooth looks for
send GPS coords if mobile app requests it for map


