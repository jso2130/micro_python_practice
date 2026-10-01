from machine import Pin
import time

flash = Pin(4, Pin.OUT, value=0)

speed = []
a = 6

for i in range(a):
    speed.append(a * 100 - i * 100)
print(speed)

for ms in speed:
    flash.value(1)
    time.sleep_ms(ms)
    flash.value(0)
    time.sleep_ms(ms//2)
