from machine import Pin,Timer

flash = Pin(4, Pin.OUT, value=0)
red = Pin(33, Pin.OUT, value=1)

ms_flag = False         
time_cnt = 0


def timer_100ms():
    flash.value(flash.value() ^ 1)

def timer_500ms():
    red.value(flash.value() ^ 1)
    
def timer_callback(t):
    global ms_flag        # 글로벌 변수 : 함수 밖에서도 쓸 수 있음
    ms_flag = True
    
tmr = Timer(0)
tmr.init(period = 1, mode = Timer.PERIODIC, callback = timer_callback) # 초기화

try:
    while True:
    
        if ms_flag:
            ms_flag = False
            time_cnt += 1
            
            if time_cnt % 100 == 0:
                timer_100ms()
                
            if time_cnt % 500 == 0:
                timer_500ms()
                
except KeyboardInterrpt:
    
    flash.value(0)
    red.value(1)
    
    tmr.deinit()
    print('타이머 정지')
        
