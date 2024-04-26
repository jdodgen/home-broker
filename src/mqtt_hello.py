import uuid

xprint = print # copy print
def print(*args, **kwargs): # replace print
    return
    xprint("[mqtt_hello]", *args, **kwargs) # the copied real print    


base_topic = "home/"
hello_request_topic = base_topic+"send_hello" # servers like home-broker publish this to get things to send a "hello"
hello_subscribe_pattern = base_topic+"+/hello" # this is a subscribe to capture IP device configs

head = '''{
"name": "%s", 
"desc": "%s",
"features": 
[
'''

tail = ''']
}'''

id = hex(uuid.getnode())  # not used currently
print("id[%s]" % (id,))

class hello:
    def __init__(self, name, desc):
        self.pl = head % (name, desc)
    
    def add_feature(self, feature):
        self.pl += feature
        self.pl += "\n,"

    def payload(self):
        return self.pl[:-1]+tail  # eat the trailing comma
    
    def topic(self):
        id = hex(uuid.getnode())
        return base_topic+id[2:]+"/hello"
    
async def send_hello(client, name, desc, *features):
    h = hello(name, desc)
    for f in features:
        h.add_feature(f)
    h.payload()
    topic=h.topic()
    payload = h.payload()
    print("[topic[%s] payload\n%s\n" % (topic, payload))
    await client.publish(topic, payload) 
    
if __name__ == "__main__":

    send_hello(None,"Alarm_button", "visual and audio notifier with push button", "{foo1}", "{foo2}")
    
    # h = hello(None,"Alarm_button", "visual and audio notifier with push button")
    # h.add_feature(alert.feature_json())
    # h.add_feature(butt.feature_json())
    # print(h.payload())
    # print("hello topic[%s]" % (h.topic(),))

