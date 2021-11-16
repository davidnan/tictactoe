import pygame, sys
from game import Game
import os

class GameWindow():
    def __init__(self, *args):
        self.x, self.y = args
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (self.x, self.y + 30)
        pygame.init()
        self.game = Game()
        self.WIDTH = 420
        self.HEIGHT = 570
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.xoFont = pygame.font.SysFont("comicsansms", 120)
        self.xShow = self.xoFont.render("X", True, (255, 32, 110))
        self.oShow = self.xoFont.render("0", True, (65, 234, 212))
        self.turnText = pygame.font.SysFont("comicsansms", 70)

    def changeWindowLocation(self, x, y):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y + 30)

    def initSurface(self):
        self.screen.fill((12, 15, 10))
        self.drawGrid()

    def initScoreBoard(self):
        if self.game.player1.getName() == None:
            player1Text = self.game.player1.getCh() + "'s score"
        else: player1Text = self.game.player1.getName()

        if self.game.player2.getName() == None:
            player2Text = self.game.player2.getCh() + "'s score"
        else: player2Text = self.game.player2.getName()

        if self.game.player1.getCh() == "X":
            player1Label = pygame.font.SysFont("comicsansms", 30).render(player1Text, True, (255, 32, 110))
            player2Label = pygame.font.SysFont("comicsansms", 30).render(player2Text, True, (65, 234, 212))
        else:
            player1Label = pygame.font.SysFont("comicsansms", 30).render(player1Text, True, (65, 234, 212))
            player2Label = pygame.font.SysFont("comicsansms", 30).render(player2Text, True, (255, 32, 110))

        text = self.turnText.render("X", True, (255, 32, 110))
        self.screen.blit(text, ((self.WIDTH - 50) / 2, 470))
        self.screen.blit(player1Label, (10, 440))
        self.screen.blit(player2Label, (280, 440))
        self.screen.blit(pygame.font.SysFont("comicsansms", 60).render(str(self.game.player1.getScore()), True, (255, 255, 255)), (53, 470))
        self.screen.blit(pygame.font.SysFont("comicsansms", 60).render(str(self.game.player2.getScore()), True, (255, 255, 255)), (338, 470))

    def drawTurnText(self, turn):
        text = None
        if turn == "X":
            text = self.turnText.render("X", True, (255, 32, 110))
        if turn == "0":
            text = self.turnText.render("0", True, (65, 234, 212))
        self.screen.blit(text, ((self.WIDTH - 50) / 2, 470))

    def deleteTurnText(self):
        rect = pygame.Rect((self.WIDTH - 50) / 2, 470, 70, 85)
        pygame.draw.rect(self.screen, (12, 15, 10), rect)

    def transparentScreen(self):
        shape_surf = pygame.Surface(pygame.Rect((0, 0, self.WIDTH, self.HEIGHT)).size, pygame.SRCALPHA)
        for i in range(0, 255):
            shape_surf.set_alpha(1)
            pygame.draw.rect(shape_surf, (12, 15, 10), shape_surf.get_rect())
            self.screen.blit(shape_surf, (0, 0, self.WIDTH, self.HEIGHT))
            pygame.display.update()


    def gameOverScreen(self, winner):
        self.transparentScreen()
        font_winner = pygame.font.SysFont("comicsansms", 120)

        if winner == "X":
            text = "X wins!"
            screen_text = font_winner.render(text, True, (255, 32, 110))
        elif winner == "0":
            text = "0 wins!"
            screen_text = font_winner.render(text, True, (65, 234, 212))
        else:
            text = "Tie!"
            screen_text = font_winner.render(text, True, (255, 255, 255))

        text_rect = screen_text.get_rect(center=(self.WIDTH / 2, 200))
        self.screen.blit(screen_text, text_rect)
        pygame.display.update()

    def drawGrid(self):
        blockSize = 140
        for x in range(0, self.WIDTH, blockSize):
            for y in range(0, self.HEIGHT - 150, blockSize):
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(self.screen, (153, 153, 153), rect, 1)

    def mouseClick(self, coords, player):
        if coords[1] < 420:
            coords[0] = (coords[0] // 140 * 140 + 70) // 140
            coords[1] = (coords[1] // 140 * 140 + 70) // 140
            self.placeMove(coords, player)

    def placeMove(self, coords, player):
        if self.game.emptySpace((coords[0], coords[1])):
            self.game.setMove((coords[0], coords[1]), player)
            self.showMove((coords[0] * 140 + 70, coords[1] * 140 + 70), player)
        else:
            self.game.turn = self.game.turn * -1

    def showMove(self, coords, player):
        if player == "0":
            text_rect = self.oShow.get_rect(center=coords)
            self.screen.blit(self.oShow, text_rect)
        if player == "X":
            text_rect = self.xShow.get_rect(center=coords)
            self.screen.blit(self.xShow, text_rect)
        self.deleteTurnText()
        turn = lambda x: "0" if x == "X" else "X"
        self.drawTurnText(turn(player))

    def wait(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return

    def gameOver(self, winner):
        self.gameOverScreen(winner)
        self.wait()
        self.game.initSettings()
        self.initSurface()
        self.initScoreBoard()
