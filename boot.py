from machine import Pin
from umqtt.simple import MQTTClient
import time
from wifi import conectar
from testedht import readDHT11

#                   Almir                                 Rafael                                    Stefano
clientid = ["aa07e300-803f-11ea-883c-638d8ce4c23d", "bf401e30-a656-11ea-93bf-d33a96695544", "a2c20010-a657-11ea-883c-638d8ce4c23d"]
channel = ["1","2","3"]

#DEFINICOES
server = "mqtt.mydevices.com"
clientid = "bf401e30-a656-11ea-93bf-d33a96695544"
username = "d6033960-7df0-11ea-a67f-15e30d90bbf4"
password = "99e45f8e4ef9ef46f3bc0c42e4d0317e5bb523cb"
led.value(1) # on ESP12E (not ESP32), the built in LED turns off with HIGH (and on with LOW)
rele = machine.Pin(13)
rele.value(0)
type = "temp"
unit = "c"
channel = 0
channelSub = 5
value = readDHT11()
topicPub = ("v1/%s/things/%s/data/%s" % (username, clientid, channel))
topicSub = ("v1/%s/things/%s/cmd/%s" % (username, clientid, channelSub))

#conectar() #wifi
c.disconnect()  #if previously connected
c = MQTTClient(clientid,server,0,username,password)
c.connect()

# sending data to channel
def pub():
  message = ("%s,%s=%s" %(type,unit,value))
  c.publish(topicPub,message)
  print("Enviado.", value)
  led.value(not led.value())
  sleep(0.2)
  led.value(not led.value())
  
# receiving data from channel
def sub():
  def sub_cb(topic, msg):
    p = msg.decode().split(',')
    print('Recebido: ',p[1])
    c.publish("v1/%s/things/%s/digital/%s" % (username, clientid, channelSub),"%s" %(p[1])) #sending status
    c.publish("v1/%s/things/%s/response" % (username, clientid),"ok,%s" %(p[0])) #sending actuator is ok
    # code to act on relay
    if str(p[1]) = "1":
      if int(value) >= 30:
        #turn relay ON
        rele.value(1)
      else:
        rele.value(0)
  c.set_callback(sub_cb)
  c.subscribe(topicSub)

while True:
  sub()
  sleep(0.1)
  pub()
  sleep(2)

