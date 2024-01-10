# client test program to retreve zigbee22mqtt devices jason and display it
import message # from home-broker
import zlib
import queue
import json

# publish this to CAUSE a refresh of the device data
get_publish = "home/MQTTdevices/get"
publish_payload = '{"db": "True"}'

# this will result in a calLback with the device data
subscribe = "home/MQTT_devices"

# sample process fetching all devices with MQTT pub/sub strings
# as well as other device information
# is using tools devloped for home-broker
def task():
    q = queue.Queue()
    msg = message.message(q) # "callback" as well as other maessages are 
                            # forwarded via  Queue messages
    # This just loops sending requests and getting stuff back
    # when the queue times out it sends the set of pub/sub
    # It is ued to load test home-broker
    while True:
        try:
            item = q.get(timeout=5) 
        except queue.Empty:
            #imed out so now get devices
            msg.publish(get_publish, publish_payload)
            msg.subscribe(subscribe)
            continue  
        except:  # not sure anything is left
            continue
        command = item[0]
        print("Item from queue cmd[%s]" % command)
        if command == "callback":
            topic = item[1]
            payload = item[2]
            print("Item from queue topic[%s] payload[%s]" % (topic, payload,))
            if topic == subscribe: # reply topic   
                devices(zlib.decompress(payload))
                pass
        elif command == "connected":
            msg.publish(get_publish, publish_payload)
            msg.subscribe(subscribe)

# simple device dump
# # designed to load/update two tables
# a devices table and a features table
# a device has 1 or more features.
# Each feature contains the proper pub/sub strings
# no status information is included or ever will be.  
def devices(jason_bytes):
    dev= json.loads(jason_bytes)
    all_devices = dev["devices"]
    for d in all_devices:
        print(d)
    all_features = dev["features"]
    for f in all_features:
        print(f)

if __name__ == "__main__":
    task()
