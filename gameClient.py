import socket
import pickle
from threading import Thread
from gameWindow import GameWindow
import pygame
import sys
import json

class OnlineGame():
    def __init__(self, main=None):
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
            self.cmd = self.client.serverMsg(self.cmd)


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
            self.window.sign = self.client.sign
            self.window.initSurface()
            self.window.initScoreBoard()

            while self.client.connected:

                if self.client.lMove != None:
                    self.window.showMove(self.client.lMove[1], self.client.lMove[0])
                    self.client.lMove = None

                if self.client.score != None:
                    self.window.score = self.client.score
                    self.window.deleteScoreText()
                    self.window.initScores()

                if self.client.winner != None:
                    self.window.gameOver(self.client.winner)
                    self.window.winner = self.client.winner
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
        self.score = [0, 0]
        self.sign = None
        self.winner = None

    def initScores(self):
        self.screen.blit(pygame.font.SysFont("comicsansms", 60).render(str(self.score[0]), True, (255, 255, 255)),
                         (53, 470))
        self.screen.blit(pygame.font.SysFont("comicsansms", 60).render(str(self.score[1]), True, (255, 255, 255)),
                         (338, 470))

    def deleteScoreText(self):
        dark_gray = (12, 15, 10)
        rect1 = pygame.Rect(30, 480, 70, 85)
        pygame.draw.rect(self.screen, dark_gray, rect1)
        rect2 = pygame.Rect(310, 480, 70, 85)
        pygame.draw.rect(self.screen, dark_gray, rect2)

    def initScoreBoard(self):
        if self.game.player1.getName() == None:
            player1Text = "You"
        else: player1Text = self.game.player1.getName()

        if self.game.player2.getName() == None:
            player2Text = "Opponent"
        else: player2Text = self.game.player2.getName()

        if self.sign == "X":
            player1Label = pygame.font.SysFont("comicsansms", 27).render(player1Text, True, (255, 32, 110))
            player2Label = pygame.font.SysFont("comicsansms", 27).render(player2Text, True, (65, 234, 212))

        else:
            player1Label = pygame.font.SysFont("comicsansms", 27).render(player1Text, True, (65, 234, 212))
            player2Label = pygame.font.SysFont("comicsansms", 27).render(player2Text, True, (255, 32, 110))

        turn = lambda x: "0" if x == "X" else "X"
        self.turn = turn(self.winner)
        if self.turn == "X":
            color = (255, 32, 110)
        else:
            color = (65, 234, 212)

        text = self.turnText.render(self.turn, True, color)
        self.screen.blit(text, ((self.WIDTH - 50) / 2, 470))
        self.screen.blit(player1Label, (45, 440))
        self.screen.blit(player2Label, (290, 440))
        self.initScores()


class GameClient():
    def __init__(self):
        self.port = 0
        self.ip = ""
        self.format = "utf-8"
        self.readData("clientInf.json")
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.game_code = "!gameCodeStart"
        self.connected = False
        self.turn = None
        self.sign = None
        self.lMove = None
        self.winner = None
        self.board = None
        self.score = [0, 0]

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

    def serverMsg(self, msg):
        if msg == "!cc":
            self.sendMessage("!ctd")

        elif msg == "!board":
            self.board = self.recvObject()
            self.showBoard()

        elif msg == "!sgn":
            self.sign = self.recvMessage()
            return "!sgn"

        elif msg == "!gameTurn":
            self.turn = int(self.recvMessage())

        elif msg == "!winner":
            self.winner = self.recvMessage()

        elif msg == "!score":
            self.score = self.recvObject()

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

    def start(self):
        while self.connected:
            try:
                msg = self.recvMessage()
                self.serverMsg(msg)
            except ConnectionResetError:
                print("Server error")
                self.connected = False