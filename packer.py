import struct
from time import time

HEADER = "COOK"
COMMAND_DATA_HEADER = "CCS"
INQUIRY_DATA_HEADER = "CIS"
STATE_REQUEST_DATA_HEADER = "CSS"
STATE_RESPONSE_DATA_HEADER = "CSR"


# HEADER DATA_LENGTH DATA_INFO DATA1 DATA2 DATA3 ...
class CommandPacker:
    count = 1

    def __init__(self):
        self.msg = HEADER.encode()  # HEADER, 4 bytes
        self.data_info = b""
        self.data = b""
        CommandPacker.count += 1

    def pack(self, command: dict):
        model = command["model"]
        instructions = command["instructions"]
        if len(instructions) == 0:
            raise NameError("instructions is empty")
        data_length = 14 + 14 * len(instructions)
        self.msg += struct.pack(">I", data_length)  # DATA_LENGTH, 4 bytes

        # DATA_INFO
        self.data_info += COMMAND_DATA_HEADER.encode()  # DATA_HEADER, 3 bytes
        self.data_info += struct.pack(">I", self.count)  # DATA_NO, 4 bytes
        self.data_info += b"\x01" if model == "single" else b"\x02" if model == "multiple" else b"\x03"  # INSTRUCTION_MODEL, 1 byte
        self.data_info += struct.pack(">H", len(instructions))  # INSTRUCTION_COUNT, 2 bytes
        self.data_info += struct.pack(">I", int(time()))  # DATA_DATETIME, 4 bytes
        self.msg += self.data_info

        # DATA
        instruction_no = 1
        for instruction in instructions:

            self.data += struct.pack(">H", instruction_no)
            instruction_no += 1

            if instruction["type"] == "ingredient":
                instruction_type = b"\x01"
                instruction_target = struct.pack(">H", instruction["target"])
                instruction_action = b"\x00"
                instruction_measures = b"\x00\x00\x00\x00"
            elif instruction["type"] == "water":
                instruction_type = b"\x02"
                instruction_target = b"\x00\x00"
                instruction_action = b"\x00"
                instruction_measures = struct.pack(">I", instruction["measures"])
            elif instruction["type"] == "seasoning":
                instruction_type = b"\x03"
                instruction_target = struct.pack(">H", instruction["target"])
                instruction_action = b"\x00"
                instruction_measures = struct.pack(">I", instruction["measures"])
            elif instruction["type"] == "fire":
                instruction_type = b"\x04"
                instruction_target = b"\x00\x00"
                if instruction["action"] == "on":
                    instruction_action = b"\x01"
                    instruction_measures = struct.pack(">I", instruction["measures"])
                else:
                    instruction_action = b"\x02"
                    instruction_measures = b"\x00\x00\x00\x00"
            elif instruction["type"] == "stir_fry":
                instruction_type = b"\x05"
                instruction_target = b"\x00\x00"
                if instruction["action"] == "on":
                    instruction_action = b"\x01"
                    instruction_measures = struct.pack(">I", instruction["measures"])
                else:
                    instruction_action = b"\x02"
                    instruction_measures = b"\x00\x00\x00\x00"
            elif instruction["type"] == "prepare":
                instruction_type = b"\x06"
                instruction_target = b"\x00\x00"
                instruction_action = b"\x00"
                instruction_measures = b"\x00\x00\x00\x00"
            elif instruction["type"] == "dish_out":
                instruction_type = b"\x07"
                instruction_target = b"\x00\x00"
                instruction_action = b"\x00"
                instruction_measures = b"\x00\x00\x00\x00"
            elif instruction["type"] == "finish":
                instruction_type = b"\x08"
                instruction_target = b"\x00\x00"
                instruction_action = b"\x00"
                instruction_measures = b"\x00\x00\x00\x00"
            elif instruction["type"] == "reset0":
                instruction_type = b"\x09"
                instruction_target = b"\x00\x00"
                instruction_action = b"\x00"
                instruction_measures = b"\x00\x00\x00\x00"
            elif instruction["type"] == "reset1":
                instruction_type = b"\x0a"
                instruction_target = b"\x00\x00"
                instruction_action = b"\x00"
                instruction_measures = b"\x00\x00\x00\x00"
            elif instruction["type"] == "wash":
                instruction_type = b"\x0b"
                instruction_target = b"\x00\x00"
                instruction_action = b"\x00"
                instruction_measures = b"\x00\x00\x00\x00"
            else:
                raise NameError("instruction type is wrong")
            self.data += instruction_type + instruction_target + instruction_action + instruction_measures \
                         + struct.pack(">I", instruction["time"])

        self.msg += self.data


class InquiryPacker:
    count = 1

    def __init__(self):
        self.msg = HEADER.encode()  # HEADER, 4 bytes
        self.data_info = b""
        InquiryPacker.count += 1

    def pack(self, model: bytes):
        self.msg += struct.pack(">I", 14)  # DATA_LENGTH, 4 bytes

        self.data_info += INQUIRY_DATA_HEADER.encode()  # DATA_HEADER, 3 bytes
        self.data_info += struct.pack(">I", self.count)  # DATA_NO, 4 bytes
        self.data_info += model  # DATA_SIGNAL, 1 byte
        self.data_info += b"\x00\x00"
        self.data_info += struct.pack(">I", int(time()))  # DATA_DATETIME, 4 bytes

        self.msg += self.data_info


class PLCCommandPacker:
    count = 1

    def __init__(self):
        self.msg = HEADER.encode()  # HEADER, 4 bytes
        self.data_info = b""
        self.data = b""
        PLCCommandPacker.count += 1

    def pack(self, command: dict):
        model = command["model"]
        instructions = command["instructions"]
        if len(instructions) == 0:
            raise NameError("instructions is empty")

        # DATA_INFO
        self.data_info += COMMAND_DATA_HEADER.encode()  # DATA_HEADER, 3 bytes
        self.data_info += struct.pack(">I", self.count)  # DATA_NO, 4 bytes
        self.data_info += b"\x01" if model == "single" else b"\x02" if model == "multiple" else b"\x03"
        self.data_info += struct.pack(">H", len(instructions))  # INSTRUCTION_COUNT, 2 bytes
        self.data_info += struct.pack(">I", int(time()))  # DATA_DATETIME, 4 bytes

        instruction_no = 1
        for instruction in instructions:
            self.data += struct.pack(">H", instruction_no)
            instruction_no += 1
            if instruction["type"] == "x":
                instruction_type = b"\x20"
                if instruction["action"] == "on":
                    instruction_target = struct.pack(">H", instruction["target"])
                    instruction_action = b"\x01"
                else:  # 复位
                    instruction_target = struct.pack(">H", 0)
                    instruction_action = b"\x02"
                instruction_measures = struct.pack(">I", 0)
            elif instruction["type"] == "y":
                instruction_type = b"\x21"
                if instruction["action"] == "on":
                    instruction_target = struct.pack(">H", instruction["target"])
                    instruction_action = b"\x01"
                else:  # 复位
                    instruction_target = struct.pack(">H", 0)
                    instruction_action = b"\x02"
                instruction_measures = struct.pack(">I", 0)
            elif instruction["type"] == "r":
                instruction_type = b"\x22"
                if instruction["action"] == "on":
                    instruction_target = struct.pack(">H", instruction["target"])
                    instruction_action = b"\x01"
                    instruction_measures = struct.pack(">I", instruction["measures"][0])
                else:  # 停转
                    instruction_target = struct.pack(">H", 0)
                    instruction_action = b"\x02"
                    instruction_measures = struct.pack(">I", 0)
            elif instruction["type"] == "liquid_pump":
                instruction_type = b"\x23"
                instruction_target = struct.pack(">H", instruction["target"])
                instruction_action = b"\x00"
                instruction_measures = struct.pack(">I", instruction["measures"][0])
            elif instruction["type"] == "solid_pump":
                instruction_type = b"\x24"
                instruction_target = struct.pack(">H", instruction["target"])
                instruction_action = b"\x00"
                instruction_measures = struct.pack(">I", instruction["measures"][0])
            elif instruction["type"] == "water_pump":
                instruction_type = b"\x25"
                instruction_target = struct.pack(">H", instruction["target"])
                instruction_action = b"\x00"
                instruction_measures = struct.pack(">I", instruction["measures"][0])
            elif instruction["type"] == "shake":
                instruction_type = b"\x26"
                instruction_target = struct.pack(">H", 0)
                instruction_action = b"\x00"
                instruction_measures = struct.pack(">I", instruction["measures"][0])
            elif instruction["type"] == "temperature":
                instruction_type = b"\x27"
                instruction_target = struct.pack(">H", 0)
                if instruction["action"] == "on":
                    instruction_action = b"\x01"
                    instruction_measures = struct.pack(">I", instruction["measures"][0])
                else:  # 关闭
                    instruction_action = b"\x02"
                    instruction_measures = struct.pack(">I", 0)
            elif instruction["type"] == "setting_x":
                instruction_type = b"\x50"
                instruction_target = struct.pack(">H", 0)
                instruction_action = b"\x00"
                instruction_measures = struct.pack(">I", instruction["measures"][0])
            elif instruction["type"] == "setting_y":
                instruction_type = b"\x51"
                instruction_target = struct.pack(">H", 0)
                instruction_action = b"\x00"
                instruction_measures = struct.pack(">I", instruction["measures"][0])
            elif instruction["type"] == "setting_r":
                instruction_type = b"\x52"
                instruction_target = struct.pack(">H", 0)
                instruction_action = b"\x00"
                instruction_measures = struct.pack(">H", instruction["measures"][0]) \
                                       + struct.pack(">H", instruction["measures"][1])
            elif instruction["type"] == "setting_shake":
                instruction_type = b"\x53"
                instruction_target = struct.pack(">H", 0)
                instruction_action = b"\x00"
                instruction_measures = struct.pack(">H", instruction["measures"][0]) \
                                       + struct.pack(">H", instruction["measures"][1])
            elif instruction["type"] == "setting_temperature":
                instruction_type = b"\x54"
                instruction_target = struct.pack(">H", 0)
                instruction_action = b"\x00"
                instruction_measures = struct.pack(">H", instruction["measures"][0]) \
                                       + struct.pack(">H", instruction["measures"][1])
            else:
                raise NameError("instruction type error")
            self.data += instruction_type + instruction_target + instruction_action + instruction_measures \
                         + struct.pack(">I", int(instruction["time"]))
        data_length = len(self.data)
        self.msg += struct.pack(">I", 14 + data_length)  # DATA_LENGTH, 4 bytes
        self.msg += self.data_info
        self.msg += self.data


class StateRequestPacker:
    count = 1

    def __init__(self):
        self.msg = HEADER.encode()  # HEADER, 4 bytes
        self.data_info = b""
        StateRequestPacker.count += 1

    def pack(self):
        self.msg += struct.pack(">I", 14)  # DATA_LENGTH, 4 bytes

        self.data_info += STATE_REQUEST_DATA_HEADER.encode()  # DATA_HEADER, 3 bytes
        self.data_info += struct.pack(">I", self.count)  # DATA_NO, 4 bytes
        self.data_info += b"\x00"  # DATA_SIGNAL, 1 byte
        self.data_info += b"\x00\x00"
        self.data_info += struct.pack(">I", int(time()))  # DATA_DATETIME, 4 bytes

        self.msg += self.data_info


if __name__ == "__main__":
    p = CommandPacker()
    p2 = CommandPacker()
    p3 = CommandPacker()
    print(p3.count)
    print(p.msg)
    print(p.len)
