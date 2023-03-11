import os.path
import socket
import struct
import threading

UNIX_SOCK_PIPE_PATH = "./unixsock_proxy.sock"
HOST = "localhost"
PORT = 9999

running_status = None


class UDPServer:
    def __init__(self):
        self.server = None
        try:
            self.server = socket.socket(family=socket.AF_UNIX, type=socket.SOCK_DGRAM)
            if os.path.exists(UNIX_SOCK_PIPE_PATH):
                os.remove(UNIX_SOCK_PIPE_PATH)
            self.addr = UNIX_SOCK_PIPE_PATH
        except Exception:
            self.server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            self.addr = (HOST, PORT)

    def run(self):
        try:
            self.server.bind(self.addr)
        except Exception:
            return
        t_listen = threading.Thread(target=self.__listen)
        t_listen.start()

    def __listen(self):
        while True:
            msg, addr = self.server.recvfrom(1024)
            header = msg[0:4].decode("utf-8")
            print(msg)
            if header == "COOK":  # 判断数据包header，如果是COOK，表示为数据包开头，如果不是，则继续
                length = struct.unpack(">I", msg[4:8])[0]
                data = msg[8:8 + length]
                self.__process(data, addr)
            else:
                print("packet is not COOK")

    def __process(self, data, addr):
        global running_status
        running_status = data
        print(data)

udp_server = UDPServer()

# if __name__ == "__main__":
#     server = UDPServer()
#     server.run()
