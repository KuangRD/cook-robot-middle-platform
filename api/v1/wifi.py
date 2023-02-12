from flask_restful import Resource, fields, marshal_with, reqparse
import subprocess as sp

wlan_response = {
    "status": fields.String,
    "ssid": fields.String,
    "signal": fields.String
}


class WlanResponse:
    def __init__(self, status="", ssid="", signal=""):
        self.status = status
        self.ssid = ssid
        self.signal = signal


class Wlan(Resource):
    def put(self, flag):
        if flag == 0:  # 关闭wlan
            result = sp.Popen("nmcli r wifi off", shell=True)
            return "close wlan success"
        else:  # 开启wlan
            result = sp.Popen("nmcli r wifi on", shell=True)
            return "open wlan success"


class Wifi(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'bssid',
            type=str,
            location='json',
            help='parameter bssid is required',
        )
        self.parser.add_argument(
            'password',
            type=str,
            location='json',
            help='parameter password is required',
        )
        self.parser.add_argument(
            'ssid',
            type=str,
            location='json',
            help='parameter ssid is required',
        )

    def get(self):
        in_use_wifi = {}
        no_use_wifi_list = []
        result = sp.Popen("nmcli device wifi", shell=True, stdout=sp.PIPE)
        wifi_connections = result.stdout.readlines()
        wifi_connections.pop(0)
        bssid_list = []
        for wifi_bytes in wifi_connections:
            wifi_list = wifi_bytes.decode("utf-8").split(" ")
            wifi_list = sorted(set(wifi_list), key=wifi_list.index)  # 去重
            # ['', 'A0:C5:F2:BD:8E:82', 'Nikon', 'Infra', '11', '54', 'Mbit/s', '32', '▂▄__', 'WPA2', '\n']
            if wifi_list[0] == "*":
                wifi_list.pop(0)
                in_use_wifi = {
                    "bssid": wifi_list[1],
                    "ssid": wifi_list[2],
                    "mode": wifi_list[3],
                    "chan": wifi_list[4],
                    "rate": wifi_list[5],
                    "signal": wifi_list[7],
                    "bars": wifi_list[8],
                    "security": wifi_list[9],
                }
            else:
                no_use_wifi = {
                    "bssid": wifi_list[1],
                    "ssid": wifi_list[2],
                    "mode": wifi_list[3],
                    "chan": wifi_list[4],
                    "rate": wifi_list[5],
                    "signal": wifi_list[7],
                    "bars": wifi_list[8],
                    "security": wifi_list[9],
                }
                if no_use_wifi["bssid"] in bssid_list:
                    continue
                else:
                    bssid_list.append(no_use_wifi["bssid"])
                    no_use_wifi_list.append(no_use_wifi)
        return {"in_use_wifi": in_use_wifi, "no_use_wifi_list": no_use_wifi_list}

    def post(self, flag):
        if flag == 1:
            args = self.parser.parse_args()
            bssid = args.get("bssid")
            password = args.get("password")
            result = sp.Popen("nmcli device wifi connect " + bssid + " password " + password, shell=True,
                              stdout=sp.PIPE,
                              stderr=sp.STDOUT)
            result_str = result.stdout.read().decode("utf-8")
            if "Error" in result_str:
                return "connect failed"
            else:
                return "connect success"
        if flag == 0:
            args = self.parser.parse_args()
            ssid = args.get("ssid")
            result = sp.Popen("nmcli connection down " + ssid, shell=True)
            return "disconnect success"
