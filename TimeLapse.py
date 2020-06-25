import time
import machine

# PWM pins: 0, 2, 4, 5, 12, 13, 14 and 15

# pin 4 -> servo 1
p1 = machine.Pin(4)
s1 = machine.PWM(p4,freq=50)

# pin 5 -> servo 2
s2 = machine.PWM(p5,freq=50)


def deep_sleep(msecs):
  # configure RTC.ALARM0 to be able to wake the device
  rtc = machine.RTC()
  rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

  # set RTC.ALARM0 to fire after X milliseconds (waking the device)
  rtc.alarm(rtc.ALARM0, msecs)

  # put the device to sleep
  machine.deepsleep()

def capture():
  # duty for servo is between 40 - 115
  s1.duty(100)
  s2.duty(100)
  time.sleep(1)
  s1.duty(60)
  s2.duty(60)


deep_sleep(1800000)  # milisecs
capture()


"""
import time
import machine
p4 = machine.Pin(4)
p5 = machine.Pin(5)
s1 = machine.PWM(p4,freq=50)
s2 = machine.PWM(p5,freq=50)
# duty for servo is between 40 - 115

s1.duty(80)
time.sleep(0.5)
s1.duty(52)
time.sleep(0.5)
s1.duty(60)
time.sleep(4)
s1.duty(52)
time.sleep(0.5)
s1.duty(80)

time.sleep(3)

s2.duty(60)
time.sleep(0.5)
s2.duty(82)
time.sleep(0.5)
s2.duty(60)
time.sleep(3)
s2.duty(82)
time.sleep(0.5)
s2.duty(60)

time.sleep(3)
s1.duty(52)
time.sleep(5)
s1.duty(80)
"""
