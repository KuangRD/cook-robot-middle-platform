import time

import serial

ser = serial.Serial("/dev/ttyS0", 9600)
# ser = serial.Serial("/dev/ttyAMA0", 9600)

while 1:
    count = ser.inWaiting()
    if count != 0:
        recv = ser.read(count)
        print(recv)
        # print(recv.encode("unicode_escape"))
        # ser.write(recv)
    ser.flushInput()

    time.sleep(0.1)
