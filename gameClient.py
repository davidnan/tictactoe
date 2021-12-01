import socket
import pickle
from threading import Thread
from gameWindow import GameWindow
import pygame, sys
import json

class OnlineGame():
    def __init__(self, main):
        self.main = main
        self.window = None
        self.client = GameClient()
        self.cmd = None
        self.usedCmd = False
        self.inGame = True
        self.recvThread = Thread(target=self.recv)
        self.recvThread.daemon = True

    def recv(self):
        while self.client.connected:
            self.cmd = self.client.recvMessage()
            self.cmd = self.client.serverMsg(self.cmd, self.main)

    def mouseClick(self, coords):
        if coords[1] < 420:
            coords[0] = (coords[0] // 140 * 140 + 70) // 140
            coords[1] = (coords[1] // 140 * 140 + 70) // 140
            self.client.sendObject(coords)

    def run(self, *args):
        if args != None:
            self.x, self.y = args
        if self.client.game_code != "000000":
            self.recvThread.start()
            self.window = OnlineGameWindow(self.x, self.y)
            self.window.initSurface()
            self.window.initScoreBoard()

            while self.client.connected:

                if self.client.lMove != None:
                    self.window.showMove(self.client.lMove[1], self.client.lMove[0])
                    self.client.lMove = None
                if self.client.winner != None:
                    self.window.gameOver(self.client.winner)
                    self.client.winner = None
                if self.cmd == "!ed":
                    self.main.app.exec_()
                    self.client.connected = False

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.client.connected = False
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN and self.client.turn == 1:
                        mouse = pygame.mouse.get_pos()
                        coords = list(mouse)
                        self.mouseClick(coords)

                pygame.display.update()


class OnlineGameWindow(GameWindow):
    def __init__(self, x, y):
        super().__init__(x, y)

class GameClient():
    def __init__(self):
        self.port = 0
        self.ip = ""
        self.format = "utf-8"
        self.readData("clientInf.json")
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.game_code = "000000"
        self.connected = False
        self.turn = None
        self.sign = None
        self.lMove = None
        self.winner = None

    def readData(self, file):
        with open(file) as f:
            data = json.load(f)
        self.ip = data['ip']
        self.port = data['port']

    def resetSocket(self):
        self.closeConnection()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, game_code):
        if not self.connected:
            self.client.connect((self.ip, self.port))
            self.connected = True
        self.sendMessage(game_code)
        if game_code == "000000":
            game_code = self.recvMessage()
            self.game_code = game_code
            return game_code
        else:
            isCodeValid = self.recvMessage()
            return isCodeValid

    def gameStart(self):
        secondJoined = False
        while not secondJoined:
            msg = self.recvMessage()
            if msg == "!sg":
                secondJoined = True
        return True

    def closeConnection(self):
        self.connected = False
        self.client.close()

    def showBoard(self):
        for i in range(0, 3):
            print(self.board[i])

    def recvMessage(self):
        msg_length = self.client.recv(64).decode(self.format)
        if msg_length:
            msg_length = int(msg_length)
            msg = self.client.recv(msg_length)
            msg = msg.decode(self.format)
            return msg

    def sendMessage(self, message):
        # Sending a message to the client to send the nickname
        message = (message.encode(self.format))
        message_length = str(len(message)).encode(self.format)
        message_length += b' ' * (64 - len(message_length))
        self.client.send(message_length)
        self.client.send(message)

    def sendObject(self, obj):
        obj = pickle.dumps(obj)
        length = str(len(obj)).encode(self.format)
        length += b' ' * (64 - len(length))
        self.client.send(length)
        self.client.send(obj)

    def recvObject(self):
        length = self.client.recv(64).decode(self.format)
        if length:
            length = int(length)
            obj = pickle.loads(self.client.recv(length))
            return obj

    def sendMove(self, args):
        move = args
        if (0 <= move[0] < 3 and 0 <= move[1] < 3):
            self.sendObject(move)
            validMove = "!valid"
        else:
            validMove = "!notvalid"

        while validMove != "!valid":
            move = []
            x = int(input("row: "))  # move
            move.append(x)
            x = int(input("column: "))  # input
            move.append(x)
            if (0 <= move[0] < 3 and 0 <= move[1] < 3) and move[0] != None and move[1] != None:
                self.sendObject(move)
                validMove = self.recvMessage()
            else:
                validMove = "!notvalid"

    def serverMsg(self, msg, main=None):
        if msg == "!cc":
            self.sendMessage("!ctd")

        elif msg == "!board":
            self.board = self.recvObject()
            self.showBoard()

        elif msg == "!sgn":
            self.sign = self.recvMessage()

        elif msg == "!rqtmove":
            return "!rqtmove"

        elif msg == "!gameTurn":
            self.turn = int(self.recvMessage())

        elif msg == "!winner":
            self.winner = self.recvMessage()

        elif msg == "!dc":
            self.connected = False
            return "!dc"

        elif msg == "!ig":
            self.sendMessage("!cig")

        elif msg == "!move":
            self.lMove = self.recvObject()
            self.lMove[1][0] = self.lMove[1][0] * 140 + 70
            self.lMove[1][1] = self.lMove[1][1] * 140 + 70

        elif msg == "!ed":
            return "!ed"

        elif msg != None:
            print(msg)

    def start(self):
        while self.connected:
            try:
                msg = self.recvMessage()
                self.serverMsg(msg)
            except ConnectionResetError:
                print("Server error")
                self.connected = False


if __name__ == "__main__":
    # game = GameClient()
    # game.start()
    # game_code = input("Game code: ")
    game = OnlineGame()
    game.run()
