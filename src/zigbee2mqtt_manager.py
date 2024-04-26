# zigbee2mqtt_manager
# Copyright 2023 by James E Dodgen Jr.  All rights reserved.
import subprocess
import time
import multiprocessing
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

def start_zigbee2mqtt_task(watch_dog_queue):
    p = multiprocessing.Process(target=task, args=(watch_dog_queue,))
    p.start()
    return p

def stop_zigbee2mqtt_task(p):
    p.terminate()
    while p.is_alive():
        print("zigbee2mqtt wont die")
        time.sleep(0.1)
    p.join()
    p.close()

def task(watch_dog_queue):
    while True:
        # not sure why they need this but this will run it
        print_always("task starting")
        os.chdir("/opt/zigbee2mqtt")
        print(os.getcwd())
        # subprocess.run(["sudo", "systemctl", "stop", "zigbee2mqtt"])  # just incase 
        subprocess.run(["/usr/bin/npm", "start"]) # runs forever or until it crashes
        # previous plan was to attempt restart of z2m but it seems 
        # only a reboot fixes things, a very brut force solution
        # This will be changed when the z2m problem is figured out
        print("exited, attempting restart")
        watch_dog_queue.put(["shutdown", "zigbee2mqtt problems"])
        time.sleep(10) # just to keep it out of a hard loop        

if __name__ == "__main__":
    task()
