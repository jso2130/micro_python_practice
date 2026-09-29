from machine import Pin
import time

flash = Pin(4, Pin_OUT, value=0)

def blink_once():
    falsh.value(1)
    time.sleep_ms(300)
    falsh.value(0)
    time.sleep_ms(300)
    
blink_once()