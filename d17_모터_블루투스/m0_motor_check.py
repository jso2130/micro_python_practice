from machine import Pin, PWM
import time

# 교재 2-4 와 같은 방법: 모터 네 개를 아주 약하게 1초 켜 본다 (프로펠러는 뺀다)
PWM_FREQ = 10000         # 10000 Hz (교재와 같다)
TEST_DUTY = 80           # 0 ~ 200 사이의 약한 세기

M1_motor = PWM(Pin(4), freq=PWM_FREQ, duty=0)    
M2_motor = PWM(Pin(5), freq=PWM_FREQ, duty=0)    
M3_motor = PWM(Pin(40), freq=PWM_FREQ, duty=0)   
M4_motor = PWM(Pin(41), freq=PWM_FREQ, duty=0)   

def set_duty(d1, d2, d3, d4):        # 모터마다 듀티를 정해주는 함수
    M1_motor.duty(d1)
    M2_motor.duty(d2)
    M3_motor.duty(d3)
    M4_motor.duty(d4)

try:
    set_duty(TEST_DUTY, TEST_DUTY, TEST_DUTY, TEST_DUTY)
    print("모터 켜짐 duty =", TEST_DUTY)
    time.sleep(1)
except KeyboardInterrupt:
    pass

set_duty(0, 0, 0, 0)   # except 안에 쓰지 않은 방식 
print("모터 꺼짐")
