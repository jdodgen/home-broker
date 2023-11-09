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


# Test system: 
"Le Potato" (because RPI 3's were unavailble).
"SONOFF Zigbee 3.0 USB Dongle" (compatable and cheap)

# from:
https://github.com/n8henrie/fauxmo-plugins

# download mqttplugin.py

and place it here with the rest of the home-broker py code

install raspbian lite or linux distro of your choice

# we name this "home-broker" later
# you can access via http://home-broker.local  when on your LAN

# set login 

# if using raspian change the following in raspi-config:

sudo raspi-config

  # fix the following:
  # system option > host name "home-broker"
  # system > auto login (this system auto runs at boot
  #        to make debugging easier)
  # interface options > enable ssh  
  # performance options > video memory as small as possable
  # localization set time zone
  # advanced options expand sd card 
  # when finished allow it to reboot

 

# now "putty in" from your computer to make things easier:

use home-broker.local for the address

sudo apt update
sudo apt upgrade
sudo apt install pip
sudo apt install mosquitto

# You do this IF we run it from main.py 
# right now we let it run by itsself

# sudo systemctl disable mosquitto.service

# to start, monitor and restart as needed 

# bring in the python packages

sudo pip install fauxmo
sudo pip install paho.mqtt
sudo pip install gevent
sudo pip install flask
sudo pip install pgrep

# fix the conf.d directory for a future ftp
# not used # sudo chmod a+w /etc/mosquitto/conf.d

# now install zigbee2mqtt

https://www.zigbee2mqtt.io/guide/installation/01_linux.html

# change config to use home-broker.local for the broker
# broker has not been configured yet 

copy mosquitto.conf to /etc/mosquitto/conf.d

# now install home-broker code
sftp down the following (filezilla):
const.py
database.py
devices_to_json.py
fauxmo_manager.py
http_server.py
index_html.py
json_tools.py
load_IP_device_data.py
load_zigbee_data.py
main.py
message.py
mosquitto_manager.py
mqtt_service_task.py
mqttplugin.py
zigbee2mqtt_manager.py

copy mosquitto.conf to /etc/mosquitto/conf.d

# set it up to auto start the home-broker code
replace /dev/ttyUSB0 with your ZBC port


edit  .bashrc 
add to the end the following 

sudo chmod a+rw /dev/ttyUSB0
echo booting in 10 seconds
sleep 10
sudo python3 main.py
```

