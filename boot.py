
from machine import Pin
from umqtt.simple import MQTTClient
import time
from wifi import conectar
from testedht import readDHT11

#DEFINICOES
server = "mqtt.mydevices.com"
clientid = "aa07e300-803f-11ea-883c-638d8ce4c23d" 			#insert your client ID
username = "d6033960-7df0-11ea-a67f-15e30d90bbf4" 			#insert your MQTT username
password = "99e45f8e4ef9ef46f3bc0c42e4d0317e5bb523cb" 			#insert your MQTT password
led.value(1) # on ESP12E (RAFAEL), the built in LED turns off with HIGH (and on with LOW)
type = "temp"
unit = "c"
channel = 0
conectar()

c = MQTTClient(clientid,server,0,username,password)
c.connect()

# sending data to channel
def pub():
  value = readDHT11()
  topic = ("v1/%s/things/%s/data/%s" % (username, clientid, channel))
  message = ("%s,%s=%s" %(type,unit,value))
  c.publish(topic,message)
  print("Enviado.")
  led.value(not led.value())
  sleep(0.2)
  led.value(not led.value())
  sleep(5)
  #c.disconnect()
  
channelSub = 5 # relay channel
topicSub = ("v1/%s/things/%s/cmd/%s" % (username, clientid, channelSub))
#            v1/username/things/clientid/cmd/channel
# receiving data from channel

def sub():
  def sub_cb(topic, msg):
    print((topic, msg))
    #if conditions to act with command
  
  c.set_callback(sub_cb)
  c.subscribe("%s" % (topicSub))
  #c.subscribe(b"%s" % (topicSub))
    
    
"""
# Example:
def sub_cb(topic, msg):
  print((topic, msg))

def main(server="localhost"):
  c = MQTTClient("umqtt_client", server)
  c.set_callback(sub_cb)
  c.connect()
  c.subscribe(b"foo_topic")
"""
while True:
  try:
    #pub()
    sub()
    time.sleep(1)
  except OSError:
    pass

