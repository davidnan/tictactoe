from gameWindow import GameWindow
import pygame
import sys
from titleScreen import TitleScreen
from onlineScreen import OnlineScreen, CreateGameScreen, JoinGameScreen
from onePlayerScreen import OnePlayerScreen
from PyQt5 import QtCore, QtGui, QtWidgets

class Main():
    def __init__(self):
        self.game = None
        self.online = False
        self.app = QtWidgets.QApplication(sys.argv)
        self.widget = QtWidgets.QStackedWidget()
        self.widget.setFixedWidth(420)
        self.widget.setFixedHeight(570)
        self.titleScreen = TitleScreen(self.widget, "resources/titleScreen.ui", self)
        self.opScreen = OnePlayerScreen(self.widget, "resources/onePlayerScreen.ui", self)
        self.onlineScreen = OnlineScreen(self.widget, "resources/onlineScreen.ui", self)
        self.createGameScreen = CreateGameScreen(self.widget, "resources/createGameScreen.ui", self)
        self.joinGameScreen = JoinGameScreen(self.widget, "resources/joinGameScreen.ui", self)
        self.widget.addWidget(self.titleScreen)
        self.widget.addWidget(self.opScreen)
        self.widget.addWidget(self.onlineScreen)
        self.widget.addWidget(self.createGameScreen)
        self.widget.addWidget(self.joinGameScreen)
        self.widget.show()


if __name__ == "__main__":
    main = Main()
    main.app.exec_()
    del main.app
    try:
        print(main.online)
        if not main.online:
            main.game.run()
    except:
        pass
