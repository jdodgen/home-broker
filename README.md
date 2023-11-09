# home-broker
<p>A server that uses fauxmo, mqtt and zigbee2mqtt to consolodate and zigbee as well as custom IP devices.
simplified mapping of Wemo names to devices.
External systems provieded with formatted MQTT topics/payload for easy device comminication.
</p>
currently tested on Raspbian Linux, should work on any linux/Unix<br>
Written in Python3 with some SQL.<br>
Designed to be zero user configuration once an img is built. 
<pre>
home-broker - a small dedicated mqtt, fauxmo and zigbee server
it consolodates zigbee and Internet/WiFi devices in a sqlite database.
It only collects and distributes configuration and does not command devices
Except when testing via HTTP 

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
</pre>
# Hardware requirements 
SBC  pretty much anthing that can run Linux<br>
with RJ45 to coonect to the users router<br>
and a USB port for the zigbee dongle



# Current development system:
Raspbian linux<br>
AML-S905X-CC (Le Potato) SBC (because RPI 3's were unavailble).<br>
"SONOFF Zigbee 3.0 USB Dongle" (compatable and cheap)<br>
Here are the working dongles<br>
https://www.zigbee2mqtt.io/guide/adapters/<br> 
