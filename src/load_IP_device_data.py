import message 
import database
import json
import time
import queue
import logging
logger = logging.getLogger(__name__)
'''The access property is a 3-bit bitmask.

Bit 1: The property can be found in the published state of this device.
Bit 2: The property can be set with a /set command
Bit 3: The property can be retrieved with a /get command (when this bit is true, bit 1 will also be true)'''

def pt(v):
    print ("(PT: [%s] %s]" % (v,type(v)))

def load_IP_device(address ,payload):
    db = database.database()
    source = "autoIP"
    logger.info("address [%s]" % address) 
    device =json.loads(payload)
    name = device["name"]
    description = device["desc"]
    db.delete_device(address)
    db.create_device(description, address, name, source)
    features = device["features"]
    for f in features:
        logger.info("load_IP", f)
        type = f["type"]
        property = f["property"]
        type = f["type"]
        if f["mqtt"] == "pub":  # the device publishes this so other things can subscribe
            access = 1 
        else:
            access = 2
        tset = f["topic_set"]
        tget = f["topic_get"]
        tpub = f["pub_topic"] 
        feature_description = f["desc"] if "desc" in f else ""
        db.update_feature(  address, 
                            property,  
                            feature_description,
                            type,
                            access,
                            tset,
			                tget,
			                tpub,   
			                f["payload_on"],
			                f["payload_off"],
                            None
                            )
        
def simple_home_broker_publish(unique_device_name, desc, type, on, off):
    payload = '''{"desc": "%s", "name": "%s", "features":
			[
                {
                "type": "%s",
                "property": "state",
                "payload_off": "%s", 
                "payload_on": "%s", 
                "topic_set": "home/%s/state/set",
                "topic_get": "home/%s/state/get",
                "pub_topic": "home/%s/state"
                }
            ]
            }''' % (desc,
                    unique_device_name,
                    type,
                    off,
                    on,
                    unique_device_name,
                    unique_device_name,
                    unique_device_name,
                      )
    topic = "home/%s/hello" % (unique_device_name,)
    return topic, payload

def example_home_broker_publish():
    unique_device_name = "friendly_name"
    description = "simple on of device"
    type = "binary"
    on = "on"
    off = "off"
    topic, payload = simple_home_broker_publish(unique_device_name, description, type, on, off)
    return topic, payload

if __name__ == "__main__":
    topic, payload = example_home_broker_publish()
    device =json.loads(payload)
    print("topic [%s]" % (topic,))
    print("device [%s]" % (device,))
    ##message.publish_single(topic,payload)