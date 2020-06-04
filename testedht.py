



import dht
from machine import Pin
from time import sleep

d = dht.DHT11(Pin(13))
led = Pin(2, Pin.OUT)
led.value(1) # NO ESP12E (RAFAEL) O LED FICA DESLIGADO EM SINAL ALTO

def readDHT11():
  d.measure()
  led.value(not led.value())
  sleep(0.2)
  led.value(not led.value())
  dt = d.temperature()
  print("Temperatura: "+ str(dt))
  return dt

#readDHT11()




