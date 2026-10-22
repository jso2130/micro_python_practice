import bluetooth,ble_simple_peripheral,time

ble = bluetooth.BLE()
p = ble_simple_peripheral.BLESimplePeripheral(ble,name='pyD_2130') # 블루투스 설정 메서드

def on_rx(read):
    print("RX", read)

p.on_write(on_rx)    # 콜백 함수
