# 누르면 켜지고 또 누르면 꺼짐 (한 번 누른상태 유지)
# 안전 장치를 만든 코드
from machine import Pin, Timer

btn = Pin(0, Pin.IN, Pin.PULL_UP)       # 누르면 0
flash = Pin(4, Pin.OUT, value=0)        # 플래시: 매우 밝다, 직시 금지

DEBOUNCE_MS = 100    # 디바운스 인정 시간
CHECK_MS = 10        # 버튼을 확인하는 간격 

raw_last = 1        # 직전에 읽은 값 (떨림 포함)
stable = 1          # 안정된 값: 1 = 뗌, 0 = 눌림 (0 도 1 도 DEBOUNCE_MS동안 안정돼야 바뀐다)
same_ms = 0         # 값이 바뀌지 않고 이어진 시간 (ms)
raw_changes = 0     # 디바운스(떨림) 의 횟수 (떨림도 센다)
presses = 0         # 인정된 눌림 횟수 (1 → 0 → 1 한 바퀴가 끝났을 때 센다)

# 인터럽트가 세우는 깃발
flag_10ms = False
isr_cnt = 0

def timer_isr(t):
    global isr_cnt, flag_10ms
    isr_cnt += 1
    if isr_cnt % CHECK_MS == 0:   # 항상 while문에 있던 타임체크를 isr에 넣어도 됨 ()
        flag_10ms = True          
    if isr_cnt >= 1000:           # 카운트 초기화      
        isr_cnt = 0
    # 깃발만 세우고 바로 빠져나간다

def task_10ms():
    global raw_last, stable, same_ms, raw_changes, presses
    now = btn.value()   # 현재 버튼 상태 
    if now != raw_last: # 전값과 현재값이 다르면 떨림으로 감지
        raw_changes += 1    # 디바운스 횟수
        raw_last = now      # 직전값을 현재값으로
        same_ms = 0         # 유지시간 0으로 초기화
        return
    same_ms += CHECK_MS     # 유지시간 
    if same_ms >= DEBOUNCE_MS and now != stable:   # 충분히 안정됐고 인정된 값과 다르면
        stable = now                    # 이제야 인정한다 (0 도 1 도 똑같이 기다린다)
        if stable == 0:                 # 1 → 0 : 눌림이 확정됐다. 아직 한 바퀴가 안 끝났다
            print("누름 확정 (뗄 때까지 기다린다)")
        else:                           
            presses += 1                # 눌린 횟수
            flash.value(flash.value() ^ 1)
            print("눌림 인정", presses, "번 / 디바운스 횟수", raw_changes)

tmr = Timer(0)
tmr.init(period=1, mode=Timer.PERIODIC, callback=timer_isr)

try:
    while True:
        if flag_10ms:
            flag_10ms = False
            task_10ms()
except KeyboardInterrupt:
    tmr.deinit()
    flash.value(0)
    print("정지. 인정된 눌림", presses, "번 / 값이 바뀐 횟수", raw_changes)

# 깨끗한 버튼이면 눌림 1번에 값이 2번(눌림, 뗌) 바뀐다. 그보다 많으면 채터링이다.
# ⭐ 도전: DEBOUNCE_MS 를 20, 70, 150 으로 바꿔 보자 (작으면 떨림을 못 거르고, 크면 짧은 누름을 놓친다)
