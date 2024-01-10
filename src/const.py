#inside const.py constants and configurable items
version = 0.1

import os
if os.name =="nt": # testing under Windows
   db_name = 'C:\\Users\jim\devices.db'
   log_path = 'C:\\Users\\jim\\log\\'
   error_log_path = 'C:\\Users\\jim\\log\\error\\'
   #broker = "home-broker.local"
   broker = "192.168.0.193"
   mosquitto_file_path = "mosquitto.conf"
   fauxmo_default_dir = "fauxmo"
else: # running as a system under Linux
   db_name = 'devices.db'
   log_path = "/dev/shm/log/"
   error_log_path = "log/"
   broker = "home-broker.local"
   mosquitto_file_path = "/etc/mosquitto/mosquitto.conf"
   fauxmo_default_dir = "/etc/fauxmo"    

fauxmo_config_file_path = fauxmo_default_dir+"/config.json"
fauxmo_sleep_seconds = 120 # wake up every two minutes, Zzzzzz
broker_mqtt_port = 1883
base_faxmo_port = 56000
mqtt_keepalive = 120
mosquitto_sleep_seconds = 1000 # change when checking for death in future versions
MQTTPlugin = "mqttplugin.py"
zigbe2mqtt = "zigbee2mqtt"
zigbee_refresh_seconds = 30

http_port = 80
mqtt_service_q_timeout = 20
watch_dog_queue_timeout = 20
db_timeout = 120 # we have nothing that would cause a long lock
               # but a multiprocessing slowdown may need more time

# common to all and needed simple configurtion info
def log(what, root=False):
   import logging
   import logging.config
   from logging.handlers import RotatingFileHandler
   import __main__
   try:
      os.mkdir(log_path)
   except:
      pass
   try:
      os.mkdir(error_log_path)
   except:
      pass
   log_file_name = os.path.splitext(os.path.basename(what))[0]
   # logger.info(">>> passed in cooked name[%s] <<<" % (log_file_name,))
   fh = logging.handlers.RotatingFileHandler(log_path+log_file_name, maxBytes=4000, backupCount=3)
   fh.setLevel(logging.INFO)
   time_format = "%Y-%m-%d %H:%M:%S"
   fh.setFormatter(logging.Formatter('[%(asctime)s][%(levelname)-5s][%(name)s.%(funcName)s -- %(message)s', datefmt=time_format))
   er = logging.handlers.RotatingFileHandler(error_log_path+log_file_name, maxBytes=8000, backupCount=2)
   er.setLevel(logging.WARNING)
   er.setFormatter(logging.Formatter('[%(asctime)s][%(levelname)-5s][%(name)s.%(funcName)s -- %(message)s', datefmt=time_format))
   
   root = logging.getLogger()
   root.setLevel(min([fh.level,  er.level]))
   root.addHandler(fh)
   root.addHandler(er)
   return log_file_name