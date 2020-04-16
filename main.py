# https://www.hackster.io/hendra/connect-mydevice-cayenne-using-micropython-with-ds18b20-c89f5d
# Hendra Kusumah

from umqtt.simple import MQTTClient
from machine import Pin
import network
import time
import ds18x20
import onewire

# the device is on GPIO12
dat =Pin(12)
# create the onewire object
ds = ds18x20.DS18X20(onewire.OneWire(dat))
# scan for devices on the bus
roms = ds.scan()
print('found devices:', roms)

#wifi setting
SSID="NET_2GEF16EA" #insert your wifi ssid
PASSWORD="" #insert your wifi password

SERVER = "mqtt.mydevices.com"
CLIENT_ID = " " #insert your client ID
username=' ' #insert your MQTT username
password=' ' #insert your MQTT password
TOPIC = ("v1/%s/things/%s/data/1" % (username, CLIENT_ID))

def connectWifi(ssid,passwd):
  global wlan
  wlan=network.WLAN(network.STA_IF)
  wlan.active(True)
  wlan.disconnect()
  wlan.connect(ssid,passwd)
  while(wlan.ifconfig()[0]=='0.0.0.0'):
    time.sleep(1)
    
connectWifi(SSID,PASSWORD)
server=SERVER
c = MQTTClient(CLIENT_ID, server,0,username,password)
c.connect()

def senddata():
  ds.convert_temp()
  time.sleep_ms(100)
  temp = ds.read_temp(roms[0])
  c.publish(TOPIC, str(temp))

  time.sleep(10)
  print("temperature is: ", temp)
  print("data sent")
  
while True:
	try:
		senddata()
	except OSError:
		pass



#...................

# from BinaryBande's github
# https://community.mydevices.com/t/use-esp8266-with-micropython-and-show-sensor-values-with-cayenne/11919

# NodeMCU Pinout https://pradeepsinghblog.files.wordpress.com/2016/04/nodemcu_pins.png?w=616
# ESP8266 Micropython Tutorial https://docs.micropython.org/en/latest/esp8266/tutorial/intro.html
# MicroPython Libs https://github.com/pfalcon/micropython-lib
# MicroPython Pycharm Plugin Tutorial https://github.com/vlasovskikh/intellij-micropython

import time                      #biblioteca
import upip                      #biblioteca
import machine                   #biblioteca
import os                        #biblioteca
import networkConfig             #arquivo
#import i2c_scanner              #arquivo
#import IOConfig                 #arquivo


networkConfig.connect_wifi()
"""
# TODO: test later with list
pkgList = ["micropython-io-0.1.tar.gz", "micropython-xmltok2-0.2.tar.gz",
           "micropython-xml.etree.ElementTree-0.1.1.tar.gz", "micropython-umqtt.simple-1.3.4.tar.gz"]
"""
try:
    f = open('lib/io.py', "r")
    io_exists = True
    f.close()
    print('io.py already installed.')
except OSError:
    io_exists = False
if not io_exists:
    upip.install("micropython-io")

try:
    f = open('lib/xmltok2.py', "r")
    xmltok2_exists = True
    f.close()
    print('xmltok2.py already installed.')
except OSError:
    xmltok2_exists = False
if not xmltok2_exists:
    upip.install("micropython-xmltok2")

try:
    f = open('lib/xml/etree/ElementTree.py', "r")
    xml_exists = True
    f.close()
    print('ElementTree.py already installed.')
except OSError:
    xml_exists = False
if not xml_exists:
    upip.install("micropython-xml.etree.ElementTree")

try:
    f = open('lib/umqtt/simple.py', "r")
    xml_exists = True
    f.close()
    print('umqtt.simple.py already installed.')
except OSError:
    xml_exists = False
if not xml_exists:
    upip.install("micropython-umqtt.simple")

from webSocket import WebSocket             #biblioteca
from htu21d import HTU21D                   #arquivo


__ledOn = 'on'
__ledOff = 'off'


def main():
    # start Power LED
    # sensor = HTU21D()
    temp = sensor.get_temp()
    hum = sensor.get_hum()
    print('Temp: %s°C / Hum: %s%%' % (temp, hum))
    #adcValue = IOConfig.__adcPin.read()
    #print('adcValue: %s' % adcValue)
               
    # Sending data to Cayenne channel ([channel],[type],[unit],[value])
    networkConfig.mqtt_subscribe("1", "temp", "c", sensor.get_temp())
    networkConfig.mqtt_subscribe("2", "rel_hum", "p", sensor.get_hum())
    #networkConfig.mqtt_subscribe("3", "analog_sensor", "null", adcValue)
    # ws = WebSocket()
    # ws.set_html()
    IOConfig.setPowerLED(__ledOn)
    switchState = IOConfig.__sleepSwitch.value()
    if switchState == 1:
        time.sleep(0.5)
        machine.deepsleep()
    else:
        pass


if __name__ == '__main__':
    # configure rtc für DEEPSLEEP wake up
    #rtc = machine.RTC()
    #rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    # DEEPSLEEP 60 minutes
    #rtc.alarm(rtc.ALARM0, 3600000)
    
    # get free space
    # https://forum.micropython.org/viewtopic.php?f=16&t=2361&hilit=statvfs
    fs_stat = os.statvfs('/')
    fs_size = fs_stat[0] * fs_stat[2]
    fs_free = fs_stat[0] * fs_stat[3]
    print("File System Size {:,} - Free Space {:,}".format(fs_size, fs_free))
    #i2c_scanner.scan()
    
    # networkConfig.set_access_point()
    
    # main loop start here
    main()

