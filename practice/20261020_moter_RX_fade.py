from machine import Pin, PWM, Timer
import bluetooth,ble_simple_peripheral,time

ble = bluetooth.BLE()
p = ble_simple_peripheral.BLESimplePeripheral(ble,name='pyD_1234') # 블루투스 초기화 및 서비스 등록 과정

M1_motor = PWM(Pin(4), freq = 10000 ,duty=0)
M2_motor = PWM(Pin(5), freq = 10000 ,duty=0)
M3_motor = PWM(Pin(40), freq = 10000 ,duty=0)
M4_motor = PWM(Pin(41), freq = 10000 ,duty=0)

moters = [M1_motor, M2_motor, M3_motor, M4_motor]

MIN_DUTY = 20  
MAX_DUTY = 100  
STEPS = 5
UPDATE_MS = 20

level = 0
direction = 1
time_cnt = 0
ms_flag = False
is_running = False    # 모터가 켜진 상태인지 알 수 있는 변수

def timer_callback(t):
    global ms_flag
    ms_flag = True

def level_to_duty(lv):  # duty 제곱 곡선
    return MIN_DUTY + (MAX_DUTY - MIN_DUTY) * lv * lv // (STEPS * STEPS)

def fade_step():
    global level, direction
    level += direction                # level의 상/하안선에 도달해 바뀐 fade 방향값이 레벨에 적용
    if level >= STEPS or level == 0:   
        direction = -direction         # level의 상/하안선에 도달하면 fade 방향이 바뀜

    for m in moters:                   # 모든 모터에 현재 level duty값 적용
        m.duty(level_to_duty(level))

def on_rx(read):
    global is_running, level
    cmd = read.decode('UTF-8').strip()
    if cmd == "1":
        is_running = True
        print("켜짐")
    elif cmd == "0":
        is_running = False
        for m in moters:
            m.duty(0)
            level = 0
        print("꺼짐")
    else:
        print("잘못 입력하셨습니다.")

p.on_write(on_rx)

tmr = Timer(0)
tmr.init(period=1, mode=Timer.PERIODIC, callback=timer_callback)

try:
    while True:
        if ms_flag:
            ms_flag = False
            time_cnt += 1

            if is_running == True and time_cnt % UPDATE_MS == 0:
                fade_step()
        
except KeyboardInterrupt:
    tmr.deinit()
