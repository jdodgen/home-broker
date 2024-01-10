import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import sys
import const
import time

import logging
logger = logging.getLogger(__name__)

class message():
    def __init__(self, q=None, on_message=None, client=None):
        self.client_name = client
        self.client = mqtt.Client(self.client_name)
        self.q = q
        try:
            logger.info("message: mqtt connecting")
            self.client.connect(const.broker,keepalive=const.mqtt_keepalive) 
        except:
            logger.warning("message: MQTT could not connect", const.broker)
            # the loop will try later
        #self.client.on_message=self.on_message
        if on_message == None:
            self.client.on_message=self.on_message  # this one uses the queue
        else:
            self.client.on_message=on_message 
        #self.client.message_callback_add("zigbee2mqtt/bridge/devices", self.on_zigbee)
        self.client.on_connect=self.on_connect
        self.client.on_publish=self.on_publish
        self.client.loop_start()
        self.last_subscribe = ""
        self.last_subscribe_time = 0
    
    def on_publish(self,client,userdata,result):             #create function for callback
        logger.info("message.on_publish: result[%s]" % result)
        pass

    def on_connect(self, client, userdata, flags, rc ):
        """Subscribe to state command on connect (or reconnect)."""
        #logger.info("message: client[%s] connected" % client)
        #when reconnect existing subscribes must be re-subscribed
        if self.q != None:
             self.q.put(("connected",None,None))
    
    def on_message(self, client, userdata, message):
        payload_size = sys.getsizeof(message.payload)
        logger.info("message.on_message: callback client[%s] topic[%s] payload size[%s]" % (client, message.topic, payload_size)) 
         #logger.info("name[%s] item[%s] value[%s]" % (name, item, value))
        self.q.put(("callback", message.topic, message.payload))

    def publish(self, topic, payload, retain=False):
        ptype=type(payload)
        payload_size = sys.getsizeof(payload)
        logger.info("message.publish: topic [%s] payload [%s] payload type[%s]" % (topic, payload_size, ptype))
        if ptype is str:
            #logger.info(""message.publish: payload is string")
            rc = self.client.publish(topic, bytes(payload, 'utf-8'), retain=retain)
        else:
            rc = self.client.publish(topic, payload, retain=retain)
        #logger.info("message.publish wait_for_publish")
        #rc.wait_for_publish() 
        #logger.info("message.publish return [%s]" % rc.is_published())
    
    def subscribe(self,topic):
         t = time.time()
         #if topic == self.last_subscribe and self.last_subscribe_time < t + 2:
              #logger.info("message.subscribe duplicate, ignored", topic)
              #return False
         self.last_subscribe = topic
         self.last_subscribe_time = t
         self.client.subscribe(topic)
         logger.info("message.subscribe[%s]" % (topic,))
         return True
         
    def cook(self, s):
         return bytes(s, 'utf-8')
    
def publish_single(topic, payload):
    logger = logging.getLogger(__name__)
    rc = publish.single(topic, payload, hostname=const.broker, client_id="http_server") 
    logger.info("message.publish_single returned[%s]" % rc)

### test area ###
# import thing


if __name__ == "__main__":
    import queue
    # import thing
    q = queue.Queue() 
    msg = message(q)

    msg.publish("zigbee2mqtt/demo_wall/set", '{"state": "on"}')
    msg.publish("zigbee2mqtt/jake/set", '{"state": "on"}')
    msg.subscribe([("zigbee2mqtt/joe/#", 0),
                        ("zigbee2mqtt/jake/#", 0),
                            ("zigbee2mqtt/motion/#", 0),
                        ("zigbee2mqtt/demo_wall/#", 0)])
    while True:
        msg = q.get()
        logger.info(msg)

