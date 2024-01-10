# fauxmo_manager.py
# Copyright 2022-2023 by James E Dodgen Jr.  All rights reserved.
import subprocess
import time
import const
import database
import multiprocessing
import os
import logging
logger = None


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
        logger.info("len devices[%s]" % (len(devices),))
        for dev in devices:
            port = dev[0].replace('"','\\"') if type(dev[0]) == str else dev[0]
            name = dev[1].replace('"','\\"')
            on_topic = dev[2].replace('"','\\"')
            on_payload = dev[3].replace('"','\\"')
            off_topic = dev[4].replace('"','\\"')
            off_payload = dev[5].replace('"','\\"')
            fauxmo_cfg = fauxmo_cfg + per_device_minimum % (port, name, on_topic,on_payload, off_topic, off_payload, const.broker, const.broker_mqtt_port)
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
        logger.info(fauxmo_cfg)
        return fauxmo_cfg
    else:
        return None

def start_fauxmo_task():
    p = multiprocessing.Process(target=task)
    p.start()
    return p

def stop_fauxmo_task(p):
    logger = logging.getLogger(__name__)
    p.terminate()
    time.sleep(1)
    while p.is_alive():
        logger.warning("fauxmo wont die")
        time.sleep(0.1)
    p.join()
    p.close()

def task():
    global logger
    logger = logging.getLogger(const.log(__file__))
    while True:
        if get_fauxmo_cfg() != None:
            try:
                os.execl("/usr/local/bin/fauxmo", "-c " + const.fauxmo_config_file_path, "-v")
            except:
                pass
            # only returns if it fails
            logger.warning("fauxmo_manager faxmo exited, waiting and restarting")
        else:
            pass
            logger.info("fauxmo_manager nothng to do, waiting and restarting")
        time.sleep(const.fauxmo_sleep_seconds)  

def get_fauxmo_cfg():
    fauxmo_cfg = build_cfg()
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
            
        #     logger.info("fauxmo_manager faxmo exited, waiting and restarting")
        #     time.sleep(10)                   

if __name__ == "__main__":
   
    task()
    time.sleep(1000)
    #logger.info(build_cfg())
   # task()
