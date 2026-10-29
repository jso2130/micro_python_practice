import machine
import time
from machine import Pin

trigger = Pin(17, mode=Pin.OUT, pull=None)
echo = Pin(1, mode=Pin.IN, pull=None)
trigger.value(0)

try:
    while True:
        trigger.value(0)
        time.sleep_us(5)   # 마이크로세컨드
        trigger.value(1)
        time.sleep_us(10)
        trigger.value(0)

        pulse_time = machine.time_pulse_us(echo, 1, 30000)
        distance_cm = (pulse_time / 2) / 29.1  # 왕복이라서 2로 나눔
        if 2 <= distance_cm <= 200:            # 2cm에서 2m거리까지만 
            print(distance_cm,"cm")
        
        time.sleep(0.1)

except KeyboardInterrupt:
    pass
