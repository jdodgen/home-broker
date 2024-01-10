import message 
import database
import json
import time
import queue

import logging
logger = logging.getLogger(__name__)

def pt(v):
    print ("(PT: [%s] %s]" % (v,type(v)))
class ZigbeeDeviceRefresher():
    def __init__(self):
        self.db = database.database()
        q = queue.Queue()
        self.msg = message.message(q)
        self.topic = "zigbee2mqtt/bridge/devices"
        self.msg.client.subscribe(self.topic, 0)
        while True:
            try:
                item = q.get(timeout=20)
            except queue.Empty:
                print("ZigbeeDeviceRefresher empty sleeping")
                time.sleep(1)
                continue
            if item is None:
                print("ZigbeeDeviceRefresher: no reply from ", self.topic)
                break
            print("item[0] [%s]" % item[0])
            if item[0] == "callback":
                if item[1] == self.topic: # reply topic
                    load_database_from_zigbee(item[2])
                    break

def load_database_from_zigbee(zigbee2mqtt_devices):
    db = database.database()
    source = "zigbee"
    db.clean_devices(source)
    devices =json.loads(zigbee2mqtt_devices)
    for d in devices:
        #logger.info(d.keys())
        device_type=d["type"]
        # print("device_type[%s]" % (device_type,))
        #logger.info("device_type[%s]" % (device_type,))
        if device_type == "Coordinator":
            continue  # ignore for now
        #logger.info("we care about [%s]" % device_type)
        definition= d["definition"]
        address=d["ieee_address"]
        name = d["friendly_name"]
        #logger.info("definition[%s]" % type(definition))
        if definition == "None":
            continue
        #logger.info("definition", definition)
        description = definition["description"]   
        #logger.info("description[%s]  ieee[%s] friendly[%s]" % (description, address, name))
        rc = db.create_device(description, address, name, source)
        #print("load_database_from_zigbee rc", rc)
        exposes = definition["exposes"]
        
        for e in exposes:
            #logger.info("exposes:", e) 
            if 'features' in e:
                e = e['features'][0] # not sure why 'features' wraps this, so process as normal
            access = e["access"]
            if e.get('description') == None:
                desc=None
            else:
                desc = e["description"]
                del e["description"]
            property = e["property"]
            type= e["type"]
            #  now create the topics
            true_value = None
            false_value = None
            set_topic = None
            get_topic = None
            pub_topic = None

            can_published, can_set, can_get = parse_access_flags(access)
            if can_set:
                set_topic = "zigbee2mqtt/%s/set" %  (name)
            if can_get:
                get_topic = "zigbee2mqtt/%s/get" %  (name)
            if can_published:
                pub_topic = "zigbee2mqtt/%s" % name
            if type == 'binary':
                true_value = '{"%s": "%s"}' % (property, e["value_on"])
                false_value = '{"%s": "%s"}' % (property, e["value_off"])
            elif type == 'enum':
                true_value = '{"%s": "%s"}' % (property, "on")
                false_value = '{"%s": "%s"}' % (property, "off")
            empty_value = '{"%s": ""}' % (property)
                
            db.update_feature(address, 
                            property,  
                            desc,
                            type,
                            access,
                            set_topic,
			                get_topic,
			                pub_topic,   
			                true_value,
			                false_value,
                            empty_value)

def parse_access_flags(access):
    published = True if (access & 1) else False
    set         = True if (access & 2) else False
    get         = True if (access & 4) else False
    return (published, set, get)

if __name__ == "__main__":
    d=ZigbeeDeviceRefresher()
    time.sleep(5)