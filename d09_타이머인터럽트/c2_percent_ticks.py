from machine import Pin
import time

flash = Pin(4, Pin.OUT, value=0)
red = Pin(33, Pin.OUT, value=1)

counter = 0        
time_cnt = 0      # 시간을 잴 변수
red_on = 0

def timer_10ms():
    return

def timer_100ms():                  # 100ms마다 flash.value 바뀜(켜지고 꺼짐)
    flash.value(not flash.value())

def timer_500ms():                   # 500ms마다 red.value 바뀜(켜지고 꺼짐)
    red.value(not red.value())


while True:
    time.sleep_ms(1)      # 1ms 동안 대기
    time_cnt += 1         # 시간을 잰다

    if time_cnt % 100 == 0:    
        timer_100ms()

    if time_cnt % 500 == 0:
        timer_500ms()
