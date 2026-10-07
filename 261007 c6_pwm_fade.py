from machine import Pin, PWM, Timer

flash = PWM(Pin(4), freq=1000, duty=0)

duty = 0
step = 5         # duty가 한 번에 바뀌는 크기
time_cnt = 0
ms_flag = False
min_value = 300
max_value = 0

def timer_callback(t):
    global ms_flag
    ms_flag = True

def timer_10ms():
    global duty, step
    duty += step
    if duty >= min_value:  # 위 끝에 닿으면
        duty = min_value
        step = -step       # 방향을 뒤집는다
    if duty <= max_value:  # 아래 끝에 닿으면
        duty = max_value
        step = -step       # -에 -를 하면 +로 전환
    flash.duty(duty)

tmr = Timer(0)
tmr.init(period=1, mode=Timer.PERIODIC, callback=timer_callback)

try:
    while True:
        if ms_flag:
            ms_flag = False
            time_cnt += 1

            if time_cnt % 10 == 0:
                timer_10ms()
except KeyboardInterrupt:
    tmr.deinit()
    flash.duty(0)
    flash.deinit()
    print("정지")
