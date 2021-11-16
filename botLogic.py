from player import Player
import random

class EasyBot(Player):
    def __init__(self):
        super().__init__()

    def emptySpace(self, coords, board):
        if board[coords[0]][coords[1]] == None:
            return True
        return False

    def getMove(self, board):
        coords = random.randint(0, 2), random.randint(0, 2)
        while not self.emptySpace(coords, board):
            coords = random.randint(0, 2), random.randint(0, 2)
        return coords


class MediumBot(Player):
    def __init__(self):
        super().__init__()

    def emptySpace(self, coords, board):
        if board[coords[0]][coords[1]] == None:
            return True
        return False
    def checkSelfWin(self, board):
        # Diagonals
        if board[0][0] == board[1][1] == self.getCh() and self.emptySpace((2, 2), board):
            return (2, 2)
        if board[2][0] == board[1][1] == self.getCh() and self.emptySpace((0, 2), board):
            return (0, 2)
        if board[2][2] == board[1][1] == self.getCh() and self.emptySpace((0, 0), board):
            return (0, 0)
        if board[0][2] == board[1][1] == self.getCh() and self.emptySpace((2, 0), board):
            return (2, 0)
        if board[0][2] == board[2][0] == self.getCh() and self.emptySpace((1, 1), board):
            return (1, 1)
        if board[2][2] == board[0][0] == self.getCh() and self.emptySpace((1, 1), board):
            return (1, 1)

        # Middle lines
        if board[0][1] == board[1][1] == self.getCh() and self.emptySpace((2, 1), board):
            return (2, 1)
        if board[0][1] == board[2][1] == self.getCh() and self.emptySpace((1, 1), board):
            return (1, 1)
        if board[1][0] == board[1][1] == self.getCh() and self.emptySpace((1, 2), board):
            return (1, 2)
        if board[1][0] == board[1][2] == self.getCh() and self.emptySpace((1, 2), board):
            return (1, 1)
        if board[2][1] == board[1][1] == self.getCh() and self.emptySpace((0, 1), board):
            return (0, 1)
        if board[2][1] == board[0][1] == self.getCh() and self.emptySpace((1, 1), board):
            return (1, 1)
        if board[1][2] == board[1][1] == self.getCh() and self.emptySpace((1, 0), board):
            return (1, 0)
        if board[1][2] == board[1][0] == self.getCh() and self.emptySpace((1, 1), board):
            return (1, 1)

        # Top Line
        if board[0][0] == board[0][1] == self.getCh() and self.emptySpace((0, 2), board):
            return (0, 2)
        if board[0][0] == board[0][2] == self.getCh() and self.emptySpace((0, 1), board):
            return (0, 1)
        if board[0][2] == board[0][1] == self.getCh() and self.emptySpace((0, 0), board):
            return (0, 0)

        # Right Line
        if board[0][2] == board[1][2] == self.getCh() and self.emptySpace((2, 2), board):
            return (2, 2)
        if board[0][2] == board[2][2] == self.getCh() and self.emptySpace((1, 2), board):
            return (1, 2)
        if board[1][2] == board[2][2] == self.getCh() and self.emptySpace((0, 2), board):
            return (0, 2)

        # Left Line
        if board[0][0] == board[1][0] == self.getCh() and self.emptySpace((2, 0), board):
            return (2, 0)
        if board[0][0] == board[2][0] == self.getCh() and self.emptySpace((1, 0), board):
            return (0, 1)
        if board[1][0] == board[2][0] == self.getCh() and self.emptySpace((0, 0), board):
            return (0, 0)

        # Bottom Line
        if board[2][0] == board[2][1] == self.getCh() and self.emptySpace((2, 2), board):
            return (2, 2)
        if board[2][0] == board[2][2] == self.getCh() and self.emptySpace((2, 1), board):
            return (2, 1)
        if board[2][1] == board[2][2] == self.getCh() and self.emptySpace((2, 0), board):
            return (2, 0)
        return None

    def getMove(self, board):
        coords = self.checkSelfWin(board)
        if coords != None:
            return coords
            # Diagonals
        if board[0][0] == board[1][1] != None and self.emptySpace((2, 2), board):
            return (2, 2)
        if board[2][0] == board[1][1] != None and self.emptySpace((0, 2), board):
            return (0, 2)
        if board[2][2] == board[1][1] != None and self.emptySpace((0, 0), board):
            return (0, 0)
        if board[0][2] == board[1][1] != None and self.emptySpace((2, 0), board):
            return (2, 0)
        if board[0][2] == board[2][0] != None and self.emptySpace((1, 1), board):
            return (1, 1)
        if board[2][2] == board[0][0] != None and self.emptySpace((1, 1), board):
            return (1, 1)

        # Middle lines
        if board[0][1] == board[1][1] != None and self.emptySpace((2, 1), board):
            return (2, 1)
        if board[0][1] == board[2][1] != None and self.emptySpace((1, 1), board):
            return (1, 1)
        if board[1][0] == board[1][1] != None and self.emptySpace((1, 2), board):
            return (1, 2)
        if board[1][0] == board[1][2] != None and self.emptySpace((1, 2), board):
            return (1, 1)
        if board[2][1] == board[1][1] != None and self.emptySpace((0, 1), board):
            return (0, 1)
        if board[2][1] == board[0][1] != None and self.emptySpace((1, 1), board):
            return (1, 1)
        if board[1][2] == board[1][1] != None and self.emptySpace((1, 0), board):
            return (1, 0)
        if board[1][2] == board[1][0] != None and self.emptySpace((1, 1), board):
            return (1, 1)

        # Top Line
        if board[0][0] == board[0][1] != None and self.emptySpace((0, 2), board):
            return (0, 2)
        if board[0][0] == board[0][2] != None and self.emptySpace((0, 1), board):
            return (0, 1)
        if board[0][2] == board[0][1] != None and self.emptySpace((0, 0), board):
            return (0, 0)

        # Right Line
        if board[0][2] == board[1][2] != None and self.emptySpace((2, 2), board):
            return (2, 2)
        if board[0][2] == board[2][2] != None and self.emptySpace((1, 2), board):
            return (1, 2)
        if board[1][2] == board[2][2] != None and self.emptySpace((0, 2), board):
            return (0, 2)

        # Left Line
        if board[0][0] == board[1][0] != None and self.emptySpace((2, 0), board):
            return (2, 0)
        if board[0][0] == board[2][0] != None and self.emptySpace((1, 0), board):
            return (0, 1)
        if board[1][0] == board[2][0] != None and self.emptySpace((0, 0), board):
            return (0, 0)

        # Bottom Line
        if board[2][0] == board[2][1] != None and self.emptySpace((2, 2), board):
            return (2, 2)
        if board[2][0] == board[2][2] != None and self.emptySpace((2, 1), board):
            return (2, 1)
        if board[2][1] == board[2][2] != None and self.emptySpace((2, 0), board):
            return (2, 0)


        coords = random.randint(0, 2), random.randint(0, 2)
        while not self.emptySpace(coords, board):
            coords = random.randint(0, 2), random.randint(0, 2)
        return coords

class HardBot(Player):
    def __init__(self):
        super().__init__()