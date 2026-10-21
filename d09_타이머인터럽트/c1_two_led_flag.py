from machine import Pin
import time

flash = Pin(4, Pin.OUT, value=0)
red = Pin(33, Pin.OUT, value=1)

counter = 0                 
red_on = 0                  # 빨간불을 끄고 킬 변수

# 구간 시작
while True:
    flash.value(1)          # 플레시 키고

    if(red_on == 1):        
        red.value(0)

    time.sleep_ms(100)      

    flash.value(0)          # 플레시 끄고

    if(red_on == 1):
        red.value(1)
        red_on = 0

    time.sleep_ms(100)      

    counter += 1

    if counter > 2:         # 빨간불은 카운터가 3일 때부터 깜빡인다.
        counter = 0
        red_on = 1
