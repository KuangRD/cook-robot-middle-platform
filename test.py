import base64
import struct

if __name__ == "__main__":

    crc16 = b"D5CA"
    print(crc16)
    print(int(crc16, base=16))

    print(b"0x"+crc16)


