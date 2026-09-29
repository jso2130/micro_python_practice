from machine import Pin
import time


# Pin 33번은 value 1이 off이다.
flash = Pin(33, Pin.OUT, value = 1)

# row함수를 알아보기 쉽게 변수로 만들면 코드의 가독성을 높일 수 있다.
# 하드웨어 값이니까 대문자로 작
ON = False
OFF = True

def s(times,ms):
    for i in range(times):
        flash.value(ON)
        time.sleep_ms(ms)
        flash.value(OFF)
        time.sleep_ms(ms)
        
def o(times,ms_on,ms_off):
    for i in range(times):
        flash.value(ON)
        time.sleep_ms(ms_on)
        flash.value(OFF)
        time.sleep_ms(ms_off)

# 함수를 담은 함수
def blink_count(count):
    for x in range(count):
        s(3,100)
        time.sleep_ms(100)
        o(3,900,100)
        time.sleep_ms(100)
        s(3,100)
        time.sleep_ms(100)

# SOS 사인 3번 반복
blink_count(3)
