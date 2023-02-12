import serial
from time import sleep, time


class QrScanStatus:
    def __init__(self, queue=None):
        self.ser = serial.Serial("/dev/ttyS0", 9600)
        self.queue = queue

    def run(self):
        while True:
            count = self.ser.inWaiting()
            if count != 0:
                recv = self.ser.read(count)
                scan_result = recv.decode("utf-8")
                self.queue.put({
                    "text": scan_result,
                    "timestamp": int(time() * 1000)
                })

            self.ser.flushInput()
            sleep(0.1)
