from machine import Pin, Timer

flash = Pin(4, Pin.OUT, value=0)  # 매우 밝다, 직시 금지

PERIODS = [200, 100, 50, 20, 10]  # 한 세트의 길이(ms): 5Hz, 10Hz, 20Hz, 50Hz, 100Hz
RATIO = 30                        # 켜진 비율(%) — 모든 단계에서 같다
STAGE_MS = 4000                   # 한 단계를 4초 동안 보여 준다

# 기본값 설정

ms_flag = False
stage = -1         # 인덱스가 0부터 시작하니까 -1로 기본값을 잡는다.
new_stage = 0
time_cnt = 0

def timer_callback(t):
    global ms_flag
    ms_flag = True  # 1ms 마다 깃발만 올린다

tmr = Timer(0)
tmr.init(period=1, mode=Timer.PERIODIC, callback=timer_callback)

try:
    while stage < len(PERIODS):     # 리스트 값의 개수만큼 실행된다.
        if ms_flag:                 # 인터럽트가 생길 때마다 실행된다.
            ms_flag = False
            time_cnt += 1

            new_stage = time_cnt // STAGE_MS       # 8000 // 4000 = 2단계
            if new_stage != stage:                 # stage가 전 단계 수이고 newstage가 현재 단계의 수일 때 실행 
                stage = new_stage                  # 단계마다 한 번만 실행되게 한다.
                if stage >= len(PERIODS):          # 마지막 단계가 되면 실행이 끝남
                    break
                
                p = PERIODS[stage]                 # 현재 리스트값(주기)
                print("한 세트", p, "ms =", 1000 // p, "Hz — 깜빡임이 보이나요?")
                              # 주기      # 주파수(빈도)
            
            # 주기의 30%만 flash를 키는 구간
            on_time = p * RATIO // 100   # 현재 값의 30%를 구한다.
            if time_cnt % p < on_time:   # 한 세트 중 앞쪽 30% 만 켠다
                flash.value(1)
            else:
                flash.value(0)           # 30%가 지나면 꺼준다
except KeyboardInterrupt:
    pass

tmr.deinit()
flash.value(0)
print("끝")
