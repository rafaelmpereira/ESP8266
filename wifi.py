




# CHECKING CONNECTION
import machine
import network
from time import sleep

sta_if = network.WLAN(network.STA_IF)
print(sta_if.ifconfig())

led = machine.Pin(2)
def conectar():
    sta_if = network.WLAN(network.STA_IF)
    #print(sta_if.ifconfig())
    print("Acessando...")
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('YOUR WIFI', 'YOUR PSWRD')  # wifi ssid, wifi password
        print("WIFI OK") 
        #print(sta_if.ifconfig())
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    if sta_if.isconnected() == True:
      led.value(0)
      for i in range(4):
        sleep(0.05)
        led.value(not led.value())
        sleep(0.05)
      sleep(0.5)
      led.value(1)


conectar()



