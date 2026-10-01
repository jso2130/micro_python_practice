from machine import Pin
import time

def blink_once(pin_num, times, ms_on, ms_off):
    led_controller = Pin(pin_num, Pin.OUT, value = 0)    # Pin도 함수이다.
    
    if pin_num == 4:
        ON = True                      # Pin 4은 value가 0일 때 on이다.       
        OFF = False
    else:
        ON = False                     # Pin 33은 value가 1일 때 on이다. 
        OFF = True
        
    for i in range(times):
        led_controller.value(ON)
        time.sleep_ms(ms_on)
        led_controller.value(OFF)
        time.sleep_ms(ms_off)

blink_once(4, 3, 100, 100)
blink_once(33, 3, 100, 100)
        
        