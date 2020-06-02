
from machine import Pin
from umqtt.simple import MQTTClient
import time
from wifi import conectar
from testedht import readDHT11

#DEFINICOES
server = "mqtt.mydevices.com"
clientid = "0000000" 			#insert your client ID
username = "0000000" 			#insert your MQTT username
password = "00000000000" 			#insert your MQTT password
led.value(1) # on ESP12E (RAFAEL), the built in LED turns off with HIGH (and on with LOW)
type = "temp"
unit = "c"
channel = 0
conectar()

c = MQTTClient(clientid,server,0,username,password)
c.connect()

def pub():
  value = readDHT11()
  topic = ("v1/%s/things/%s/data/%s" % (username,clientid, channel))
  message = ("%s,%s=%s" %(type,unit,value))
  c.publish(topic,message)
  print("Enviado.")
  led.value(not led.value())
  sleep(0.2)
  led.value(not led.value())
  sleep(5)
  #c.disconnect()

while True:
  try:
    pub()
    time.sleep(1)
  except OSError:
      pass

