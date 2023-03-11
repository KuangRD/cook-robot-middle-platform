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
        self.data_info += b"\x01" if model == "single" else b"\x02"  # INSTRUCTION_MODEL, 1 byte
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
            elif instruction["type"] == "water":
                instruction_type = b"\x02"
            elif instruction["type"] == "seasoning":
                instruction_type = b"\x03"
            elif instruction["type"] == "fire":
                instruction_type = b"\x04"
            elif instruction["type"] == "stir_fry":
                instruction_type = b"\x05"
            else:
                raise NameError("instruction type is wrong")
            self.data += instruction_type

            if instruction["type"] in ["ingredient", "seasoning"]:
                instruction_target = struct.pack(">H", instruction["target"])
            else:
                instruction_target = b"\x00\x00"
            self.data += instruction_target

            if instruction["action"] == "off":
                instruction_action = b"\x01"
            elif instruction["action"] == "on":
                instruction_action = b"\x02"
            elif instruction["action"] == "open":
                instruction_action = b"\x03"
            else:
                raise NameError("instruction action is wrong")
            self.data += instruction_action

            if (instruction["type"] in ["ingredient", "seasoning", "fire", "stir_fry"]) and \
                    instruction["action"] == "on":
                instruction_measure = struct.pack(">I", instruction["measure"])
            else:
                instruction_measure = b"\x00\x00\x00\x00"
            self.data += instruction_measure

            self.data += struct.pack(">I", instruction["time"])
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


if __name__ == "__main__":
    p = CommandPacker()
    p2 = CommandPacker()
    p3 = CommandPacker()
    print(p3.count)
    print(p.msg)
    print(p.len)
