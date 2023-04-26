import os
import socket
import struct
import sys
from functools import wraps

from packer import StateRequestPacker

UNIX_SOCK_PIPE_PATH_COMMAND_CLIENT = "/tmp/unixsock_command_client.sock"
UNIX_SOCK_PIPE_PATH_COMMAND_SERVER = "/tmp/unixsock_command_server.sock"
UNIX_SOCK_PIPE_PATH_STATE_CLIENT = "/tmp/unixsock_state_client.sock"
UNIX_SOCK_PIPE_PATH_STATE_SERVER = "/tmp/unixsock_state_server.sock"
HOST = "127.0.0.1"
# HOST = "169.254.70.55"
COMMAND_CLIENT_PORT = 10010
COMMAND_SERVER_PORT = 10011
STATE_CLIENT_PORT = 10012
STATE_SERVER_PORT = 10013

plc_state = {}

state_template = {
    "time": 0,
    "machine_state": 0,

    "y_reset_control_word": 0,
    "y_set_control_word": 0,
    "y_set_target_position": 0,
    "y_set_real_position": 0,
    "y_set_total_distance": 0,
    "y_set_rotate_speed": 0,

    "x_reset_control_word": 0,
    "x_set_control_word": 0,
    "x_set_target_position": 0,
    "x_set_real_position": 0,
    "x_set_total_distance": 0,
    "x_set_move_speed": 0,

    "r_control_word": 0,
    "r_rotate_mode": 0,
    "r_rotate_speed": 0,
    "r_rotate_number": 0,

    "shake_control_word": 0,
    "shake_current_number": 0,
    "shake_total_number": 0,
    "shake_up_speed": 0,
    "shake_down_speed": 0,

    "liquid_pump_control_word": 0,
    "liquid_pump_number": 0,
    "liquid_pump_time": 0,

    "water_pump_control_word": 0,
    "water_pump_number": 0,
    "water_pump_time": 0,

    "solid_pump_control_word": 0,
    "solid_pump_number": 0,
    "solid_pump_time": 0,

    "temperature_control_word": 0,
    "temperature_target_number": 0,
    "temperature_current_number": 0,
    "temperature_up_number": 0,
    "temperature_down_number": 0,
    "temperature_warning": 0,
    "temperature_infrared_number": 0,

    "emergency": 0,
}


class UDPClient:
    def __init__(self, local_path, remote_path, local_port, remote_port):
        self.client = None
        if sys.platform == "linux11":
            self.client = socket.socket(family=socket.AF_UNIX, type=socket.SOCK_DGRAM)
            if os.path.exists(local_path):
                os.remove(local_path)
            self.addr = local_path
            self.remote_addr = remote_path
        else:
            self.client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            self.addr = (HOST, local_port)
            self.remote_addr = (HOST, remote_port)
        print(self.addr)
        self.client.bind(self.addr)
        print(self.__class__.__name__)

    def run(self):
        while True:
            try:
                msg, addr = self.client.recvfrom(1024)
            except Exception as e:
                print(e)
                continue
            header = msg[0:4].decode("utf-8")
            if header == "COOK":  # 判断数据包header，如果是COOK，表示为数据包开头，如果不是，则继续
                length = struct.unpack(">I", msg[4:8])[0]
                data = msg[8:8 + length]
                self._process(data)
            else:
                print("packet is not COOK")

    def send(self, msg):
        self.client.sendto(msg, self.remote_addr)
        return True

    def _process(self, data: bytes):
        # override
        pass


class UDPCommandClient(UDPClient):
    def __init__(self, local_path, remote_path, local_port, remote_port):
        super().__init__(local_path, remote_path, local_port, remote_port)

    def _process(self, data: bytes):
        data_header = data[0:3].decode("utf-8")
        if data_header == "CCR":
            return True if data[7] == 1 else False
        elif data_header == "CIR":
            return True if data[7] == 1 else False
        else:
            return False


class UDPStateClient(UDPClient):
    def __init__(self, local_path, remote_path, local_port, remote_port):
        super().__init__(local_path, remote_path, local_port, remote_port)
        self.count = 1

    def _process(self, data: bytes):
        data_header = data[0:3].decode("utf-8")
        if data_header == "CSR":
            global plc_state
            state = data[14:]
            for index, key in enumerate(state_template):
                plc_state[key] = struct.unpack(">H", state[2 * index:2 * index + 2])[0]
            return plc_state
        else:
            return False


command_client = UDPCommandClient(UNIX_SOCK_PIPE_PATH_COMMAND_CLIENT,
                                  UNIX_SOCK_PIPE_PATH_COMMAND_SERVER,
                                  COMMAND_CLIENT_PORT, COMMAND_SERVER_PORT)
state_client = UDPStateClient(UNIX_SOCK_PIPE_PATH_STATE_CLIENT,
                              UNIX_SOCK_PIPE_PATH_STATE_SERVER,
                              STATE_CLIENT_PORT, STATE_SERVER_PORT)
