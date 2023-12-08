# home-broker
A LAN server system desighed to run on low end Linux SBCs<br>
It is best described as a System of Systems, gluing together other open source projects. 
    
### Features:
- MQTT
- WeMo (amazon Alexa)
- ZigBee Home Automation Devices
- IP/WiFi MQTT home automation devices
    
### It uses these other open source projects:
- [fauxmo](https://github.com/n8henrie/fauxmo)
- [mqtt](https://github.com/eclipse/mosquitto)
- [zigbee2mqtt](https://github.com/Koenkk/zigbee2mqtt)
- And ofcourse tools like Python, sqlite

### home-broker provides the following services: 
- Collecting IP/ZigBee devices into a simplified interface
- Lightweight HTTP serverer for:
  - maintain/map fauxmo devices
  - provides a link zigbee2mqtt to maintain zigbee devices
  - allow manual entry of custom IP devices
  - auto collects home-broker IP devices
  - view consilodated devices and generated pub/sub topics/payloads
  - it can be used to test devices turn on and off
- Publish a simplified JSON file of all IP and Zigbee devices
  - containing MQTT pup/sub and payload strings
  - Available to feed other Home Automation systems
- A local MQTT Broker
- A WeMo to MQTT device mapping

currently developed/tested on Raspbian Linux, should work on any linux/Unix<br>
Written in Python3 with some SQL<br>
Designed to require NO user configuration after a img is built. 
### Summary:
<pre>
home-broker - a small dedicated mqtt, fauxmo and zigbee server
it consolodates zigbee and Internet/WiFi devices in a sqlite database.
It only collects and distributes configuration
It serves device information via pub/sub to extract devices from database
to be used by other automation systems.
This data is simplfied and provides formatted data including the pub/sub strings
</pre>
## Hardware requirements 
SBC  pretty much anything that can run Linux<br>
with RJ45 to connect to the home router<br>
and a USB port for the zigbee dongle
## Current development system:
Raspbian linux<br>
AML-S905X-CC (Le Potato) SBC (because RPI 3's were unavailble).<br>
"SONOFF Zigbee 3.0 USB Dongle" (compatable and cheap)<br>
Here are the working dongles<br>
https://www.zigbee2mqtt.io/guide/adapters/<br> 
