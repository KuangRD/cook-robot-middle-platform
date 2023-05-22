import socket
import sys

from apscheduler.schedulers.background import BackgroundScheduler
from flask_restful import Resource, reqparse
from utils.get_net_info import get_net_info

from utils.m_dns_service import mDnsService

broadcast_state = 0  # 0:关闭 1:开启 2:暂停


def send_broadcast_message():
    broadcast_ip = "255.255.255.255"
    port = 12345
    if sys.platform == "linux":
        interface_ip, mac = get_net_info("wlan0")
    else:
        interface_ip, mac = "192.168.222.235", "00:00:00:00:00:00"
    # 创建UDP套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 设置套接字选项，绑定到特定的网卡IP地址
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind((interface_ip, 0))

    message = "pairing," + interface_ip + "," + mac
    print(message)

    # 发送广播消息
    sock.sendto(message.encode(), (broadcast_ip, port))

    # 关闭套接字
    sock.close()


apscheduler = BackgroundScheduler()
apscheduler.add_job(send_broadcast_message, 'interval', seconds=1)

pairing_state_data = {
    "pairing_state": 0,  # 0:未开启 1.开启配对 2:配对中 3:配对成功 4:配对失败
    "phone_info": {
        "ip": "",
        "mac": "",
        "hostname": ""
    }
}

api_key = "Cook-Robot"


class PhonePairingForMachine(Resource):
    def put(self, flag):
        global broadcast_state
        res = {
            "success": True,
        }
        if flag == 0:  # 关闭配对
            print("关闭配对")
            mDnsService.pause()
            if broadcast_state != 0:
                apscheduler.pause()
                broadcast_state = 2
            pairing_state_data["pairing_state"] = 0
            return res
        elif flag == 1:  # 开启配对
            mDnsService.start()
            print("开启配对")
            if broadcast_state == 0:
                apscheduler.start()
            else:
                apscheduler.resume()
            broadcast_state = 1
            pairing_state_data["pairing_state"] = 1
            return res
        elif flag == 2:  # 确认配对
            if pairing_state_data["phone_info"]["ip"] != "" and pairing_state_data["phone_info"]["hostname"] != 0:
                pairing_state_data["pairing_state"] = 3
                print("配对成功")
            else:
                pairing_state_data["pairing_state"] = 4
                res["success"] = False
                print("配对失败")
            pairing_state_data["phone_info"]["ip"] = ""
            pairing_state_data["phone_info"]["mac"] = ""
            pairing_state_data["phone_info"]["hostname"] = ""
            return res
        elif flag == 3:  # 取消配对
            pairing_state_data["pairing_state"] = 4
            pairing_state_data["phone_info"]["ip"] = ""
            pairing_state_data["phone_info"]["mac"] = ""
            pairing_state_data["phone_info"]["hostname"] = ""
            print("取消配对")
            return res

    def get(self):
        res = {
            "success": True,
            "data": pairing_state_data
        }

        return res


class PhonePairingForPhone(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'ip',
            type=str,
            location='json',
            help='parameter ip is required',
        )
        self.parser.add_argument(
            'mac',
            type=str,
            location='json',
            help='parameter mac is required',
        )
        self.parser.add_argument(
            'hostname',
            type=str,
            location='json',
            help='parameter hostname is required',
        )

    def get(self):
        res = {
            "success": True,
            "data": pairing_state_data
        }

        return res

    def post(self):
        args = self.parser.parse_args()
        ip = args.get("ip")
        mac = args.get("mac")
        hostname = args.get("hostname")
        pairing_state_data["pairing_state"] = 2
        pairing_state_data["phone_info"]["ip"] = ip
        pairing_state_data["phone_info"]["mac"] = mac
        pairing_state_data["phone_info"]["hostname"] = hostname
        print(pairing_state_data)
        res = {
            "success": True,
            "data": api_key
        }
        return res
