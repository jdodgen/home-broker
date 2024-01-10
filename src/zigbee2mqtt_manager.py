# zigbee2mqtt_manager
# Copyright 2023 by James E Dodgen Jr.  All rights reserved.
import subprocess
import time
import multiprocessing
import os
import const
import logging
logger = None

def start_zigbee2mqtt_task(watch_dog_queue):
    p = multiprocessing.Process(target=task, args=(watch_dog_queue,))
    p.start()
    return p

def stop_zigbee2mqtt_task(p):
    p.terminate()
    while p.is_alive():
        logger.info("zigbee2mqtt wont die")
        time.sleep(0.1)
    p.join()
    p.close()

def task(watch_dog_queue):
    global logger
    logger = logging.getLogger(const.log(__file__))
   
    while True:
        # not sure why they need this but this will run it
        os.chdir("/opt/zigbee2mqtt")
        logger.info(os.getcwd())
        # subprocess.run(["sudo", "systemctl", "stop", "zigbee2mqtt"])  # just incase 
        subprocess.run(["/usr/bin/npm", "start"]) # runs forever or untill it crashes
        # previous plan was to attempt restart of z2m but it seems 
        # only a reboot fixes things, a very brut force solution
        # This will be changed when the z2m problem is figured out
        logger.warning("exited, attempting restart")
        print("zigbee2mqtt exited, attempting restart")
        watch_dog_queue.put(["shutdown", "zigbee2mqtt problems"])
        time.sleep(10) # just to keep it out of a hard loop        

if __name__ == "__main__":
    task()
