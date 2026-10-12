# 누르면 켜지고 또 누르면 꺼짐 (한 번 누른상태 유지)
# 안전 장치가 없는 코드
from machine import Pin, Timer

btn = Pin(0, Pin.IN, Pin.PULL_UP)    # 입력, 초기값 1(high)
flash = Pin(4, Pin.OUT, value=0)     # 출력, 초기값 0(off)
red = Pin(33, Pin.OUT, value=1)      # 출력, 초기값 1(off)

time_cnt = 0
ms_flag = False
btn_last = 1    
red_start = 0   

def timer_callback(t):   # ISR : 함수를 최대한 간단하게 세팅해야 함
    global ms_flag
    ms_flag = True

def task_10ms():
    global btn_last, red_start
    now = btn.value()        
    if btn_last == 1 and now == 0:      # 버튼을 누르는 순간 
        red_start = 1                   # red led의 상태를 최초 누른 상태부터 쭉 1로 유지하므로 계속 깜빡임
        flash.value(flash.value() ^ 1)  # 플래시 토글 (on/off 전환)
        print("버튼 눌림 → 플래시 토글")
    btn_last = now                      # 버튼을 떼면 1이 담기고 누르고 있는 동안은 0이 담긴다

def task_500ms():
    if red_start == 1:
        red.value(red.value() ^ 1)       # 버튼과 상관없이 500ms마다 깜빡임

TASKS = [
    (10, task_10ms),
    (500, task_500ms),
]
CYCLE = 1000

tmr = Timer(0)
tmr.init(period=1, mode=Timer.PERIODIC, callback=timer_callback)

try:
    while True:
        if ms_flag:
            ms_flag = False
            time_cnt += 1

            for period, task in TASKS:
                if time_cnt % period == 0:     # 10ms, 500ms 타임체크
                    task()                     # 함수 실행 

            if time_cnt >= CYCLE:       # 1000에 초기화
                time_cnt = 0
except KeyboardInterrupt:
    tmr.deinit()
    flash.value(0)
    red.value(1)
    print("타이머 정지")
