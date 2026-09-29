from machine import Pin
import time

flash = Pin(4, Pin.OUT, value=0)
patterns = [50, 50, 50, 100, 100, 300, 50, 50, 50]

#flash.value(1)
#time.sleep_ms(patterns[2])
#flash.value(0)
#print("켠 시간:", patterns[2])

#for ms in patterns:
#    print("이번 곡:", ms)
#    flash.value(1)
#    time.sleep_ms(ms)
#    flash.value(0)
#    time.sleep_ms(200)
    
#print("끝")