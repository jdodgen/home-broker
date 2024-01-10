# database.py
import sqlite3
from paho.mqtt.client import Client
import const
import os
import json
import logging
import time
from textwrap import wrap

logger = logging.getLogger(__name__)

class database:
	def __init__(self):
		self.con = sqlite3.connect(const.db_name, timeout=const.db_timeout)
		# logger.info("working directory[%s]" % os.getcwd())
		cur = self.con.cursor()
		try:  # see if  db exists
			cur.execute("select rowid from mqtt_device")
			cur.close()
		except:
			cur.close()
			self.initialize()

	def __del__(self):
		self.con.commit()
		self.con.close()

	def replace_password(self, pw):
		if pw == "":
			return False
		cur = self.con.cursor()
		status = True
		try:
			cur.execute("""
			insert or replace into password (password) values (?)""", 
				(pw,))
		except:
			status = False
		cur.close()
		self.con.commit()
		return status
	
	def get_all_MQTT_devices(self):
		cur = self.con.cursor()
		cur.execute("""
		select  
		ieee_address, 
		friendly_name, 
		description, 
		source,
		date 
		from mqtt_device 
	    """)
		all = cur.fetchall()
		#logger.info(all)
		cur.close()
		return all
	
	def get_devices_for_wemo(self):
		cur = self.con.cursor()
		cur.execute("""
		select distinct
			mqtt_feature.rowid,
			
			mqtt_device.friendly_name,  
			mqtt_device.description, 
			
			mqtt_feature.property,
			mqtt_feature.description
			
			from mqtt_feature
			join mqtt_device on mqtt_feature.ieee_address = mqtt_device.ieee_address
			where access in (2,6,7) and type = 'binary'
			order by mqtt_feature.ieee_address, mqtt_feature.access desc
	    """)
		all = cur.fetchall()
		#logger.info(all)
		cur.close()
		return all
	
	def get_fauxmo_devices(self):
		cur = self.con.cursor()
		where = ''
		cur.execute("""
		select
		 	wemo_port,
	        wemo_name,
	        mqtt_feature.set_topic,
			mqtt_feature.true_value,
		    mqtt_feature.set_topic,
			mqtt_feature.false_value,
	        qos,
	        retain
	    from wemo
	    left join mqtt_feature on wemo.ieee_address = mqtt_feature.ieee_address
	      	and mqtt_feature.property = wemo.property
		""")
		all = cur.fetchall()
		#logger.info(all)
		cur.close()
		return all
	
	def get_all_features(self, source="all"):
		cur = self.con.cursor()
		where = ''
		if source in ("manIP", "autoIP", "zigbee"):
			where = "where source = '%s'" %  (source,)
		query = """
		select
			ieee_address, 
			property,
			description, 
			type,
			access, 
			set_topic,
			get_topic,
			pub_topic,  
			true_value,  
			false_value,
			empty_value
			from mqtt_feature
			"""
		cur.execute(query)
		all = cur.fetchall()
		#logger.info(all)
		cur.close()
		return all


	def get_all_devices_features(self, source="all"):
		cur = self.con.cursor()
		where = ''
		if source in ("manIP", "autoIP", "zigbee"):
			where = "where source = '%s'" %  (source,)
		query = """
		select
			mqtt_feature.rowid,
			mqtt_device.ieee_address, 
			mqtt_device.friendly_name,  
			mqtt_device.description, 
			mqtt_device.date,
			mqtt_feature.property,
			mqtt_feature.description, 
			mqtt_feature.type,
			mqtt_feature.access, 
			mqtt_feature.set_topic,
			mqtt_feature.get_topic,
			mqtt_feature.pub_topic,  
			mqtt_feature.true_value,  
			mqtt_feature.false_value,
			mqtt_feature.empty_value
			from mqtt_device
			left join mqtt_feature on mqtt_feature.ieee_address = mqtt_device.ieee_address
			%s
			order by mqtt_feature.ieee_address, mqtt_feature.access desc
	    """ % (where,)
		#logger.info(query)
		cur.execute(query)
		all = cur.fetchall()
		#logger.info(all)
		cur.close()
		return all
	
	def cook_devices_features_for_html(self,source='all'):
		all = self.get_all_devices_features(source=source)
		last_ieee = "0"
		new_all = []
		for d in all:
			new = list(d)
			if d[1] == last_ieee:
				new[1] = ''
				new[2] = ''
				new[3] = ''
				new[4] = ''   # date
				cooked_address=""
			else:
				try:
					new[4] = time.strftime("%d %b %H:%M", time.localtime(float(new[4])))
					#'Thu, 28 Jun 2001 14:17:15 +0000
				except:
					new[4] = ''
				cooked_address = " ".join(wrap(d[1],width=9)) 
			last_ieee = d[1]
			access = d[8]
			if access in (2,6,7):
				new.append(True)
			else:
				new.append(False)
			new.append(cooked_address)
			new_all.append(tuple(new))
		return new_all
	
	def get_manIP_device(self, rowid):
		if rowid == None:
			return None
		cur = self.con.cursor()
		cur.execute("""
		select
			mqtt_feature.rowid,
			mqtt_device.ieee_address, 
			mqtt_device.friendly_name,  
			mqtt_feature.property,
			mqtt_feature.type,
			mqtt_feature.set_topic,  
			mqtt_feature.true_value,  
			mqtt_feature.false_value,
			mqtt_feature.get_topic,
			mqtt_feature.empty_value,
			mqtt_feature.pub_topic
			from mqtt_device
			left join mqtt_feature on mqtt_feature.ieee_address = mqtt_device.ieee_address
			where mqtt_feature.rowid = ?
	    """, (rowid,))
		rec = cur.fetchone()
		#logger.info(all)
		cur.close()
		return rec	
	
	def update_manIP_feature(self,   
			value_type,
			set_topic,
			true_value,  
			false_value,
			get_topic,
			empty_value,
			pub_topic, 
			rowid, 
			):
		cur=self.get_cursor()
		logger.info("database: set_topic type", type(set_topic))
		b1 = 0 if set_topic in (None, "None", "")  else 4
		b2 = 0 if get_topic in (None, "None", "")  else 2
		b3 = 0 if pub_topic in (None, "None", "")  else 1
		cur.execute("""update mqtt_feature 
			set type 	= ?,
			access		= ?, 
			set_topic 	= ?,
			get_topic 	= ?,
			pub_topic	= ?,  
			true_value	= ?,  
			false_value	= ?,
			empty_value = ?
			where rowid = ?
			""",(value_type,
				b1+b2+b3,
				set_topic,
				get_topic,
				pub_topic,
				true_value,  
				false_value, 
				empty_value,
				rowid,  
			))
		cur.close()
		self.con.commit()

	def get_wemo(self, row_id):
		cur = self.con.cursor()
		cur.execute("""
		select wemo.rowid, 
	        wemo_name,
	        wemo_port, 
			mqtt_feature.rowid,
	        mqtt_device.friendly_name,
	        mqtt_feature.property,
	        qos,
	        retain
	    from wemo
	    left join mqtt_device on mqtt_device.friendly_name = wemo.friendly_name
	    left join mqtt_feature on mqtt_device.ieee_address = mqtt_feature.ieee_address
	      	and mqtt_feature.name = wemo.feature_name
		where wemo.rowid = ?
	    	""", (row_id,))
		rec = cur.fetchone()
		cur.close()
		return rec
	
	def clean_devices(self, source):
		cur=self.get_cursor()
		try:
			cur.execute("""delete from mqtt_feature where mqtt_feature.ieee_address in
						(select mqtt_device.ieee_address from mqtt_device where source = ?)""", (source,))
			cur.execute("delete from mqtt_device where source = ?", (source,))		
		except:
			logger.info("no mqtt tables? Initilizing? ")
		cur.close()
		self.con.commit()

	def delete_device(self, address):
		print("delete_device [%s]"% (address,))
		cur=self.get_cursor()
		try:
			cur.execute("delete from mqtt_feature where ieee_address = ?", (address,))
			cur.execute("delete from mqtt_device where ieee_address = ?", (address,))		
		except:
			logger.info("problem deleteing?")
		cur.close()
		self.con.commit()

	def create_device_by_name(self, description, address, name, source):
		error = None
		now = str(time.time())
		if address == None:
			address = 0
			cur=self.get_cursor()
			cur.execute("""
			select max(ieee_address) from mqtt_device 
				where cast(ieee_address as INTEGER) > 0 
				and cast(ieee_address as INTEGER) < 500
			""")
			largest = cur.fetchone()[0]
			cur.close()
			logger.info("current largest_wemo_port[%s]" % largest)
			if 	largest == None:
				address = 1
			else:
				address = int(largest) + 1
			
		if isinstance(address, int):
			address = str(address)
		cur=self.get_cursor()
		cur.execute("""
			select friendly_name, source from mqtt_device 
				where friendly_name = ? 
				and source = ?
			""", (name, source))
		does_it_exist = cur.fetchone()
		cur.close()
		cur=self.get_cursor()
		if not does_it_exist:
			cur.execute("""insert or replace into mqtt_device 
					(description, 
					ieee_address, 
					friendly_name, 
					source,
			   		date) 
					values (?,?,?,?,?)""", 
				(description, address, name, source, now))
		else:
			error='name[%s] source[%s]' % (name, source)
		cur.close()
		self.con.commit()
		return error

	def create_device(self, description, address, name, source):
		now = str(time.time())
		cur=self.get_cursor()
		cur.execute("""insert or replace into mqtt_device 
					(description, 
					ieee_address, 
					friendly_name, 
					source,
			 		date) 
					values (?,?,?,?,?)""", 
				(description, address, name, source, now))
		cur.close()
		self.con.commit()

	'''def delete_device_only(self, rowid):
		cur=self.get_cursor()
		cur.execute("""select
				description, 
				ieee_address, 
				friendly_name
				from mqtt_device  
				where rowid = ?""", (rowid,))
		(description,ieee_address,friendly_name) = cur.fetchone()
		cur.execute("""delete from mqtt_device 
				where rowid = ?""", (rowid,))
		cur.close()
		self.con.commit()
		return description,ieee_address,friendly_name
	'''

	def decode_access(self,access):
		published = True if (access & 1) else False
		set         = True if (access & 2) else False
		get         = True if (access & 4) else False
		return (published, set, get)

	def get_cursor(self):
		#try:
		cur = self.con.cursor()
		#except:
		#	self.con = sqlite3.connect(const.db_name)
		#	cur = self.con.cursor()
		return cur
	
	def update_feature(self, 
		    ieee_address, 
			property,  
			description, 
			type,
			access, 
			set_topic,
			get_topic,
			pub_topic,  
			true_value,  
			false_value,
			empty_value
			):
		cur=self.get_cursor()
		cur.execute("""insert or replace into mqtt_feature 
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
			empty_value)
			  values (?,?,?,?,?,?,?,?,?,?,?)""", 
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
			empty_value))
		cur.close()
		self.con.commit()

	def get_feature(self, ieee, property):
		cur = self.con.cursor()
		cur.execute("""
		select 
			mqtt_device.rowid,
			mqtt_device.friendly_name,
			mqtt_device.description,
			mqtt_device.source,
			mqtt_device.ieee_address, 
			 
			mqtt_feature.rowid, 
			mqtt_feature.property,
			mqtt_feature.description,
			mqtt_feature.type, 
			mqtt_feature.access, 
			mqtt_feature.set_topic, 
			mqtt_feature.get_topic,
			mqtt_feature.pub_topic, 
			mqtt_feature.true_value, 
			mqtt_feature.false_value, 
			mqtt_feature.empty_value 
			from mqtt_feature
			join mqtt_device on mqtt_device.ieee_address = mqtt_feature.ieee_address
			where mqtt_feature.ieee_address = ? 
			AND   mqtt_feature.name = ?
	    """, (ieee, property))
		rec = cur.fetchone()
		cur.close()
		#logger.info("get_feature returned [%s]" % (rec,))
		return rec
	
	def get_feature_mqtt(self, rowid):
		cur = self.con.cursor()
		cur.execute("""
		select 
			access, 
			set_topic, 
			get_topic, 
			pub_topic,
			true_value, 
			false_value, 
			empty_value 
			from mqtt_feature
			where rowid = ?
	    """, (rowid,))
		rec = cur.fetchone()
		cur.close()
		#logger.info("get_feature returned [%s]" % (rec,))
		return rec

	def delete_wemo(self, row_id):
		cur = self.con.cursor()
		cur.execute("""
		delete from wemo where rowid = ?
		""", (row_id,))
		cur.close()
		self.con.commit()

	def create_wemo(self, name, wemo_port, device):
		if name == "":
			return False
		cur = self.con.cursor()
		if not wemo_port:
			cur.execute("""
			select COALESCE(max(wemo_port),0)
				from wemo
			""")
			largest_wemo_port = cur.fetchone()[0]
			cur.close()
			logger.info("current largest_wemo_port[%s]" % largest_wemo_port)
			if 	largest_wemo_port == 0:
				wemo_port = const.base_faxmo_port
			else:
				wemo_port = int(largest_wemo_port) + 1
			cur = self.con.cursor()
		status = True
		try:
			cur.execute("""
			insert or replace into wemo (
			   wemo_name, 
			   wemo_port, 
			   ieee_address,
			   property
			   ) 
				select 
				?,
				?,
				mqtt_device.ieee_address, 
				mqtt_feature.property
				from mqtt_feature
				join  mqtt_device on mqtt_device.ieee_address = mqtt_feature.ieee_address
				where mqtt_feature.rowid = ? """, (name,  wemo_port, device))
		except Exception as e:
			logger.info("create_wemo failed,", e)
			status = False
		cur.close()
		self.con.commit()
		return status

	def get_all_wemo(self):
		cur = self.con.cursor()
		cur.execute("""
		select  
				wemo.rowid,
				wemo_name,
				wemo_port,
				mqtt_device.friendly_name,
				mqtt_feature.property, 
				mqtt_feature.set_topic,
				mqtt_feature.true_value,
				mqtt_feature.false_value
			from wemo
			left join mqtt_device on mqtt_device.ieee_address = wemo.ieee_address 
			left join mqtt_feature on mqtt_device.ieee_address = mqtt_feature.ieee_address
	      			and mqtt_feature.property = wemo.property
			order by wemo_name;
	    """)
		all = cur.fetchall()
		cur.close()
		return all

	def get_all_manual_device_names(self):
		cur = self.con.cursor()
		cur.execute("""
		select  mqtt_device.ieee_address, 
			mqtt_device.friendly_name,
	        mqtt_device.description
			from mqtt_device
			where mqtt_device.source = "manIP"
			order by mqtt_device.friendly_name
	    """)
		all = cur.fetchall()
		cur.close()
		#for e in all:
		#	logger.info(e)
		return all
	
	def initialize(self):
		create="""
		drop table if exists wemo;
		create table wemo
		(
			wemo_name unique,
		 	wemo_port unique,
			ieee_address,
			property,
			qos default 0,
		    retain default 0,
			PRIMARY KEY (wemo_name, wemo_port)
		);
		drop table if exists mqtt_device;
		create table mqtt_device
		(
			ieee_address text, 
			friendly_name,
			description,
			source, -- "zigbee" or "wifi/IP" others in future
					-- name is friendler than IEEE
					-- zigbee2mqtt requires unique names
					-- so  name + source must be unique
			date, 
			PRIMARY KEY (friendly_name, source)
		);

		-- one or more features to each device
		drop table if exists mqtt_feature;
		create table mqtt_feature
		(
			ieee_address text, 
			property,  -- unique within a device same as zigbee name
			description, 
			type, -- like binary, lots of others things like battery etc.
			access,   -- bit field   1 is pib_topic, 4 is 
			set_topic,
			get_topic,
			pub_topic,   -- a lot of devices only do this, subscribe to this
			true_value,   -- usualy the "on" value or result from a pub only device
			false_value,   -- off value 
			empty_value,
	    	PRIMARY KEY (ieee_address, property)
	    );
		"""
		# this is a dummy device mostly for testing
		self.con.executescript(create)
		self.create_device("Example", "1", "test", "manIP")
		self.update_feature("1",
		      		"state",
					"relay1",
					"binary", 
					7, 
					"/home/dodod/set", 
					"/home/dodod/get", 
					"/home/dodod/status", 
					"ON",
					"OFF",
					None )
		self.con.commit()

	def void_make_wifi_tail(self,off, on, set,get, get_payload):
		tail =	"""{"payload_off": "%s", 
					"payload_on": "%s", 
					"topic_set": "%s",
					"topic_get": "%s",
					"get_payload": "%s", 
					}""" %  (off, on, set, get, get_payload)
		try:
			work = json.loads(tail)
		except:
			work ='{"error": "not valid json"}'
			logger.info("did not like work")
		#logger.info("work", work)
		new_tail = json.dumps(work)
		
		return new_tail

	
# test stuff  
if __name__ == "__main__":
	db=database()
	print(db.cook_devices_features_for_html())
	#logger.info(db.delete_device(13))
	#db.update_device("no addr test", None, "noaddr", "test")
	#db.get_all_manual_devices()
	#logger.info("database  opened")
	#js =db.make_wifi_tail("OFF","ON", "/dodod/set","/dodod/get")
	#logger.info(js)
	#logger.info("initialize?")
	#input()
	#db.initialize()
	# db.create_device("hot")
	# db=database()
	# db.create_device("water")
	# db.create_broker([server1])
	# row = [0,"server", "server.local","", "", "" ]
	# db.update_broker(row)
	# row = [0,"another server", "server.local","", "", "" ]
	# db.update_broker(row)
	# brokers = db.get_all_brokers()
	# print (brokers)

	# """rowid,device_name, topic, payload_on, payload_off,payload_state,
	# 		broker_name, client_id """
	
	# row=[0,"water","valve","on","off","","server",""]
	# db.update_device(row)
	# row=[0,"hot","pump","on","off","","server",""]
	# db.update_device(row)
	# devices = db.get_all_devices()	
	# for row in devices:
	# 	logger.info(row)
	# 	#for col in row:
	# 		#logger.info(col)
	# row = db.get_device(4)

	# if row == None:
	# 	logger.info("not found")
	# logger.info(row)
	# d = db.get_fauxmo_devices()
	# logger.info(d)




	
