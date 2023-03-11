import socket
import threading
import time


class Server:
    def __init__(self):
        self.server = None
        self.host = "127.0.0.1"
        self.port = 9999
        self.buff_size = 1024

    def run(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(1)

        while True:
            conn, addr = self.server.accept()
            t = threading.Thread(target=self.task, args=(conn,))
            t.start()

    def task(self, conn: socket.socket):
        while True:
            data = conn.recv(self.buff_size)
            print(data)
            if len(data) == 0:
                print("quit")
                break
        conn.close()


if __name__ == "__main__":
    server = Server()
    server.run()
