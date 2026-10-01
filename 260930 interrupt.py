<<<<<<< Updated upstream
from machine import Pin
import time

flash = Pin(4, Pin.OUT, value=0)
red = Pin(33, Pin.OUT, value=1)

counter = 0
red_on = 0

a = 2
b = 1

while a > b:              #'true'대신 '조건 결과가 true'인 것도 넣어도 됨
    flash.value(1)
    if red_on == 1:
        red.value(0)
    time.sleep_ms(100)
    
    flash.value(0)
    if red_on == 1:
        red.value(1)
        red_on = 0         # 빨간불이 1번 켜지고 나서는 초기화
    time.sleep_ms(100)
    
    counter += 1
        
    if counter > 3:        # counter가 2미만일 때마다 counter가 초기화
        counter = 0
        red_on = 1         # flash가 3번 깜빡일 때 red 1번
    
    
#   if b % 3 == 0:         # 나머지값으로 하면 counter변수가 필요없다.
#      red_on = 1          
        
=======
from machine import Pin
import time

flash = Pin(4, Pin.OUT, value=0)
red = Pin(33, Pin.OUT, value=1)

counter = 0
red_on = 0

a = 2
b = 1

while a > b:              #'true'대신 '조건 결과가 true'인 것도 넣어도 됨
    flash.value(1)
    if red_on == 1:
        red.value(0)
    time.sleep_ms(100)
    
    flash.value(0)
    if red_on == 1:
        red.value(1)
        red_on = 0         # 빨간불이 1번 켜지고 나서는 초기화
    time.sleep_ms(100)
    
    counter += 1
        
    if counter > 3:        # counter가 2미만일 때마다 counter가 초기화
        counter = 0
        red_on = 1         # flash가 3번 깜빡일 때 red 1번
    
    
#   if b % 3 == 0:         # 나머지값으로 하면 counter변수가 필요없다.
#      red_on = 1          
        
>>>>>>> Stashed changes
