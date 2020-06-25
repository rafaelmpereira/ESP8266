

from machine import Pin
import machine
import time

s1 = machine.PWM(machine.Pin(4),freq=50)
s2 = machine.PWM(machine.Pin(5),freq=50)
led = machine.Pin(2,Pin.OUT)

# LED
for i in range(4):
  led.value(not led.value())
  time.sleep(0.1)
led.value(1)

def deep_sleep(msecs):      # MUST connect RST to D0 (GPIO16 - WAKE)
  # configure RTC.ALARM0 to be able to wake the device
  rtc = machine.RTC()
  rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

  # set RTC.ALARM0 to fire after X milliseconds (waking the device)
  rtc.alarm(rtc.ALARM0, msecs)

  # put the device to sleep
  machine.deepsleep()

# duty for servo is between 40 - 115
def capture():
  # Turning camera on
  s1.duty(80)
  time.sleep(0.5)
  s1.duty(52)
  time.sleep(0.5)
  s1.duty(60)
  time.sleep(4)
  s1.duty(52)
  time.sleep(0.5)
  s1.duty(80)
  time.sleep(1)
  
  # Capturing photo
  s2.duty(60)
  time.sleep(0.5)
  s2.duty(82)
  time.sleep(0.5)
  s2.duty(60)
  time.sleep(5)
  
  # Turning camera off
  s1.duty(52)
  time.sleep(2.5)
  s1.duty(80)


print('capturando')
capture()
print('sleep para comandos')
time.sleep(3)
for i in range(2):
  led.value(not led.value())
  time.sleep(0.1)
led.value(1)
print('indo dormir')
deep_sleep(5*60000)  # milisecs
# 30 s      ->     30 000 ms
# 60 s      ->     60 000 ms
# 30 min    ->  1 800 000 ms

