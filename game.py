from player import Player

class Game():
    def __init__(self):
        self.player1 = Player()
        self.player1.setCh('X')
        self.player2 = Player()
        self.player2.setCh('0')
        self.initSettings()

    def initSettings(self):
        self.turn = 1
        self.__boardCount = 0
        self.boardFull = False
        self.resetBoard()

    def showBoard(self):
        for i in range(0, 3):
            print(self.board[i])

    def setMove(self, coords, player):
        self.board[coords[0]][coords[1]] = player
        self.__boardCount += 1
        if self.__boardCount == 8:
            self.boardFull = True

    def resetBoard(self):
        self.board = [[None, None, None],
                      [None, None, None],
                      [None, None, None]]

    def emptySpace(self, coords):
        if self.board[coords[0]][coords[1]] == None:
            return True
        return False

    def checkForWin(self):
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != None:
            return self.board[0][0]

        elif self.board[0][2] == self.board[1][1] == self.board[2][0] != None:
            return self.board[0][2]

        for i in range(0, 3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != None:
                return self.board[i][0]

            elif self.board[0][i] == self.board[1][i] == self.board[2][i] != None:
                return self.board[0][i]

        tie = True
        for i in range(0, 3):
            for j in range(0, 3):
                if self.board[i][j] == None:
                    tie = False

        if tie == True:
            return "T"
        return None

    def increaseWinnerScore(self, winner):
        if self.player1.getCh() == winner:
            self.player1.incrementScore()
        elif self.player2.getCh() == winner:
            self.player2.incrementScore()