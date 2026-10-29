import machine                                  
import time                                     
from machine import Pin, PWM, Timer             

# ---- 객체 만들기 ---- 
buzzer = PWM(Pin(6), freq=440, duty=0)
trigger = Pin(17, mode=Pin.OUT, pull=None)
echo = Pin(1, mode=Pin.IN, pull=None)
trigger.value(0)                 # value() 메서드 : 핀 값을 정한다. 0 = 끔 (처음에는 소리를 쏘지 않는다)

# ---- 내가 바꾸는 값 ----
NEAR_CM = 5                      # 손을 가장 가까이 둘 때의 거리 (가장 작은 소리)
FAR_CM = 60                      # 손을 가장 멀리 둘 때의 거리 (가장 큰 소리) : NEAR_CM 보다 커야 한다
LEVELS = 20                      # 소리 크기를 몇 단계로 나눌까
DUTY_TABLE = [10, 12, 13, 15, 18, 20, 24, 27, 31, 36, 42, 48, 55, 64, 73, 85, 98, 113, 130, 150]
EIGHTH_MS = 200                  # 8분음표 한 개의 길이 : 4분음표 = 2개 = 400 ms
GAP_MS = 100                     # 음이 끝나기 전에 부저를 꺼 두는 시간 : 부저가 켜져있으면 거리 측정 때 흔들림이 있어 방해를 받는다.
LISTEN_MS = 60                   # 부저를 끈 뒤 기다리는 시간 : 거리 측정을 위해 

# 계명 -> 주파수(Hz). 쉼은 0
NOTE_HZ = {"도": 523, "레": 587, "미": 659, "솔": 784, "라": 880, "쉼": 0}

# (계명, 음길이)  음길이 : 8분음표 몇 개 만큼 자리를 차지하나 (1 = 8분, 2 = 4분, 4 = 2분)
school_bell = [
    ("솔", 2), ("솔", 2), ("라", 2), ("라", 2),
    ("솔", 2), ("솔", 2), ("미", 4),                  # 학교종이 땡땡땡
    ("솔", 2), ("솔", 2), ("미", 2), ("미", 2),
    ("레", 4), ("쉼", 4),                             # 어서 모이자
    ("솔", 2), ("솔", 2), ("라", 2), ("라", 2),
    ("솔", 2), ("솔", 2), ("미", 4),                  # 선생님이 우리를
    ("솔", 2), ("미", 2), ("레", 2), ("미", 2),
    ("도", 4), ("쉼", 4),                             # 기다리신다
]

# ---- 인터럽트 깃발 : 알람 ----
ms = 0
flag_10 = False
flag_500 = False

def tick(t):
    global ms, flag_10, flag_500                
    ms += 1
    if ms % 10 == 0:
        flag_10 = True
    if ms % 500 == 0:
        flag_500 = True

def get_distance_cm():                          
    trigger.value(0)                            # value(0) : 끈 상태에서 시작
    time.sleep_us(5)                            # sleep_us() : 5 µs 기다린다 (µs = 마이크로초 = 100만분의 1초)
    trigger.value(1)                            # value(1) : 켠다 = 초음파를 쏘기 시작
    time.sleep_us(10)                           # 10 µs 동안 켜 둔다
    trigger.value(0)                            # value(0) : 끈다 = 쏘기를 끝낸다
    
    # 6000 µs 의 왕복할 수 있는 거리는 약 100 cm. 이보다 멀리 있거나 장애물이 없으면 넘어간다.
    # time_pulse_us(핀, 1, 최대µs) : echo 가 켜져 있던 시간(µs)을 잰다. 
    # echo 가 켜져 있던 시간(µs)으로 거리 측정
    pulse_time = machine.time_pulse_us(echo, 1, 6000)  
    distance_cm = (pulse_time / 2) / 29.1              # 왕복 시간의 절반 ÷ 29.1 = 거리(cm)

    if 2 <= distance_cm <= 200:
        return distance_cm
    else:
        return 0                                       # 못 읽으면(변화가 없으면) 0 반환     

def distance_level(cm):
    # 가까울수록 작은 단계 (t2 와 반대) : NEAR_CM 이하 -> 0, FAR_CM 이상 -> 19
    level = int((cm - NEAR_CM) * LEVELS // (FAR_CM - NEAR_CM))
    # (FAR_CM - NEAR_CM) : 측정할 수 있는 전체 폭
    # cm - NEAR_CM) : 최소 거리 기준 얼마나 떨어져 있는지
    # * LEVELS : 구한 비율에 단계수를 곱해서 몇 번째 단계인지 환산
    if level < 0:
        level = 0
    if level > LEVELS - 1:
        level = LEVELS - 1
    return level

    # level = max(0, min(level,LEVELS - 1))
    # return level
    

idx = 0                          # 지금 몇 번째 음인가
note_start = 0                   # 현재 음이 시작한 ms
measured = False                 # 현재 음에서 거리를 쟀는지 확인 (한 음에서 한번만 측정한다.)(쟀으면 true, 안쟀으면 false)
cm = 0
level = 9
duty = DUTY_TABLE[level]
buzzer.freq(NOTE_HZ[school_bell[0][0]])         # 음악의 첫 음(주파수)으로 설정


tmr = Timer(0)
tmr.init(period=1, mode=Timer.PERIODIC, callback=tick)

try:
    while True:
        if flag_10:                               # 10 ms : 음을 넘기고, 소리 크기를 주고, 소리를 끈 틈에 거리를 잰다
            flag_10 = False
            name, length = school_bell[idx]       # school_bell 리스트에서 현재 음의 계이름과 음길이를 가져온다
            t = ms - note_start                   # 이 음이 재생되고 있는 시간
            
            # 다음 음으로 넘어가는 시점
            if t >= length * EIGHTH_MS:           # 현재 재생시간 >= 음 길이
                note_start += length * EIGHTH_MS  # 음 재생 시작시간 다시 설정
                idx = idx + 1                     # 다음 음으로 넘어간다
                if idx >= len(school_bell):       # 곡이 끝났으면 처음부터 다시
                    idx = 0
                name, length = school_bell[idx]   # 다음 음의 계이름과 음길이를 다시 가져온다
                t = ms - note_start               # left(남은 시간)를 위해 재생되고 있는 시간을 잰다.
                measured = False                  # 새로운 음에서 거리 다시 측정 (듀티 새로 설정하기 위해)
                if NOTE_HZ[name] != 0:            # 바뀐 음으로 (주파수) 적용
                    buzzer.freq(NOTE_HZ[name])  
                    
            left = length * EIGHTH_MS - t        # 이 음이 끝나기까지 남은 ms
            if name == "쉼" or left <= GAP_MS:   # 쉬는 시간이거나 음이 끝나기 직전이면 소리를 끈다
                buzzer.duty(0)                   # 소리를 꺼야지 거리 잴 때 간섭을 받지 않는다.
                if not measured and (name == "쉼" or left <= GAP_MS - LISTEN_MS):
                    measured = True               # 거리 재기 전에 true로 전환
                    cm = get_distance_cm()        # 거리를 다시 잼 (듀티 값 새로 설정)
                    if cm != 0:                   # 0 은 못 읽은 것(변화없음): 이전 단계를 그대로 쓴다
                        level = distance_level(cm)
                        duty = DUTY_TABLE[level]  # 새로운 거리 값으로 듀티 새로 설정
                        
            else:
                buzzer.duty(duty)               # duty() 메서드 : 소리 크기를 정한다 (켜짐)
        if flag_500:                            # 500 ms : 어디쯤인지 쉘에 찍는다
            flag_500 = False
            print("거리", int(cm), "cm -> 단계", level, "-> duty", duty, "|", idx + 1, "/", len(school_bell), school_bell[idx][0])
except KeyboardInterrupt:                       
    pass
finally:                                        # 끝날 때 꼭 실행된다 : 부저와 타이머를 정리한다
    tmr.deinit()                                
    buzzer.duty(0)                                  
    buzzer.deinit() 
