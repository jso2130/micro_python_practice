from machine import Pin
import time

flash = Pin(4, Pin.OUT, value=0)
red = Pin(33, Pin.OUT, value=1)

# counter = 0
time_cnt = 0
# red_on = 0

# def timer_10ms():
#     return

def timer_333ms():
    if time_cnt % 333 == 0:
        flash.value(0)
    if time_cnt % 333 == 1:
        flash.value(1)

def timer_500ms():
    if time_cnt % 500 == 0:
        red.value(1)
    if time_cnt % 500 == 1:
        red.value(0)
    

while True:
    time.sleep_ms(1)
    time_cnt += 1
    
    timer_333ms()
    timer_500ms()
    
