import subprocess as sp
from time import sleep, time


def wlanStatus(status="", ssid="", signal=""):
    return {
        "status": status,
        "ssid": ssid,
        "signal": signal,
        "timestamp": int(time() * 1000)
    }


class WlanStatus:
    def __init__(self, queue):
        self.show_wlan_command = "nmcli d show wlan0 | grep STATE"
        self.list_wifi_command = "nmcli device wifi | grep \*"

        self.queue = queue

    def run(self):
        result = sp.Popen(self.show_wlan_command, shell=True, stdout=sp.PIPE, stderr=sp.STDOUT)
        result_str = (result.stdout.read()).decode("utf-8")
        result_list = result_str.split(" ")
        result_list = sorted(set(result_list), key=result_list.index)  # 去重
        status_code = int(result_list[2])
        if status_code == 20:
            self.queue.put(wlanStatus(status="unavailable"))
        elif status_code == 30:
            self.queue.put(wlanStatus(status="disconnected"))
        elif status_code == 100:
            result = sp.Popen(self.list_wifi_command, shell=True, stdout=sp.PIPE, stderr=sp.STDOUT)
            result_str = (result.stdout.read()).decode("utf-8")
            result_list = result_str.split(" ")
            result_list = sorted(set(result_list), key=result_list.index)  # 去重
            if len(result_list) == 1:
                self.queue.put(wlanStatus(status="disconnected"))
            ssid = result_list[3]
            signal = result_list[8]
            self.queue.put(wlanStatus(status="connected", ssid=ssid, signal=signal))

