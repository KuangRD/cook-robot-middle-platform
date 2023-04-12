import socket

client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
client.bind(('127.0.0.1', 10020))

if __name__ == "__main__":
    while 1:
        msg, addr = client.recvfrom(1024)
