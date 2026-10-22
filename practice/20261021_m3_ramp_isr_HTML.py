import bluetooth, ble_simple_peripheral
from machine import Pin, PWM, Timer

# ───── ★ 고쳐 쓰는 값(파라미터): 이 칸의 숫자만 바꾸면 된다 ─────
SSID = "여기에_와이파이_이름"                   # ★ 화면에 안내된 와이파이 이름으로 바꾼다
PASSWORD = "여기에_비밀번호" 

NAME = "pyD_2130"        
MAX_DUTY = 100           
STEP = 1                 # 100ms 마다 바뀌는 듀티 크기
PWM_FREQ = 10000         # PWM 주파수 (교재 2-4 와 같다)
INPUT_MODE = "text"      # "text": 글자 숫자 "150" 을 보낸다 · "byte": 숫자 1바이트를 보낸다
# ───── 여기까지 ─────

M1_motor = PWM(Pin(4), freq=PWM_FREQ, duty=0)    # 1번 모터
M2_motor = PWM(Pin(5), freq=PWM_FREQ, duty=0)    # 2번 모터
M3_motor = PWM(Pin(40), freq=PWM_FREQ, duty=0)   # 3번 모터
M4_motor = PWM(Pin(41), freq=PWM_FREQ, duty=0)   # 4번 모터

rx_data = None           # 폰이 보낸 것을 적어 두는 포스트잇
target = 0               # 폰이 정해 준 목표 듀티
duty = 0                 # 지금 듀티

ble = bluetooth.BLE()
p = ble_simple_peripheral.BLESimplePeripheral(ble, name=NAME)

wlan = network.WLAN(network.STA_IF)
wlan.active(False)                              # 앞 실행에서 남은 접속 시도를 지우려고
time.sleep_ms(1000)                             # 껐다가 1초 쉬고
wlan.active(True)                               # 다시 켠다
wlan.connect(SSID, PASSWORD)
while not wlan.isconnected():
    time.sleep_ms(300)
ip = wlan.ifconfig()[0]
print("브라우저에 이 주소를 입력하세요 → http://" + ip)

def on_rx(read):                   # 받은 값을 변수에 저장
    global rx_data
    rx_data = read
    
p.on_write(on_rx)

def page(state):
    return ("HTTP/1.0 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
            "<html><body style='font-size:40px;text-align:center'>"
            "<h1>드론 모터 제어하기</h1><p>지금: <b>" + state + "</b></p>"
            "<p><a href='/on'>켜기</a> &nbsp; <a href='/off'>끄기</a></p>"
            "</body></html>")

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("0.0.0.0", 80))
server.listen(2)


state = "꺼짐"
try:
    while True:
        client, addr = server.accept()          # 브라우저가 문을 두드릴 때까지 기다린다
        request = client.recv(512).decode()
        path = request.split(" ")[1] if " " in request else "/"
        print("요청:", addr[0], path)
        if path == "/on":
            flash.duty(BRIGHT)
            state = "켜짐"
        elif path == "/off":
            flash.duty(0)
            state = "꺼짐"
        client.send(page(state))
        client.close()
except KeyboardInterrupt:
    pass
finally:
    server.close()
    flash.duty(0)
    flash.deinit()
    red.value(1)
    print("정지")