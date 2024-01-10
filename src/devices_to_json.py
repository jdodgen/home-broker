import json
import const
import database
import logging
logger = logging.getLogger(__name__)


def devices_to_json():
    #logger.info("eee[%s] Feature[%s]" % (ieee,feature))
    db = database.database()
    devices_dict = []
    devices = db.get_all_MQTT_devices()
    for dev in devices:
        (ieee_address, friendly_name, description, source, date) = dev
        d = {"ieee_address": ieee_address, 
            "friendly_name": friendly_name,
            "description": description,
            "source": source,
            "date": date}
        devices_dict.append(d)
    features_dict = []
    features = db.get_all_features(source="all")
    for feat in features:
        (ieee_address, 
			property,  
			description, 
			type,
			access, 
			set_topic,
			get_topic,
			pub_topic,  
			true_value,  
			false_value,
			empty_value,) = feat
        f = {"ieee_address": ieee_address, 
            "property": property,
            "description": description,
            "type": type,
            "access": access,
            "set_topic": set_topic,
            "get_topic": get_topic,
            "pub_topic": pub_topic,
            "true_value": true_value,
            "false_value": false_value,
            "empty_value": empty_value}
        features_dict.append(f)
    all = {"devices": devices_dict, "features": features_dict}
    as_json = json.dumps( all)   
    #logger.info(as_json)
    return as_json

if __name__ == "__main__":
    devices_to_json()