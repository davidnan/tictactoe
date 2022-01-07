import socket, pickle, random
from threading import Thread
from game import Game
import json
from player import Player

class PlayerServer(Player):
    def __init__(self):
        super().__init__()
        self.game_code = "000000"
        self.connection = None

    def setCode(self, game_code): self.game_code = game_code
    def getCode(self): return self.game_code
    def setConnection(self, conn): self.connection = conn
    def getConnection(self): return self.connection

class GameSever(Game):
    def __init__(self, conn):
        super().__init__()
        self.player1 = PlayerServer()
        self.setPlayer1Connection(conn)
        self.player2 = PlayerServer()
        self.game_code = '000000'
        self.game_started = False
        self.setPlayer1Ch("X")
        self.setPlayer2Ch("0")
        self.last_start_turn = 1

    def closeConnections(self):
        self.getPlayer1Connection().close()
        self.getPlayer2Connection().close()

    def turnOnGame(self): self.game_started = True
    def turnOffGame(self): self.game_started = False
    def isGameOn(self): return self.game_started
    def setPlayer1Connection(self, conn): self.player1.setConnection(conn)
    def setPlayer2Connection(self, conn): self.player2.setConnection(conn)
    def getPlayer1Connection(self): return self.player1.getConnection()
    def getPlayer2Connection(self): return self.player2.getConnection()
    def getCode(self): return self.game_code
    def setCode(self, code): self.game_code = code
    def setPlayer1Ch(self, ch): self.player1.setCh(ch)
    def setPlayer2Ch(self, ch): self.player2.setCh(ch)
    def getPlayer1Ch(self): return self.player1.getCh()
    def getPlayer2Ch(self): return self.player2.getCh()

class Server():
    def __init__(self):
        # Server information
        self.ip = ""
        self.port = 0
        self.format = "utf-8"
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.games = []
        self.readData("serverInf.json")

        self.server.bind((self.ip, self.port))
        self.server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        self.start()

    def readData(self, file):
        with open(file) as f:
            data = json.load(f)
        self.ip = data['ip']
        self.port = data['port']

    def recvMessage(self, conn):
        msg_length = conn.recv(64).decode(self.format)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(self.format)
            return msg

    def sendMessage(self, conn, message):
        # Sending a message to the client to send the nickname
        message = (message.encode(self.format))
        message_length = str(len(message)).encode(self.format)
        message_length += b' ' * (64 - len(message_length))
        conn.send(message_length)
        conn.send(message)

    def sendObject(self, conn, obj):
        obj = pickle.dumps(obj)
        length = str(len(obj)).encode(self.format)
        length += b' ' * (64 - len(length))
        conn.send(length)
        conn.send(obj)

    def recvObject(self, conn):
        length = conn.recv(64).decode(self.format)
        if length:
            length = int(length)
            obj = pickle.loads(conn.recv(length))
            return obj

    def showBoard(self, game):
        for i in range(0, 3):
            print(game.board[i])

    def checkConnection(self, conn):
        self.sendMessage(conn, "!cc")
        cc = self.recvMessage(conn)
        if cc == "!ctd":
            return True
        return False

    def checkInGame(self, conn):
        self.sendMessage(conn, "!ig")
        ig = self.recvMessage(conn)
        if ig == "!cig":
            return True
        return False

    def sendMove(self, conn, player, coords):
        move = [player, coords]
        self.sendMessage(conn, "!move")
        self.sendObject(conn, move)

    def sendBoard(self, game):
        self.sendMessage(game.getPlayer1Connection(), "!board")
        self.sendMessage(game.getPlayer2Connection(), "!board")
        self.sendObject(game.getPlayer1Connection(), game.board)
        self.sendObject(game.getPlayer2Connection(), game.board)

    def sendSigns(self, game):
        self.sendMessage(game.getPlayer1Connection(), "!sgn")
        self.sendMessage(game.getPlayer2Connection(), "!sgn")
        self.sendMessage(game.getPlayer1Connection(), game.getPlayer1Ch())
        self.sendMessage(game.getPlayer2Connection(), game.getPlayer2Ch())

    def requestMove(self, game, conn):
        self.sendMessage(conn, "!rqtmove")
        move = self.recvObject(conn)
        while not game.emptySpace(move):
            move = self.recvObject(conn)
        return move

    def sendTurn(self, game):
        self.sendMessage(game.getPlayer1Connection(), "!gameTurn")
        self.sendMessage(game.getPlayer2Connection(), "!gameTurn")
        if game.turn == 1:
            self.sendMessage(game.getPlayer1Connection(), "0")
            self.sendMessage(game.getPlayer2Connection(), "1")
            game.turn = 2
        elif game.turn == 2:
            self.sendMessage(game.getPlayer1Connection(), "1")
            self.sendMessage(game.getPlayer2Connection(), "0")
            game.turn = 1

    def sendWinner(self, game, winner):
        self.sendMessage(game.getPlayer1Connection(), "!winner")
        self.sendMessage(game.getPlayer2Connection(), "!winner")
        self.sendMessage(game.getPlayer1Connection(), winner)
        self.sendMessage(game.getPlayer2Connection(), winner)
        self.sendMessage(game.getPlayer1Connection(), "!score")
        self.sendMessage(game.getPlayer2Connection(), "!score")

        if game.player1.getCh() == winner:
            game.player1.incrementScore()
            self.sendObject(game.getPlayer1Connection(), [game.player1.getScore(), game.player2.getScore()])
            self.sendObject(game.getPlayer2Connection(), [game.player2.getScore(), game.player1.getScore()])
        else:
            game.player2.incrementScore()
            self.sendObject(game.getPlayer2Connection(), [game.player2.getScore(), game.player1.getScore()])
            self.sendObject(game.getPlayer1Connection(), [game.player1.getScore(), game.player2.getScore()])


    def gameEnd(self, game, winner):
        print(winner)
        game.resetBoard()
        self.sendWinner(game, winner)
        if game.last_start_turn == 2:
            game.last_start_turn = 1
            game.turn = 1
        elif game.last_start_turn == 1:
            game.last_start_turn = 2
            game.turn = 2
        self.sendTurn(game)

    def recvCode(self, conn):
        valid = False
        while not valid:
            game_code = self.recvMessage(conn)
            for game in self.games:
                if game_code == game.getCode() and not game.isGameOn():
                    game.setPlayer2Connection(conn)
                    game.turnOnGame()
                    game_thread = Thread(target=self.handleGame, args=(game,))
                    game_thread.start()
                    self.games.remove(game)
                    valid = True

            if not valid:
                self.sendMessage(conn, "!codeNotValid")

    def gameStartSettings(self, game):
        game.turn = 2
        try:
            self.sendMessage(game.getPlayer1Connection(), "!sg")
        except:
            self.sendMessage(game.getPlayer2Connection(), "!dc")

        if not self.checkConnection(game.getPlayer1Connection()):
            self.sendMessage(game.getPlayer2Connection(), "!dc")

        elif self.checkInGame(game.getPlayer1Connection()):
            self.sendMessage(game.getPlayer2Connection(), "!codeValid")

        else:
            game.turnOffGame()
            self.sendMessage(game.getPlayer2Connection(), "!dc")
            self.sendMessage(game.getPlayer1Connection(), "!dc")

        if not self.checkConnection(game.getPlayer2Connection()):
            self.sendMessage(game.getPlayer1Connection(), "!dc")

        if game.isGameOn():
            self.sendSigns(game)
            self.sendTurn(game)

    def handleGame(self, game):
        self.gameStartSettings(game)
        try:
            while game.isGameOn():
                winner = game.checkForWin()
                if winner != None:
                    self.gameEnd(game, winner)
                elif game.turn == 1:
                    move = self.requestMove(game, game.getPlayer1Connection())
                    game.setMove(move, game.getPlayer1Ch())
                    self.sendMove(game.getPlayer1Connection(), game.getPlayer1Ch(), move)
                    self.sendMove(game.getPlayer2Connection(), game.getPlayer1Ch(), move)
                    self.sendTurn(game)
                    self.showBoard(game)

                elif game.turn == 2:
                    move = self.requestMove(game, game.getPlayer2Connection())
                    game.setMove(move, game.getPlayer2Ch())
                    self.sendMove(game.getPlayer1Connection(), game.getPlayer2Ch(), move)
                    self.sendMove(game.getPlayer2Connection(), game.getPlayer2Ch(), move)
                    self.sendTurn(game)
                    self.showBoard(game)

            game.closeConnections()
        except:
            if game.turn == 1:
                self.sendMessage(game.getPlayer2Connection(), "!ed")
            if game.turn == 2:
                self.sendMessage(game.getPlayer1Connection(), "!ed")

            print("user disconnected")

    def start(self):
        self.server.listen()
        print("[SERVER] Server started...")

        while True:
            try:
                conn, addr = self.server.accept()
                game_code = self.recvMessage(conn)
                game_code_not_found = True
                if game_code == "!gameCodeStart":
                    game_code_not_found = False
                    game_code = random.randint(100000, 999999)
                    for game in self.games:
                        while game_code == game.getCode():
                            game_code = random.randint(100000, 999999)
                    self.sendMessage(conn, str(game_code))
                    print(game_code)
                    game = GameSever(conn)
                    game.setCode(str(game_code))
                    self.games.append(game)

                for game in self.games:
                    if game_code == game.getCode() and not game.isGameOn():
                        game_code_not_found = False
                        game.setPlayer2Connection(conn)
                        game.turnOnGame()
                        game_thread = Thread(target=self.handleGame, args=(game,))
                        game_thread.start()
                        self.games.remove(game)

                if game_code_not_found == True:
                    self.sendMessage(conn, "!codeNotValid")
                    recv_codeThread = Thread(target=self.recvCode, args=(conn,))
                    recv_codeThread.start()
            except ConnectionResetError:
                print("Client disconnected")


if __name__ == '__main__':
    server = Server()
