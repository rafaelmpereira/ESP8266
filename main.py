# https://www.hackster.io/hendra/connect-mydevice-cayenne-using-micropython-with-ds18b20-c89f5d
# Hendra Kusumah

from umqtt.simple import MQTTClient
from machine import Pin
import network
import time

#wifi setting
ssid="NET_2GEF16EA"             #insert your wifi ssid
password=""                     #insert your wifi password
server = "mqtt.mydevices.com"
clientid = "" 			#insert your client ID
username = "" 			#insert your MQTT username
password = "" 			#insert your MQTT password

topic = ("v1/%s/things/%s/" % (username, clientid))

def connectWifi(ssid,passwd):
  global wlan
  wlan=network.WLAN(network.STA_IF)
  wlan.active(True)
  wlan.disconnect()
  wlan.connect(ssid,passwd)
  while(wlan.ifconfig()[0]=='0.0.0.0'):
    time.sleep(1)
    
connectWifi(SSID,PASSWORD)
#server = SERVER
c = MQTTClient(clientid, server,0,username,password)
c.connect()

def senddata():
  type = "temp"
  unit = "c"
  value = 25.4
  channel = "1"
  data = ("%s,%s=%s/%s" %(type, unit, value, channel))
    
  """
  # DA BIBLIOTECA CAYENNE
  # forma de envio
  def getDataTopic(self, channel):
        """Get the data topic string.
        channel is the channel to send data to.
        """
        return "%s/%s/%s" % (self.rootTopic, DATA_TOPIC, channel)
  
  # forma de envio
  topic = self.getDataTopic(channel)
            if dataType:                # COM DATATYPE CONHECIDO
                payload = "%s,%s=%s" % (dataType, dataUnit, value)
            else:                       # SEM DATATYPE CONHECIDO
                payload = value
            self.mqttPublish(topic, payload)
  
  	# DO SITE CAYENNE
  	Send Sensor Data to Channel 2
	PUB v1/A1234B5678C/things/0123-4567-89AB-CDEF/data/2
	temp,c=20.7
  """  
  
  c.publish(topic, data)

  time.sleep(10)
  print("temperature is: ", value)
  print("data sent")
  
  # Send data format: v1/username/things/clientID/type,unit=value/channel
  
while True:
	try:
		senddata()
	except OSError:
		pass
