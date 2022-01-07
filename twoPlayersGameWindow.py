import pygame
from gameWindow import GameWindow
import sys

class TpgWindow(GameWindow):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.initSurface()
        self.initScoreBoard()

    def run(self):
        while True:
            winner = self.game.checkForWin()
            if winner != None:
                self.game.increaseWinnerScore(winner)
                self.gameOver(winner)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    coords = list(mouse)
                    player = None
                    if self.game.turn == -1:
                        self.game.turn = 1
                        player = "0"
                    elif self.game.turn == 1:
                        self.game.turn = -1
                        player = "X"

                    self.mouseClick(coords, player)

            pygame.display.update()