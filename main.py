from umqtt.simple import MQTTClient
import time

from wifi import conectar
#DEFINICOES
server = "mqtt.mydevices.com"
clientid = "aa07e300-803f-11ea-883c-638d8ce4c23d" 			#insert your client ID
username = "d6033960-7df0-11ea-a67f-15e30d90bbf4" 			#insert your MQTT username
password = "99e45f8e4ef9ef46f3bc0c42e4d0317e5bb523cb" 			#insert your MQTT password
type = "analog_sensor"
#type = "temp"
unit = ""
#unit = "c"
value = 0
#value = 5.0
channel = 0
c = MQTTClient(clientid,server,0,username,password)
c.connect()

def pub():
  topic = ("v1/%s/things/%s/data/%s" % (username,clientid, channel))
  message = ("%s,%s=%s" %(type,unit,value))
  c.publish(topic,message)
  
  print("Enviado: "+ str(value))
  #c.disconnect()
  
for i in range(2):
  value += 5
  pub()
  time.sleep(1)
"""
while True:
	try:
    pub()
    time.sleep(1)
	except OSError:
		pass
"""

