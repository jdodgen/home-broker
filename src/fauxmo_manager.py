# fauxmo_manager.py
# Copyright 2022-2023 by James E Dodgen Jr.  All rights reserved.
import subprocess
import time
import const
import database
import multiprocessing
from message import our_ip_address
import os
#
# conditional print
import os 
my_name = os.path.basename(__file__).split(".")[0]
xprint = print # copy print
def print(*args, **kwargs): # replace print
    #return
    xprint("["+my_name+"]", *args, **kwargs) # the copied real print
def print_always(*args, **kwargs): # replace print
    xprint("["+my_name+"]", *args, **kwargs) # the copied real print
#
#

head = """
{
    "FAUXMO": {
        "ip_address": "auto"
    },
    "PLUGINS": {
        "MQTTPlugin": {
            "path": "%s",
            "DEVICES": ["""

tail = """
            ]
        }
    }
}
"""
per_device_minimum = """
                {
                    "port": %s,
                    "name": "%s",
                    "on_cmd": [ "%s", "%s" ],
                    "off_cmd": [ "%s", "%s" ],
                    "mqtt_server": "%s",
                    "mqtt_port": %s,"""

state_cmd = """
                    "state_cmd": "%s","""
qos_cmd = """
                    "qos": "%s","""
retain_cmd = """
                    "retain": "%s","""
use_fake_state = """
                    "use_fake_state": true,"""
initial_state = """
                    "initial_state": "off","""
client_id ="""
                    "mqtt_client_id": "%s","""

login = """
                    "mqtt_user": "%s",
                    "mqtt_pw": "%s","""

end = """
                },"""


def build_cfg():
    db = database.database()
    devices = db.get_fauxmo_devices()
    if len(devices) > 0:
        fauxmo_cfg = head % (const.MQTTPlugin)
        print("number of fauxmo devices[%s]" % (len(devices),))
        for dev in devices:
            port = dev[0].replace('"','\\"') if type(dev[0]) == str else dev[0]
            name = dev[1].replace('"','\\"')
            topic = dev[2].replace('"','\\"')
            on_payload = dev[3].replace('"','\\"')
            off_payload = dev[4].replace('"','\\"')
            fauxmo_cfg = fauxmo_cfg + per_device_minimum % (port, name, topic,on_payload, topic, off_payload, our_ip_address(), const.broker_mqtt_port)
            fauxmo_cfg = fauxmo_cfg + use_fake_state  
            fauxmo_cfg = fauxmo_cfg + initial_state
            """
            # in the future this MAY be added to fauxmo mqtt addon
            if dev[8] != "None" and dev[8] != "":
                fauxmo_cfg = fauxmo_cfg +	state_cmd % (dev[8],)
            if dev[9] != "None" and dev[9] != "":
                fauxmo_cfg = fauxmo_cfg +	client_id % (dev[9],)
            if dev[10] != "None" and dev[10] != "":
                fauxmo_cfg = fauxmo_cfg +	login % (dev[10],dev[11])
            if dev[12] != "None" and dev[12] != "":
                fauxmo_cfg = fauxmo_cfg +	qos_cmd % (dev[12],)
            if dev[13] != "None" and dev[13] != "":
                fauxmo_cfg = fauxmo_cfg +	retain_cmd % (dev[13],) """
            fauxmo_cfg = fauxmo_cfg[:-1] + end
        fauxmo_cfg = fauxmo_cfg[:-1] + tail
        print(fauxmo_cfg)
        return fauxmo_cfg
    else:
        return None
    
def start_fauxmo_task():
    print_always("creating process")
    p = multiprocessing.Process(target=task)
    p.start()
    print_always("is_alive =",p.is_alive())
    return p

def stop_fauxmo_task(p):
    p.terminate()
    time.sleep(1)
    while p.is_alive():
        print("fauxmo wont die")
        time.sleep(0.1)
    p.join()
    p.close()

def task():
    print_always("task starting")
    while True:
        if get_fauxmo_cfg() != None:
            try:
                os.execl("/usr/local/bin/fauxmo", "-c " + const.fauxmo_config_file_path, "-vv")
                # for testing  /usr/local/bin/fauxmo -c /etc/fauxmo/config.json   "
            except:
                pass
            # only returns if it fails
            print("ERROR: faxmo exited, waiting and restarting")
        else:
            pass
            print("No fauxmo devices")
        time.sleep(const.fauxmo_sleep_seconds)  

def get_fauxmo_cfg():
    fauxmo_cfg = build_cfg()
    print("config:",fauxmo_cfg)
    if fauxmo_cfg != None:
        # write the config file
        try:
            os.mkdir(const.fauxmo_default_dir)
        except:
            pass
        fauxmo_config = open(const.fauxmo_config_file_path, "w")
        n = fauxmo_config.write(fauxmo_cfg)
        fauxmo_config.close() 
    return fauxmo_cfg

        # while True:
        #     subprocess.run(["/usr/local/bin/fauxmo", "-c", const.config_file_path])
        #     ## never returns
            
        #     print("fauxmo_manager faxmo exited, waiting and restarting")
        #     time.sleep(10)                   

if __name__ == "__main__":
   
    task()
    time.sleep(1000)
    #print(build_cfg())
   # task()
