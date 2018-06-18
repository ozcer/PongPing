import logging
import socket
import threading
from pprint import pprint


class Server:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '0.0.0.0'
        port = 5000
        self.sock.bind((host, port))
        self.sock.listen(1)

        self.con1 = None
        self.con2 = None
        self.username1 = 'username1'
        self.username2 = 'username2'

    def handler(self, connection, address):
        while True:
            try:
                data = connection.recv(1024)
            except ConnectionResetError:
                self.remove_connection(connection)
                connection.close()
                break
            msgs = data.decode("utf-8")
            print(f'received: {msgs} from {connection.getpeername()}')
            for msg in msgs.split('|')[:-1]:
                parts = msg.split()
                print(f"parsing: {parts}")
                # initialization
                if parts[0] == 'iam':
                    username = parts[1]
                    if connection == self.con1:
                        self.username1 = username
                    elif connection == self.con2:
                        self.username2 = username

                    self.send_all(f'id player1 {self.username1}')
                    self.send_all(f'id player2 {self.username2}')
                elif parts[1] == 'win':
                    self.send_all(data, encoded=True)
                else:
                    self.send_other(data, connection, encoded=True)

    def run(self):
        print("Server running")
        while True:
            con, adr = self.sock.accept()
            self.add_connection(con)
            con_thread = threading.Thread(target=self.handler, args=(con, adr))
            con_thread.daemon = True
            con_thread.start()


    def add_connection(self, connection):
        print(f"{connection.getpeername()} connected")
        if self.con1 is None:
            self.con1 = connection
            self._send_msg('ur player1', self.con1)
        elif self.con2 is None:
            self.con2 = connection
            self._send_msg('ur player2', self.con2)
        else:
            raise Exception("LOBBY FULL")

    def remove_connection(self, connection):
        if self.con1 == connection:
            n = 1
            self.con1 = None
        elif self.con2 == connection:
            n = 2
            self.con2 = None
        else:
            raise Exception("NO SUCH CONNECTION CONNECTED")

        print(f"{connection.getpeername()} disconnected as player{n}")

    def send_other(self, payload, connection, encoded=False):
        if connection == self.con1 and self.con2:
            self._send_msg(payload, self.con2, encoded=encoded)
        elif connection == self.con2 and self.con1:
            self._send_msg(payload, self.con1, encoded=encoded)

    def send_all(self, payload, encoded=False):
        if self.con1:
            self._send_msg(payload, connection=self.con1, encoded=encoded)
        if self.con2:
            self._send_msg(payload, connection=self.con2, encoded=encoded)

    @staticmethod
    def _send_msg(payload, connection, encoded=False):
        if encoded:
            _data = payload
        else:
            _data = (payload + '|').encode('utf-8')

        print(f"sending: {_data.decode('utf-8')} to {connection.getpeername()}")
        connection.send(_data)


if __name__ == "__main__":
    s = Server()
    s.run()
