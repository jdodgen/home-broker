# home-broker
A server that uses fauxmo, mqtt and zigbee2mqtt to consolodate and zigbee as well as custom IP devices.
simplified mapping of Wemo names to devices.
External systems provieded with formatted MQTT topics/payload for easy device comminication.

currently tested on Raspbian Linux, should work on any linux/Unix
Written in Python3 with some SQL.

Here is my Install.txt for some doucmentation I will edit as files are added
```
home-broker - a small dedicated mqtt, fauxmo and zigbee server
it consolodates zigbee and Internet/WiFi devices in a sqlite database.
It only collects configuration and does not command devices

a small http server exists: 
    1) maintain/map fauxmo devices
    2) provides a link zigbee2mqtt to maintain zigbee devices
    3) allow manual entry of custom IP devices
    4) auto collects home-broker IP devices 
    5) view consilodated devices and generated pub/sub topics/payloads
    6) it can be used to test devices turn on and off

It serves device information via pub/sub to extract devices from database
to be used by other automation systems.
This data is simplfied and provides formatted data including the pub/sub strings 

Hardware. 
SBC  pretty much anthing that can run Linux with RJ45 
    and a USB port for the zigbee dongle
 
here are the working dongles
https://www.zigbee2mqtt.io/guide/adapters/ 


# Current development system:
Raspbian linux
"Le Potato" SBC (because RPI 3's were unavailble).
"SONOFF Zigbee 3.0 USB Dongle" (compatable and cheap)


```

