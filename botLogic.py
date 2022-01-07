from player import Player
import random
from math import inf as infinity

class EasyBot(Player):
    def __init__(self):
        super().__init__()

    @staticmethod
    def emptySpace(coords: tuple, board) -> bool:
        if board[coords[0]][coords[1]] is None:
            return True
        return False

    def getMove(self, board):
        coords = random.randint(0, 2), random.randint(0, 2)
        while not self.emptySpace(coords, board):
            coords = random.randint(0, 2), random.randint(0, 2)
        return coords


class MediumBot(EasyBot):
    def __init__(self):
        super().__init__()

    def checkSelfWin(self, board):
        # Diagonals
        if board[0][0] == board[1][1] == self.getCh() and self.emptySpace((2, 2), board):
            return (2, 2)
        if board[2][0] == board[1][1] == self.getCh() and self.emptySpace((0, 2), board):
            print(self.getCh())
            return 0, 2
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
        if board[1][0] == board[1][2] == self.getCh() and self.emptySpace((1, 1), board):
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
            return (1, 0)
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
        if board[1][0] == board[1][2] != None and self.emptySpace((1, 1), board):
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
            return (1, 0)
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

class HardBot(EasyBot):
    def __init__(self):
        super().__init__()

    def checkForWin(self, board):
        if board[0][0] == board[1][1] == board[2][2] != None:
            return board[0][0]

        elif board[0][2] == board[1][1] == board[2][0] != None:
            return board[0][2]

        for i in range(0, 3):
            if board[i][0] == board[i][1] == board[i][2] != None:
                return board[i][0]

            elif board[0][i] == board[1][i] == board[2][i] != None:
                return board[0][i]

        return None

    def emptyCells(self, board):
        cells = []
        for x, row in enumerate(board):
            for y, cell in enumerate(row):
                if cell is None:
                    cells.append([x, y])

        return cells

    def evaluate(self, board):
        winner = self.checkForWin(board)
        if winner == "X": score = -1
        elif winner == "0": score = 1
        else: score = 0
        return score

    def gameOver(self, board):
        winner = self.checkForWin(board)
        if winner is not None and winner != "T":
            return True
        return False

    def validMove(self, board, x, y):
        return True if self.emptySpace((x, y), board) else False

    def minimax(self, board, depth, player):
        if player == "0":
            best = [-1, -1, -infinity]
        else:
            best = [-1, -1, +infinity]

        if depth == 0 or self.gameOver(board):
            score = self.evaluate(board)
            return [-1, -1, score]

        for cell in self.emptyCells(board):
            x, y = cell
            board[x][y] = player
            if player == '0':
                player_m = 'X'
            else:
                player_m = '0'
            score = self.minimax(board, depth - 1, player_m)
            board[x][y] = None
            score[0], score[1] = x, y
            if player == "0":
                if score[2] > best[2]:
                    best = score
            else:
                if score[2] < best[2]:
                    best = score

        return best

    def getMove(self, board):
        depth = len(self.emptyCells(board))
        move = self.minimax(board, depth, "0")
        coords = move[0], move[1]
        return coords