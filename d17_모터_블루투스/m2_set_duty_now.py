import bluetooth, ble_simple_peripheral
from machine import Pin, PWM

# ───── ★ 고쳐 쓰는 값 ─────
NAME = "pyD_2130"        
MAX_DUTY = 100           
PWM_FREQ = 10000         
INPUT_MODE = "text"      # "text": 글자 숫자 "150" 을 보낸다 · "byte": 숫자 1바이트를 보낸다
# ───── 여기까지 ─────

M1_motor = PWM(Pin(4), freq=PWM_FREQ, duty=0)    # 1번 모터
M2_motor = PWM(Pin(5), freq=PWM_FREQ, duty=0)    # 2번 모터
M3_motor = PWM(Pin(40), freq=PWM_FREQ, duty=0)   # 3번 모터
M4_motor = PWM(Pin(41), freq=PWM_FREQ, duty=0)   # 4번 모터

ble = bluetooth.BLE()
p = ble_simple_peripheral.BLESimplePeripheral(ble, name=NAME)

rx_data = None           # 폰이 보낸 것을 적어 두는 포스트잇

def on_rx(read):
    global rx_data
    rx_data = read

p.on_write(on_rx)

def to_number(read):
    if INPUT_MODE == "byte":
        return read[0]
    return int(read.decode().strip())

def limit(n, lo, hi):
    if n < lo:
        return lo
    if n > hi:
        return hi
    return n

def set_duty(d1, d2, d3, d4):        # 모터마다 듀티를 하나씩 직접 정해 준다
    M1_motor.duty(d1)
    M2_motor.duty(d2)
    M3_motor.duty(d3)
    M4_motor.duty(d4)

print("광고 중:", NAME)

try:
    while True:
        if rx_data is not None:   # rx_data를 data에 담고 비워준다
            data = rx_data
            rx_data = None
            try:
                target = limit(to_number(data), 0, MAX_DUTY)   # duty범위에 들어가는지 확인한 최종 숫자를 담아준다
                set_duty(target, target, target, target)       # 받은 숫자를 듀티 적용 함수에 던져준다
                print("목표 듀티 =", target)
                if target == 0:
                    print("모터 꺼짐")
            except ValueError:
                print("숫자를 보내 주세요:", data)
except KeyboardInterrupt:
    set_duty(0, 0, 0, 0)
    M1_motor.deinit()
    M2_motor.deinit()
    M3_motor.deinit()
    M4_motor.deinit()
    print("정지 — 모터 꺼짐")
