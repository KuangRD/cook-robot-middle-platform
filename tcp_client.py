import socket
import struct
import threading
import time
from queue import Queue


class TcpClient:
    def __init__(self):
        self.client = None
        self.host = "127.0.0.1"
        self.port = 9999
        self.buff_size = 1024
        self.queue = Queue(maxsize=1)

    def run(self):
        t_connect = threading.Thread(target=self.__connect)
        t_task = threading.Thread(target=self.__task)

        t_connect.start()
        t_task.start()

    def __connect(self):
        while True:
            try:
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client.connect((self.host, self.port))
            except Exception as e:
                print("connecting:%s" % e)
                time.sleep(1)
                continue
            else:
                print("connect to tcp server successfully.")
                break

    def __task(self):
        while True:
            try:
                data = self.client.recv(8)
                head = data[0:4].decode("utf-8")
                if head == "COOK":
                    length = struct.unpack(">I", data[4:8])[0]
                    remained_length = length
                    all_data = b""
                    recv_size = 0
                    while recv_size < length:
                        if remained_length <= self.buff_size:
                            data = self.client.recv(remained_length)
                        else:
                            data = self.client.recv(self.buff_size)
                            remained_length = remained_length - self.buff_size
                        recv_size += len(data)
                        all_data += data
                    self.__process(all_data)
                else:
                    continue
            except Exception as e:
                print("receive:%s" % e)
                time.sleep(1)
                continue

    def __process(self, data: bytes):
        data_header = data[0:3].decode("utf-8")
        if data_header == "CCR":
            self.queue.put(True if data[7] == 1 else False)
        elif data_header == "CIR":
            self.queue.put(True if data[7] == 1 else False)
        elif data_header == "CSR":  # c controller工作状态
            return
        else:
            return False

    def send(self, msg):
        for i in range(10):
            try:
                self.client.sendall(msg)
                res = self.queue.get()
                return res
            except Exception as e:
                print(e)
                print("send")
                self.__connect()
                continue
        return False


tcp_client = TcpClient()
