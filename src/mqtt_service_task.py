import message
import multiprocessing
import queue
from multiprocessing import Queue 
import devices_to_json
import load_zigbee_data
import load_IP_device_data
import sys
import zlib
import time
import const
import logging
logger = None


zigbee2mqtt_bridge_devices = "zigbee2mqtt/bridge/devices"
home_MQTTdevices_get = "home/MQTTdevices/get"
home_MQTT_devices = "home/MQTT_devices"
hello_subscribe = "home/+/hello"

persistent_subscribes = [(home_MQTTdevices_get,0),(hello_subscribe,0)];

def task(q):
    global logger
    logger = logging.getLogger(const.log(__file__))
   
    logger.info("mqtt_service_task: queue  passed in type[%s]" % type(q))
    msg = message.message(q, client="MQTT_service_task")
    msg.subscribe(persistent_subscribes)
    last_time_zigbee_refreshed = 0.0
    compressed_json = None
    while True:
        try:
            item = q.get(timeout=const.mqtt_service_q_timeout) 
        except queue.Empty:
            logger.info("mqtt_service_task: queue timed out:  empty")
            msg.subscribe(persistent_subscribes)
            continue
        except Exception as e: 
            logger.warning("mqtt_service_task unhandled exception", e)
            continue
        command = item[0]
        logger.info("mqtt_service_task: Item from queue [%s] [%s]" % (command, item[1]))
        if command == "callback":
            topic = item[1]
            payload = item[2]
            logger.info("callback topic[%s] payload[%s]" % (topic, payload,))
            if topic == zigbee2mqtt_bridge_devices:
                load_zigbee_data.load_database_from_zigbee(payload)
                raw_json = devices_to_json.devices_to_json()
                text_size = sys.getsizeof(raw_json)
                compressed_json = zlib.compress(bytes(raw_json, "utf-8"))
                compressed_size = sys.getsizeof(compressed_json)
                logger.info("mqtt_service_task: json size[%s] compressed[%s]" % (text_size, compressed_size))
                msg.publish(home_MQTT_devices, compressed_json, retain=True)
                #msg.subscribe(persistent_subscribes)
            elif topic == home_MQTTdevices_get: # refresh of devices requested
                # this causes subscribe to get the zigbee devices 
                # then then "if" above happens
                # we avoid excessive database refreshes 
                # by not refreshing the zigbee data
                now = time.time() 
                if last_time_zigbee_refreshed + const.zigbee_refresh_seconds < now: 
                    last_time_zigbee_refreshed = now
                    msg.subscribe(zigbee2mqtt_bridge_devices)  # this get the zigbee2mqtt devices
                else:
                    msg.publish(home_MQTT_devices, compressed_json, retain=True)
                    #msg.subscribe(persistent_subscribes)
            else:
                t = topic.split("/")
                home = t[0]
                address = t[1]
                hello = t[2]
                logger.info("task: home[%s] address[%s] hello{%s] payload[%s]" % (home, address, hello, payload))
                if home == "home"and hello == "hello": # refresh of devices requested
                    load_IP_device_data.load_IP_device(address, payload)
        elif command == "connected":
            logger.info("connected")
            msg.subscribe(persistent_subscribes)
        else:
            logger.info("mqtt_service_task: unknown cmd")

def start_MQTT_service_task(mqtt_queue):
    p = multiprocessing.Process(target=task, args=(mqtt_queue,))
    p.start()
    return p

def stop_MQTT_service_task(p):
    p.terminate()
    while p.is_alive():
        logger.info("MQTT wont die")
        time.sleep(0.1)
    p.join()
    p.close()

# unit test code 
if __name__ == "__main__":
    mqtt_queue = Queue()
    #task(q)
    start_MQTT_service_task(mqtt_queue)
    time.sleep(100)
