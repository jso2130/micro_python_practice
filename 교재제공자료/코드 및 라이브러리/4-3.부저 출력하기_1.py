from machine import Pin, PWM
import time

melody_buzzer = PWM(Pin(6, Pin.OUT), freq=100, duty=0)
melody_buzzer.duty(0)  

do = 261
re = 293
mi = 329
fa = 349
sol = 392
la = 440
si = 493
do2 = 523

frequency_list = [do,re,mi,fa,sol,la,si,do2]

try:
    while True:
        for frequency in frequency_list:
            melody_buzzer.duty(100) 
            melody_buzzer.freq(int(frequency))
            time.sleep_ms(200)  
except:
    melody_buzzer.duty(0) 