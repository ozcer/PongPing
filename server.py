import logging
import socket
import threading
from pprint import pprint


class Server:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('', 8008))
        self.sock.listen(1)

        self.con1 = None
        self.con2 = None

    def handler(self, connection, address):
        while True:
            data = connection.recv(1024)
            print(f'received: {data.decode("utf-8")}')
            self.send_other(connection, data)
            if not data:
                self.remove_connection(connection)
                connection.close()
                break

    def run(self):
        print("running server...")
        while True:
            con, adr = self.sock.accept()
            con_thread = threading.Thread(target=self.handler, args=(con, adr))
            con_thread.daemon = True
            con_thread.start()
            self.add_connection(con)

    def add_connection(self, connection):
        print(f"{connection} connected")
        if self.con1 is None:
            self.con1 = connection
        elif self.con2 is None:
            self.con2 = connection
        else:
            raise Exception("LOBBY FULL")

    def remove_connection(self, connection):
        print(f"{connection} disconnected")
        if self.con1 == connection:
            self.con1 = None
            if self.con2 == connection:
                self.con2 = None
        else:
            raise Exception("NO SUCH CONNECTION CONNECTED")

    def send_other(self, connection, data):
        logging.warning(f"sending {data}")
        if connection == self.con1:
            self.con2.send(bytes(data))
        else:
            self.con1.send(bytes(data))


if __name__ == "__main__":
    s = Server()
    s.run()