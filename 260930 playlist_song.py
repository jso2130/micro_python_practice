from machine import Pin
import time

flash = Pin(4, Pin.OUT, value=0)
red = Pin(33, Pin.OUT, value=1)

heart = [100, 100, 600]
sos = [150, 150, 150, 450, 450, 450, 150, 150, 150]
speedup = [600, 500, 400, 300, 200, 100]
 
playlist = [heart, sos, speedup]

def run_pattern(pin_obj, pattern_list, on=1):
    for ms in pattern_list:
        pin_obj.value(on)
        time.sleep_ms(ms)
        pin_obj.value(1 - on)
        time.sleep_ms(200)
 
def make_speedup(count, start, step):
    result = []
    for i in range(count):
        result.append(start - i * step)
    return result

for song in playlist:
    print("재생:", song)
    run_pattern(flash, song)
    run_pattern(red, [800], 0)
 
print("플레이리스트 끝")