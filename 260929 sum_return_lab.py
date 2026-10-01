from machine import Pin
import time

flash = Pin(4, Pin.OUT, value=0)

UNIT = 150
SOS = [1,1,1,3,3,3,1,1,1]
SES = [1,1,1,0,1,0,1,1,1]
ILOVEYOU = [1,1,0,1,3,1,1,0,3,3,3,0,1,1,1,3,0,1,0,3,1,3,3,0,3,3,3,0,1,1,3]

def send_morse(pin_obj, signals, unit):
    on_times = []
    for s in signals:
        pin_obj.value(1)
        time.sleep_ms(s * unit)
        pin_obj.value(0)               
        time.sleep_ms(unit)
        
        on_times.append(s * unit)
        
    if signals == SOS:
        print("SOS 전송 완료")
        print("총 시간: ", sum(on_times) + unit * len(signals))
    elif signals == ILOVEYOU:
        print("I LOVE YOU 전송 완료")
        print("총 시간: ", sum(on_times) + unit * len(signals))
    elif signals == SES:
        print("SES 전송 완료")
        print("총 시간: ", sum(on_times) + unit * len(signals))
        
    return on_times
        
send_morse(flash, ILOVEYOU, UNIT)