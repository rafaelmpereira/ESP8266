import time
import machine

s1 = machine.PWM(machine.Pin(4),freq=50)
s2 = machine.PWM(machine.Pin(5),freq=50)

def deep_sleep(msecs):      # MUST connect RST to D4 (GPIO16 - WAKE)
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
  
  # Capturing photo
  s2.duty(60)
  time.sleep(0.5)
  s2.duty(82)
  time.sleep(0.5)
  s2.duty(60)
  time.sleep(3)
  s2.duty(82)
  time.sleep(0.5)
  s2.duty(60)
  time.sleep(5)
  
  # turning camera off
  s1.duty(52)
  time.sleep(5)
  s1.duty(80)

deep_sleep(1800000)  # milisecs
capture()

