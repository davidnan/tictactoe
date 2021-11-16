from gameWindow import GameWindow
import pygame, sys

class OpgWindow(GameWindow):
    def __init__(self, bot, x, y):
        super().__init__(x, y)
        self.initSurface()
        self.initScoreBoard()
        self.game.player2 = bot
        self.game.player2.setCh("0")

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
                    if self.game.turn == 1:
                        self.game.turn = -1
                        self.mouseClick(coords, self.game.player1.getCh())
                    winner = self.game.checkForWin()
                    if self.game.turn == -1 and winner == None:
                        self.game.turn = 1
                        if not self.game.boardFull:
                            coords = self.game.player2.getMove(self.game.board)
                        self.placeMove(coords, self.game.player2.getCh())


            pygame.display.update()