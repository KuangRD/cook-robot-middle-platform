from time import sleep

import serial


ser = serial.Serial("/dev/ttyS0", 9600)

while True:
    print("waiting")
    count = ser.inWaiting()
    if count != 0:
        recv = ser.read(count)
        scan_result = recv.decode("utf-8")
        print(scan_result)
    ser.flushInput()
    sleep(0.1)