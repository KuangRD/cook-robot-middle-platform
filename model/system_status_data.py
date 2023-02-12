class SystemStatusData:
    def __init__(self):
        self.wlan = {
            "status": "",
            "ssid": "",
            "signal": "",
            "timestamp": 0
        }
        self.qr_scan_data = {
            "is_new": False,
            "text": "",
            "timestamp": 0
        }

    def get_status(self):
        return {
            "wlan": self.wlan,
            "qr_scan_data": self.qr_scan_data
        }

    def clear_qr_scan_data(self):
        self.qr_scan_data = {
            "is_new": False,
            "text": "",
            "timestamp": 0
        }
