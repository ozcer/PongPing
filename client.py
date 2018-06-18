import socket
import threading
import time

from src.const import *


class Client:

    def __init__(self, game, addr, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = USERNAME
        self.connect_server(addr, port)

        input_thread = threading.Thread(target=self.receive_msg)
        input_thread.daemon = True
        input_thread.start()

        self.game = game

    def connect_server(self, addr, port):
        while True:
            try:
                self.sock.connect((addr, port))
                print(f"connected to server at {self.sock.getpeername()}")
                self.send_msg(f'iam {self.username}')
                break
            except ConnectionRefusedError:
                print("Failed to connect to server. Re-attempt in 5 sec")
                time.sleep(5)

    def send_msg(self, msg):
        _msg = msg + '|'
        print(f"sending: {_msg}")
        self.sock.send(_msg.encode("utf-8"))

    def receive_msg(self):
        while True:
            try:
                data = self.sock.recv(1024).decode("utf-8")
            except ConnectionResetError:
                raise ConnectionResetError('Server disconnected')
            print(f"received: {data}")
            for msg in data.split('|')[:-1]:
                parts = msg.split()
                print(f"parsing: {parts}")
                # initialization
                if parts[0] == 'ur':
                    if parts[1] == 'player1':
                        self.game.p1.image.fill(D_BLUE)
                        self.game.control_type = 1
                    elif parts[1] == 'player2':
                        self.game.p2.image.fill(D_BLUE)
                        self.game.control_type = 2

                # gameplay
                elif parts[0] == 'p0':
                    self.game.p1.x = float(parts[1])
                    self.game.p1.y = float(parts[2])
                elif parts[0] == 'p1':
                    self.game.p2.x = float(parts[1])
                    self.game.p2.y = float(parts[2])
                elif parts[0] == 'b':
                    self.game.ball.dx = int(parts[1])
                    self.game.ball.dy = int(parts[2])

                elif parts[0] == 'id':
                    username = parts[2]
                    if parts[1] == 'player1':
                        self.game.username1 = username
                    elif parts[1] == 'player2':
                        self.game.username2 = username

                elif parts[0] == 'win':
                    if parts[1] == 'player1':
                        self.game.point1 += 1
                    elif parts[1] == 'player2':
                        self.game.point2 += 1

                    self.game.ball.reset()

                elif parts[0] == 'ball':
                    self.game.ball.x = float(parts[1])
                    self.game.ball.y = float(parts[2])
