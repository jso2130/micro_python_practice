from machine import Pin
import time

flash = Pin(4, Pin.OUT, value=0)
red = Pin(33, Pin.OUT, value=1)

time_cnt = 0

def timer_100ms():
    flash.value(not flash.value())

def timer_500ms():
    red.value(not red.value())
    time.sleep_ms(300)             # red값을 바꾸고 300ms 쉰다. 


while True:
    time.sleep_ms(1)
    time_cnt += 1        # sleep시간을 이용해 카운트 세기

    if time_cnt % 100 == 0:
        timer_100ms()

    if time_cnt % 500 == 0:     
        timer_500ms()
