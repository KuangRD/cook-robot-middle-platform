import struct
from time import time

HEADER = "COOK"
COMMAND_DATA_HEADER = "CCS"
INQUIRY_DATA_HEADER = "CIS"


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
        data_length = 14 * len(instructions)
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
                    if instruction["target"] == "forward":  # 正转
                        instruction_target = struct.pack(">H", 1)
                    elif instruction["target"] == "reverse":  # 反转
                        instruction_target = struct.pack(">H", 2)
                    else:  # 正反转
                        instruction_target = struct.pack(">H", 3)
                    instruction_action = b"\x01"
                    instruction_measures = struct.pack(">B", instruction["measures"][0]) \
                                           + struct.pack(">B", instruction["measures"][1]) + struct.pack(">H", 0)
                else:  # 停转
                    instruction_target = struct.pack(">H", 0)
                    instruction_action = b"\x02"
                    instruction_measures = struct.pack(">I", 0)
            elif instruction["type"] == "pump":
                instruction_type = b"\x23"
                instruction_target = struct.pack(">H", 0)
                instruction_action = b"\x00"
                instruction_measures = struct.pack(">I", instruction["measures"][0])
            elif instruction["type"] == "shake":
                instruction_type = b"\x24"
                instruction_target = struct.pack(">H", 0)
                instruction_action = b"\x00"
                instruction_measures = struct.pack(">B", instruction["measures"][0]) \
                                       + struct.pack(">B", instruction["measures"][1]) \
                                       + struct.pack(">B", instruction["measures"][2]) + struct.pack(">B", 0)
            elif instruction["type"] == "temperature":
                instruction_type = b"\x25"
                instruction_target = struct.pack(">H", 0)
                if instruction["action"] == "on":
                    instruction_action = b"\x01"
                    instruction_measures = struct.pack(">I", instruction["measures"][0])
                else:  # 关闭
                    instruction_action = b"\x02"
                    instruction_measures = struct.pack(">I", 0)
            else:
                raise NameError("instruction type error")
            self.data += instruction_type + instruction_target + instruction_action + instruction_measures \
                         + struct.pack(">I", int(instruction["time"]))
        data_length = len(self.data)
        print(data_length)
        self.msg += struct.pack(">I", data_length)  # DATA_LENGTH, 4 bytes
        self.msg += self.data_info
        self.msg += self.data


# class PLCCommandPacker:
#     count = 1
#
#     def __init__(self):
#         self.msg = HEADER.encode()  # HEADER, 4 bytes
#         self.data_info = b""
#         self.data = b""
#         PLCCommandPacker.count += 1
#
#     def pack(self, command: dict):
#         model = command["model"]
#         instructions = command["instructions"]
#         if len(instructions) == 0:
#             raise NameError("instructions is empty")
#
#         # DATA_INFO
#         self.data_info += COMMAND_DATA_HEADER.encode()  # DATA_HEADER, 3 bytes
#         self.data_info += struct.pack(">I", self.count)  # DATA_NO, 4 bytes
#         self.data_info += b"\x01" if model == "single" else b"\x02" if model == "multiple" else b"\x03"
#         self.data_info += struct.pack(">H", len(instructions))  # INSTRUCTION_COUNT, 2 bytes
#         self.data_info += struct.pack(">I", int(time()))  # DATA_DATETIME, 4 bytes
#
#         for instruction in instructions:
#             if instruction["type"] == "x":
#                 if instruction["action"] == "on":
#                     # D20=1,D22=target
#                     address_number = struct.pack(">B", 2)  # 1 byte
#                     address_no_1 = struct.pack(">H", 20)  # 2 bytes
#                     address_value_1 = struct.pack(">H", 1)  # 2 bytes
#                     address_no_2 = struct.pack(">H", 22)  # 2 bytes
#                     address_value_2 = struct.pack(">H", int(instruction["target"]))  # 2 bytes
#                     self.data += address_number + address_no_1 + address_value_1 + address_no_2 + address_value_2
#                 else:
#                     # 复位 D2=1
#                     address_number = struct.pack(">B", 1)  # 1 byte
#                     address_no_1 = struct.pack(">H", 2)  # 2 bytes
#                     address_value_1 = struct.pack(">H", 1)  # 2 bytes
#                     self.data += address_number + address_no_1 + address_value_1
#             elif instruction["type"] == "y":
#                 if instruction["action"] == "on":
#                     # D10=1,D12=target
#                     address_number = struct.pack(">B", 2)  # 1 byte
#                     address_no_1 = struct.pack(">H", 10)  # 2 bytes
#                     address_value_1 = struct.pack(">H", 1)  # 2 bytes
#                     address_no_2 = struct.pack(">H", 12)  # 2 bytes
#                     address_value_2 = struct.pack(">H", int(instruction["target"]))  # 2 bytes
#                     self.data += address_number + address_no_1 + address_value_1 + address_no_2 + address_value_2
#                 else:
#                     # 复位 D0=1
#                     address_number = struct.pack(">B", 1)  # 1 byte
#                     address_no_1 = struct.pack(">H", 0)  # 2 bytes
#                     address_value_1 = struct.pack(">H", 1)  # 2 bytes
#                     self.data += address_number + address_no_1 + address_value_1
#             elif instruction["type"] == "r":
#                 if instruction["action"] == "on":
#                     # 开始转动
#                     address_number = struct.pack(">B", 2)  # 1 byte
#                     address_no_1 = struct.pack(">H", 4)  # 2 bytes
#                     address_value_1 = struct.pack(">H", 1)  # 2 bytes
#                     address_no_2 = struct.pack(">H", 6)  # 2 bytes
#                     if instruction["target"] == "forward":
#                         # 正转，D4=1,D6=1,**D8=speed,D10=circles**
#                         address_value_2 = struct.pack(">H", 1)  # 2 bytes
#                     elif instruction["target"] == "reverse":
#                         # 反转，D4=1,D6=2,**D8=speed,D10=circles**
#                         address_value_2 = struct.pack(">H", 2)  # 2 bytes
#                     else:
#                         # 正反转，D4=1,D6=3,**D8=speed,D10=circles**
#                         address_value_2 = struct.pack(">H", 3)  # 2 bytes
#                     self.data += address_number + address_no_1 + address_value_1 + address_no_2 + address_value_2
#                 else:
#                     # 停止转动 D4=0
#                     address_number = struct.pack(">B", 1)  # 1 byte
#                     address_no_1 = struct.pack(">H", 4)  # 2 bytes
#                     address_value_1 = struct.pack(">H", 0)  # 2 bytes
#                     self.data += address_number + address_no_1 + address_value_1
#             elif instruction["type"] == "pump":
#                 # D40=1,D42=target,D44=period
#                 address_number = struct.pack(">B", 3)  # 1 byte
#                 address_no_1 = struct.pack(">H", 40)  # 2 bytes
#                 address_value_1 = struct.pack(">H", 1)  # 2 bytes
#                 address_no_2 = struct.pack(">H", 42)  # 2 bytes
#                 address_value_2 = struct.pack(">H", int(instruction["target"]))  # 2 bytes 单位0.1s
#                 address_no_3 = struct.pack(">H", 44)  # 2 bytes
#                 address_value_3 = struct.pack(">H", instruction["measures"][0])  # 2 bytes
#                 self.data += address_number + address_no_1 + address_value_1 + address_no_2 + address_value_2 + address_no_3 + address_value_3
#             elif instruction["type"] == "shake":
#                 # D30=1,D34=count,up_speed,down_speed
#                 address_number = struct.pack(">B", 2)  # 1 byte
#                 address_no_1 = struct.pack(">H", 30)  # 2 bytes
#                 address_value_1 = struct.pack(">H", 1)  # 2 bytes
#                 address_no_2 = struct.pack(">H", 34)  # 2 bytes
#                 address_value_2 = struct.pack(">H", instruction["measures"][0])  # 2 bytes 单位0.1s
#                 self.data += address_number + address_no_1 + address_value_1 + address_no_2 + address_value_2
#             else:
#                 raise NameError("instruction type error")
#             self.data += struct.pack(">I", int(instruction["time"]))  # 4 bytes
#         data_length = len(self.data)
#         self.msg += struct.pack(">I", data_length)  # DATA_LENGTH, 4 bytes
#         self.msg += self.data_info
#         self.msg += self.data


if __name__ == "__main__":
    p = CommandPacker()
    p2 = CommandPacker()
    p3 = CommandPacker()
    print(p3.count)
    print(p.msg)
    print(p.len)
