import fauxmo_manager
import mosquitto_manager
import zigbee2mqtt_manager
import mqtt_service_task
import load_zigbee_data
import const
import database
import http_server
import time
import os
from multiprocessing import Queue, active_children
from queue import Empty
import logging

if __name__ == "__main__":
    print("home-broker starting: Version[%s]" % (const.version,))
    time.sleep(1) # a pause to read above
    logger = logging.getLogger(const.log(__file__))
    mqtt_queue = Queue()
    watch_dog_queue = Queue()
    database.database() #just to get tables created if needed
    
    mosquitto_task = None
    mqtt_task = None
    fauxmo_task = None 
    zigbee_task = None 
    http_thread = None 

    # process watchdog starting now
    watch_dog_queue.put(["test_message",0])
    logger.info("entering start/watchdog loop")
    time.sleep(2)
    while True:
        # this runs once to start all proceses
        if not mosquitto_task or not mosquitto_task.is_alive():
            mosquitto_task=mosquitto_manager.start_mosquitto_task()
            logger.warning("watchdog mosquitto_task needs to be started")

        if not fauxmo_task or not fauxmo_task.is_alive():
            fauxmo_task = fauxmo_manager.start_fauxmo_task()
            logger.warning("watchdog fauxmo_task needs to be started")
        
        if not mqtt_task or not mqtt_task.is_alive():
            logger.warning("watchdog mqtt_task needs to be started")
            mqtt_task   = mqtt_service_task.start_MQTT_service_task(mqtt_queue)

        if not zigbee_task:
            zigbee_task = zigbee2mqtt_manager.start_zigbee2mqtt_task(watch_dog_queue)
            logger.warning("watchdog zigbee_task needs to be started")
            load_zigbee_data.ZigbeeDeviceRefresher()

        if not http_thread or not http_thread.is_alive():
            http_thread = http_server.start_http_task(fauxmo_task, mqtt_queue, watch_dog_queue)
            logger.warning("watchdog http_thread needs to be started")

        # now looping    
        try:
            item = watch_dog_queue.get(timeout=const.watch_dog_queue_timeout)
        except Empty : # timed out
            continue # so loop
        except Exception as e: 
            print(e)
            continue
        else:
            # got something
            logger.info(item)
            (command, oprand) = item
            print("watch_dog_queue [%s]" % (command,))
            if command == "startfauxmotask":
                # comes from http_server.py after a restart request
                fauxmo_task = None # this cause it to be started
            elif command == "shutdown":
                active = active_children()
                for child in active:
                    print("terminating")
                    child.terminate()
                os._exit(-1)
        