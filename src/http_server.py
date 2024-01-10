from gevent import monkey; monkey.patch_all()
from flask import Flask, Response, render_template_string, stream_with_context, request
from gevent.pywsgi import WSGIServer
import os
import database
import load_zigbee_data
import fauxmo_manager
import const
import message
import threading
#import multiprocessing
from queue import Empty
import time
import index_html

import logging
logger = None

app = Flask(__name__)
shared=[]
q=True
btc=None
db=None
#p= None
db_values=None
fauxmo_task = None
mqtt_queue = None
watch_dog_queue = None


##############################
@app.route("/")
def render_index():
    logger.info("getting index.html")
    return render("")  

@app.route("/whoareyou")
def whoareyou():
    myhost = os.uname()[1]
    logger.info("host name ", myhost)
    return "iam/"+myhost

@app.route("/password", methods =["GET", "POST"])
def create_password():
    if request.method == "POST":
        pw = request.form["password"]
        db.replace_password(pw)

@app.route("/create_wemo", methods =["GET", "POST"])
def create_wemo():
    error_msg = ''
    logger.info("entering create_wemo[%s]" % (request.method,))
    global fauxmo_task
    global db
    global watch_dog_queue
    if request.method == "POST":
        logger.info("got post")
        action = request.form["action"]
        logger.info("action[%s]" % action)
        if action == "restart":
            fauxmo_manager.stop_fauxmo_task(fauxmo_task)
            # to keep watchdog happy, let it know about the change
            watch_dog_queue.put(["startfauxmotask", "start"])
        else:
            if "wemo_name" in request.form and "wemo_device" in request.form:
                logger.info("create_wemo  form[%s]" % request.form)
                port = request.form["wemo_port"]
                logger.info("create_wemo  port[%s]" % port)
                name = request.form["wemo_name"]
                device = request.form["wemo_device"]
                if port in ("Optional", None):
                    port = None 
                logger.info("CREATE_WEMO name[%s] device[%s] port[%s]" % (name, device, port,))  
                status = db.create_wemo(name, port, device)  
                if (not status):
                    error_msg = "error inserting"
            else:
                error_msg = 'Both wemo name and device required, port is optional and usualy auto assigned'
    return render(error_msg) 

@app.route("/modify_wemo", methods =["GET", "POST"])
def modify_wemo():
    logger.info("modify_wemo called")
    global db
    if request.method == "POST":
        error_msg = ''
        logger.info(request.form)	
        action = request.form["action"]
        logger.info("action",action)	
        thing, rowid = request.form["action"].split("/")
        logger.info("modify_device_broker thing[%s] rowid[%s]" % (thing, rowid))
        db.delete_wemo(rowid)
    return render(error_msg)

@app.route("/all_devices", methods =["GET", "POST"])
def all_devices():
    if request.method == "POST":
        global db
        message = ""
        rowid=None
        update_IP = False
        logger.info("/all_devices action[%s]" % request.form["action"])
        parts = request.form["action"].split("/")
        logger.info("/all_devices action part 0 [%s]" % parts[0])
        if parts[0] == "send":
            send_mqtt_publish(parts[2], parts[1])
        elif parts[0] == "refresh":
            load_zigbee_data.ZigbeeDeviceRefresher()
            message="ZigBee devices refreshed"
        elif parts[0] == 'delete':
            db.delete_device(parts[1])
        elif parts[0] == "manIP":
            update_IP = True
            rowid = parts[1]
    return render(message, update_ip=update_IP,manIP_rowid=rowid)

@app.route("/create_IP_device", methods =["GET", "POST"])
def create_IP_device():
    if request.method == "POST":
        global db
        error=''
        name = request.form["IP_name"]
        desc = request.form["IP_description"]
        logger.info("create_IP_device", name, desc)
        if name and desc:
            db.create_device_by_name(desc, None, name, "manIP")
        else:
            error = "Both name and description needed"  
    return render(error)   

@app.route("/create_IP_feature", methods =["GET", "POST"])
def create_IP_feature():
    if request.method == "POST":
        global db
        logger.info(
        request.form["property"],
        request.form["device_ieee_address"])
        db.update_feature(
            request.form["device_ieee_address"] ,
            request.form["property"],
            None, 
            "binary",
            0, 
            None,
            None,
            None,  
            'on',  
            'off',
            None)		  
    return render("")  

@app.route("/update_IP", methods =["GET", "POST"])
def update_IP( ):
    global db
    if request.method == "POST":
        parts = request.form["action"].split("/")
        cmd = parts[0]
        if cmd == "Update":
            db.update_manIP_feature(  
                request.form["type"],
                request.form["set_topic"],
                request.form["on"],  
                request.form["off"],
                request.form["get_topic"],
                request.form["empty"],
                request.form["pub_topic"], 
                parts[1], 
                )
    return render("")  
        
def render(error, update_ip=False, manIP_rowid=None):
    logger.info("http_server.render called")
    return render_template_string(index_html.html, 
        error_message = error,
        do_update_IP = update_ip,
        man_ip = db.get_manIP_device(manIP_rowid),
        manIP_devices =  db.cook_devices_features_for_html(source='manIP'),
        autoIP_devices = db.cook_devices_features_for_html(source='autoIP'),
        zigbee_devices = db.cook_devices_features_for_html(source='zigbee'),
        get_devices_for_wemo = db.get_devices_for_wemo(),
        all_wemo = db.get_all_wemo(),
        manual_device_names = db.get_all_manual_device_names()
        ) 

def send_mqtt_publish(feature_rowid, true_or_false):
    logger.info("send_mqtt_publish rowid[%s] [%s]" % (feature_rowid, true_or_false))
    (access, 
    set_topic, 
    get_topic,
    pub_topic, 
    true_value, 
    false_value, 
    empty_value) = db.get_feature_mqtt(feature_rowid)
    if true_or_false ==  "1":
        payload = true_value
    else:
        payload = false_value
    message.publish_single(set_topic,payload)
    #mqtt_queue.put(("subscribe", pub_topic, None))
    #mqtt_queue.put(("publish", set_topic, payload))

def mqtt_task(mqtt_queue):
    logger.info("http_server.mqtt_task starting", type(mqtt_queue))
    m=message.message(mqtt_queue, client="HTTP_server")
    while True:
        try:
            item = mqtt_queue.get(timeout=const.mqtt_keepalive)
        except Empty:
            logger.info("http_server.mqtt_task mqtt_queue timed out")
            continue
        cmd = item[0]
        logger.info("http_server.mqtt_task dequeued", item)
        if cmd == "subscribe":
            m.subscribe(item[1])
        elif cmd == "publish":
            logger.info("http_server.mqtt_task publishing[%s][%s]" % (item[1], item[2]))
            m.publish(item[1], item[2])

def start_http_task(fauxmo, q, watch_dog_queue):
    http_thread = threading.Thread(target=task, args=[fauxmo, q, watch_dog_queue])
    http_thread.start()
    return http_thread

def stop_http_task(p):
    p.terminate()
    while p.is_alive():
        logger.info("http wont die")
        time.sleep(0.1)
    p.join()
    p.close()

def task(fauxmo, mqtt_queue_in, watch_dog_queue_in):
    global logger
    logger = logging.getLogger(const.log(__file__))
    global fauxmo_task
    global db
    global p
    global mqtt_queue
    global watch_dog_queue
    watch_dog_queue = watch_dog_queue_in
    mqtt_queue = mqtt_queue_in
    fauxmo_task = fauxmo
    db=database.database()
    logger.info("Starting http server")
    http_server = WSGIServer(("0.0.0.0", const.http_port), app)
    logger.info("Starting http server serve_forever")
    http_server.serve_forever()
    logger.info("http_server.serve_forever we should not get here")

# unit test
if __name__ == "__main__":
    from queue import Queue
    q =Queue()
    http_thread = None
    while True:
        if not http_thread or not http_thread.is_alive():
            http_thread = start_http_task("fauxmo", q)
            logger.info("watchdog http_thread needs to be started")
        else:
            pass
        #logger.info("watchdog http_thread running")
        time.sleep(10)
