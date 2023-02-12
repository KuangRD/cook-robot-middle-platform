from status.qrscan import QrScanStatus
from status.wlan import WlanStatus
from concurrent import futures
from queue import Queue
from apscheduler.schedulers.background import BackgroundScheduler


def getQueue(q, data="", name=""):
    while True:
        if name == "wlan":
            data.wlan = q.get()
        if name == "qr_scan_data":
            new_data = q.get()
            is_new = False
            if data.qr_scan_data["text"] != new_data["text"] or \
                    new_data["timestamp"] - data.qr_scan_data["timestamp"] > 5000:
                is_new = True
            data.qr_scan_data = {
                "is_new": is_new,
                "text": new_data["text"],
                "timestamp": new_data["timestamp"]
            }


class SystemStatus:
    def __init__(self, data):
        self.data = data
        self.qrScanQueue = Queue(1)
        self.qrScanStatus = QrScanStatus(self.qrScanQueue)
        self.wlanQueue = Queue(1)
        self.wlanStatus = WlanStatus(self.wlanQueue)

        self.pool = futures.ThreadPoolExecutor(max_workers=4)

    def run(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=self.wlanStatus.run, trigger="interval", max_instances=10, seconds=1)
        # scheduler.add_job(func=self.data.clear_qr_scan_data, trigger="interval", max_instances=10, seconds=2)
        scheduler.start()
        task1 = self.pool.submit(self.qrScanStatus.run)
        # task3 = self.pool.submit(getQueue, [self.qrScanQueue, self.data, "qr_scan_data"])
        # task4 = self.pool.submit(getQueue, [self.wlanQueue, self.data, "wlan"])
        task4 = self.pool.submit(lambda p: getQueue(*p), (self.qrScanQueue, self.data, "qr_scan_data"))
        task4 = self.pool.submit(lambda p: getQueue(*p), (self.wlanQueue, self.data, "wlan"))
