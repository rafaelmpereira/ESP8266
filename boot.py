from umqtt.simple import MQTTClient
import time
#DEFINICOES
server = "mqtt.mydevices.com"
clientid = "aa07e300-803f-11ea-883c-638d8ce4c23d" 			#insert your client ID
username = "d6033960-7df0-11ea-a67f-15e30d90bbf4" 			#insert your MQTT username
password = "99e45f8e4ef9ef46f3bc0c42e4d0317e5bb523cb" 			#insert your MQTT password
tipo = "digital"
unit = "d"
value = "1"
channel = "1"
c = MQTTClient(clientid,server,0,username,password)
c.connect()

def pub():
  topic = ("v1/%s/things/%s" % (username, clientid))
  #topic = ("v1/%s/things/%s/%s" % (username, clientid, channel))
  data = ("%s,%s=%s/%s" % (tipo, unit, value, channel))
  #data = ("%s,%s=%s" % (tipo, unit, value))
  c.publish(topic,data)
  print("Enviado. ")
  #c.disconnect()
  
  for i in range(5):
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
