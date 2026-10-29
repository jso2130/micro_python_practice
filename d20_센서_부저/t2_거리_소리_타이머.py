import machine                                  # machine : 보드의 부품(핀·타이머 등)을 다루는 도구 모음
import time                                     # time : 기다리거나 시간을 다루는 도구 모음
from machine import Pin, PWM, Timer             # machine 에서 부품 도구(클래스)를 가져온다 : Pin(핀), PWM(부저), Timer(타이머)

# ---- 객체 만들기 ----
buzzer = PWM(Pin(6), freq=880, duty=0)
trigger = Pin(17, mode=Pin.OUT, pull=None)
echo = Pin(1, mode=Pin.IN, pull=None)
trigger.value(0)                       # value() 메서드 : 핀 값을 정한다. 0 = 끔 (처음에는 소리를 쏘지 않는다)

# ---- 내가 바꾸는 값 ----
NEAR_CM = 5
FAR_CM = 40
LEVELS = 20
DUTY_TABLE = [10, 12, 13, 15, 18, 20, 24, 27, 31, 36, 42, 48, 55, 64, 73, 85, 98, 113, 130, 150]

# ---- 인터럽트 깃발 : 알람 ----
ms = 0
flag_10 = False
flag_50 = False
flag_500 = False

def tick(t):
    global ms, flag_10, flag_50, flag_500       
    ms += 1
    if ms % 10 == 0:
        flag_10 = True
    if ms % 50 == 0:
        flag_50 = True
    if ms % 500 == 0:
        flag_500 = True

def get_distance_cm():                          # 못 읽으면 0
    trigger.value(0)                            # value(0) : 끈 상태에서 시작
    time.sleep_us(5)                            # sleep_us() : 5 µs 기다린다 (µs = 마이크로초 = 100만분의 1초)
    trigger.value(1)                            # value(1) : 켠다 = 초음파를 쏘기 시작
    time.sleep_us(10)                           # 10 µs 동안 켜 둔다
    trigger.value(0)                            # value(0) : 끈다 = 쏘기를 끝낸다
    
    # 6000 µs 의 왕복할 수 있는 거리는 약 100 cm. 이보다 멀리 있거나 장애물이 없으면 넘어간다.
    # time_pulse_us(핀, 1, 최대µs) : echo 가 켜져 있던 시간(µs)을 잰다. 
    # echo 가 켜져 있던 시간(µs)으로 거리 측정
    pulse_time = machine.time_pulse_us(echo, 1, 6000)  
    distance_cm = (pulse_time / 2) / 29.1       # 왕복 시간의 절반 ÷ 29.1(소리가 1cm를 이동하는 시간) = 거리(cm)
    if 2 <= distance_cm <= 200:                 # 2cm에서 2m
        return distance_cm
    else:
        return 0

def distance_level(cm):          
    level = int((FAR_CM - cm) * LEVELS // (FAR_CM - NEAR_CM))
    if level < 0:
        level = 0
    if level > LEVELS - 1:
        level = LEVELS - 1
    return level

beep_on = False            # 지금 킨 상태인지 보는 변수
cm = 0
level = 9
duty = DUTY_TABLE[level]

tmr = Timer(0)
tmr.init(period=1, mode=Timer.PERIODIC, callback=tick)

try:
    while True:
        if flag_10:                              # 10 ms : 소리 크기를 부저에 반영한다
            flag_10 = False
            if beep_on:                          
                buzzer.duty(duty)                
            else:
                buzzer.duty(0)                   
        if flag_50:                              # 50 ms : 거리를 재서 듀티값을 설정한다.
            flag_50 = False
            cm = get_distance_cm()
            if cm != 0:                          # 0은 이전 듀티값을 그대로 유지한다.
                level = distance_level(cm)
                duty = DUTY_TABLE[level]
        if flag_500:                             # 500 ms : 소리를 켜고 끄고, 정보를 쉘에 찍는다
            flag_500 = False
            beep_on = not beep_on
            print("거리", int(cm), "cm -> 단계", level, "-> duty", duty)
except KeyboardInterrupt:                       
    pass
finally:                                        
    tmr.deinit()                               
    buzzer.duty(0)                              
    buzzer.deinit()                             