import socket
import threading


class Client:

    def __init__(self, game, adrs, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((adrs, port))

        input_thread = threading.Thread(target=self.receive_msg)
        input_thread.daemon = True
        input_thread.start()

        self.game = game

    def send_msg(self, msg):
        _msg = msg + '|'
        print(f"sending: {_msg}")
        self.sock.send(_msg.encode("utf-8"))

    def receive_msg(self):
        while True:
            data = self.sock.recv(1024).decode("utf-8")
            print(f"received: {data}")
            if data:
                for msg in data.split('|')[:-1]:
                    print(f"parsing {msg}")
                    parts = msg.split()
                    print(f"parts: {parts}")
                    if parts[0] == 'p0':
                        self.game.p1.x = float(parts[1])
                        self.game.p1.y = float(parts[2])
                    elif parts[0] == 'p1':
                        self.game.p2.x = float(parts[1])
                        self.game.p2.y = float(parts[2])
                    elif parts[0] == 'b':
                        self.game.ball.dx = int(parts[1])
                        self.game.ball.dy = int(parts[2])
            else:
                break
