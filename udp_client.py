import os
import socket
import struct
import sys
from functools import wraps

UNIX_SOCK_PIPE_PATH_COMMAND_CLIENT = "/tmp/unixsock_command_client.sock"
UNIX_SOCK_PIPE_PATH_COMMAND_SERVER = "/tmp/unixsock_command_server.sock"
UNIX_SOCK_PIPE_PATH_STATUS_CLIENT = "/tmp/unixsock_status_client.sock"
UNIX_SOCK_PIPE_PATH_STATUS_SERVER = "/tmp/unixsock_status_server.sock"
# HOST = "127.0.0.1"
HOST = "169.254.70.55"
COMMAND_PORT = 9999
STATUS_PORT = 9998


class UDPClient:
    def __init__(self, local_path, remote_path, port):
        self.buff_size = 1024
        self.remote_path = remote_path
        if sys.platform == "linux":
            self.client = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
            if os.path.exists(local_path):
                os.remove(local_path)
            self.client.bind(local_path)
            self.addr = remote_path
        else:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.addr = (HOST, port)

    def send(self, msg):
        self.client.sendto(msg, self.addr)
        res, addr = self.client.recvfrom(1024)
        header = res[0:4].decode("utf-8")
        if header == "COOK":
            length = struct.unpack(">I", res[4:8])[0]
            data = res[8:8 + length]
            return self._process(data)
        else:
            return False

    def _process(self, data: bytes):
        # override
        pass


class UDPCommandClient(UDPClient):
    def _process(self, data: bytes):
        data_header = data[0:3].decode("utf-8")
        if data_header == "CCR":
            return True if data[7] == 1 else False
        elif data_header == "CIR":
            return True if data[7] == 1 else False
        else:
            return False


class UDPStatusClient(UDPClient):
    def _process(self, data: bytes):
        data_header = data[0:3].decode("utf-8")
        if data_header == "CSR":
            return
        else:
            return False


udp_command_client = UDPCommandClient(UNIX_SOCK_PIPE_PATH_COMMAND_CLIENT,
                                      UNIX_SOCK_PIPE_PATH_COMMAND_SERVER,
                                      COMMAND_PORT)
udp_status_client = UDPStatusClient(UNIX_SOCK_PIPE_PATH_STATUS_CLIENT,
                                    UNIX_SOCK_PIPE_PATH_STATUS_SERVER,
                                    STATUS_PORT)
