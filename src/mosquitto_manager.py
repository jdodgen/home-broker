# mosquitto_manager
# a subroutine library to support mosquitto
# currently this does nothing just a task that sleeps in a loop
# future mods should more management
# For now it just forces mosquitto to reload config
# see cfg below to change
#
import os, signal
import time
import const
from  pgrep import pgrep
import multiprocessing
import logging
logger = None


# edit this as needed, 
cfg = """
# created by mosquitto_manager.py
# go there to make changes and reboot
allow_anonymous true
listener 1883
log_dest none
"""

def start_mosquitto_task():
    p = multiprocessing.Process(target=task)
    p.start()
    return p

def is_mosquitto_alive():
    result = pgrep("mosquitto")
    if not result:
        print("mosquitto not running")
        return None
    else:
        return result[0]

def reload_config():
    mos_config = open(const.mosquitto_file_path, "w")
    n = mos_config.write(cfg)
    mos_config.close()
    pid = is_mosquitto_alive()
    if not pid:
        return False
    print("mosquitto pid[%s]" % (pid,))
    os.kill(pid, signal.SIGHUP)   # tells mosquitto to reload config
    return True

def task():
    global logger
    # this allows us to control mosquitto
    # If sleeping a reboot was expected to refresh mosquitto
    # if a wake then we are now trying to start and stop mosquitto
    result = reload_config()
    logger = logging.getLogger(const.log(__file__))
    if not result:
        logger.warning("reload_config detected mosquitto is not running")
    while True:
        #subprocess.run(["/usr/sbin/mosquitto", "-c", const.mosquitto_file_path,]) # '-v'])
        ## never returns, I hope :)
        #logger.info("mosquitto exited, waiting and restarting")
        # future will be 
        time.sleep(const.mosquitto_sleep_seconds)   # asleep as you see Zzzzzzzz

if __name__ == "__main__":
    #reload_config()
    task()
    time.sleep(11111)
