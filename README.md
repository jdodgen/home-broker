# AlertAway   
A lightweight home automation system designed to run on low end Linux Computers
It it built on MQTT. It is composed of timers" like for a security light, triggers: where one device causes action on another device, emailer: where events cause emails with jpgs, and voice commands through smart speakers)
It is Edge server system desighed to run on low end Linux SBCs
It is best described as a System of Systems, gluing together other open source projects 
Code lives here: [MQTT-home/linux/alertaway](https://github.com/jdodgen/MQTT-home/tree/main/linux/alertaway)
It is currently a work in progress during converson from a older system.
It has a domain alertaway.com that displays this content.

### Features:
- MQTT - A IBM designed messaging system for devices
- WeMo emulation- legacy
- Phillips Hue emulation (TBD)
- ZigBee HA Home Automation Devices
- IP/WiFi home automation devices
    
### It uses these and other open source projects:
- [fauxmo](https://github.com/n8henrie/fauxmo)
- [zigbee2mqtt](https://github.com/Koenkk/zigbee2mqtt)
- [DiyHue](https://diyhue.org/)
- [Eclipse Mosquitto](https://mosquitto.org/)
- And of course lots of tools like python3, sqlite3

### AlertAway provides the following services: 
- Collecting IP and ZigBee devices into a simplified interface
- Lightweight HTTP servers for:
  - maintain/map fauxmo/Hue  devices
  - Uses zigbee2mqtt to maintain zigbee devices
  - Allow automatic and manual entry of custom IP devices
  - Map MQTT messages to emails with optional IP camera pictures
  - Trigger devices from other devices
- Uses a local or cloud MQTT Brokers
- Written in Python3 with some SQL<br>
- Designed to require NO user configuration after a SD image is built. 

## Hardware requirements 
Simple SBC pretty much anything that can run Linux.      
Must have both a RJ45 to connect to the home router,    
Also a USB port for the zigbee2mqtt compatable [zigbee dongle](https://www.zigbee2mqtt.io/guide/adapters/)

## Current development system:
- Raspbian linux<br>
- AML-S905X-CC (Le Potato) SBC (because RPI 3's were unavailble)
- SONOFF Zigbee 3.0 USB Dongle (compatable and cheap)


It is best described as a System of Systems, gluing together other open source projects.    
Code lives here: [github](https://github.com/jdodgen/MQTT-home/tree/main/linux/alertaway)   
### Features:
- MQTT - A IBM designed messaging system for devices
- WeMo emulation- legacy
- Phillips Hue emulation
- ZigBee HA Home Automation Devices
- IP/WiFi MQTT home automation devices
    
### It uses these and other open source projects:
- [fauxmo](https://github.com/n8henrie/fauxmo)
- [mqtt](https://github.com/eclipse/mosquitto)
- [zigbee2mqtt](https://github.com/Koenkk/zigbee2mqtt)
- [DiyHue](https://diyhue.org/)
- And of course lots of tools like python3, sqlite3

### AlertAway provides the following services: 
- Collecting IP and ZigBee devices into a simplified interface
- Lightweight HTTP servers for:
  - maintain/map fauxmo/Hue  devices
  - Uses zigbee2mqtt to maintain zigbee devices
  - Allow automatic and manual entry of custom IP devices
  - Map MQTT messages to emails with optional IP camera pictures
  - Trigger devices from other devices
- Uses a local or cloud MQTT Brokers
- Written in Python3 with some SQL<br>
- Designed to require NO user configuration after a SD image is built. 

## Hardware requirements 
small SBC, pretty much anything that can run Linux.    
A RJ45/Ethernet port to connect to the home router,        
Also a USB port for the zigbee2mqtt compatable [zigbee dongle](https://www.zigbee2mqtt.io/guide/adapters/)

## Current development system:
- Raspbian linux<br>
- AML-S905X-CC (Le Potato) SBC (because RPI 3's were unavailble)
- SONOFF Zigbee 3.0 USB Dongle (compatable and cheap)

### History:
<pre>
The Project was started in 2011. Originaly written in Perl. 
I started it after a friend had some damage from a water leak when they were away.
At first it used Digi XBee's and later some ZigBee HA devices.
XBee's are all gone now.  
</pre>
