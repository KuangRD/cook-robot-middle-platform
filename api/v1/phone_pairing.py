import socket
import sys

from apscheduler.schedulers.background import BackgroundScheduler
from flask_restful import Resource, reqparse
from utils.get_net_info import get_net_info


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

    message = interface_ip + "," + mac

    # 发送广播消息
    sock.sendto(message.encode(), (broadcast_ip, port))

    # 关闭套接字
    sock.close()


apscheduler = BackgroundScheduler()
apscheduler.add_job(send_broadcast_message, 'interval', seconds=1)


class PhonePairing(Resource):
    def put(self, flag):
        if flag == 0:  # 关闭配对
            print(123)
            apscheduler.pause()
            return "close wlan success"
        else:  # 开启配对
            print(456)
            apscheduler.start()
            return "open wlan success"
