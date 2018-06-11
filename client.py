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
        print(f"sending: {msg}")
        self.sock.send(msg.encode("utf-8"))

    def receive_msg(self):
        while True:
            data = self.sock.recv(1024).decode("utf-8")
            print(f"received: {data}")
            if data == "1u":
                self.game.p1.move("up")
            elif data == "1d":
                self.game.p1.move("down")
            elif data == "2u":
                self.game.p2.move("up")
            elif data == "2d":
                self.game.p2.move("down")
            elif data[0] == "k":
                _, x, y = data.split()
                self.game.ball.dx = int(x)
                self.game.ball.dy = int(y)

            if not data:
                break
