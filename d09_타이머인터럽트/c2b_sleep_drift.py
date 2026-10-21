from machine import Pin
import time

flash = Pin(4, Pin.OUT, value=0)

time_cnt = 0
start = time.ticks_ms()  # 타이머 시작 시각(ms)

while time_cnt < 1000:
    time.sleep_ms(1)     # sleep시간(1ms)으로 시간 카운트 세기
    time_cnt += 1

    if time_cnt % 100 == 0:    # 100ms마다 flash값 바뀜
        flash.value(not flash.value())

spent = time.ticks_diff(time.ticks_ms(), start)    
print("1ms 를 1000번 센 시간:", spent, "ms")               # 실제로 시작하고 시간이 얼마나 지났는지 확인
print("목표는 1000ms 입니다. 차이:", spent - 1000, "ms")    # 실제 걸린 시간과 1000ms의 차이 확인
