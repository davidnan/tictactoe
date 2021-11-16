import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal, QObject

from titleScreen import TitleScreen
from gameClient import OnlineGame
from threading import Thread
import pyperclip

class Communicate(QObject):
    closeApp = pyqtSignal()

class OnlineScreen(TitleScreen):
    def __init__(self, widget, uiLocation, main):
        super().__init__(widget, uiLocation, main)

    def initButtonActions(self):
        self.backButton.clicked.connect(self.backClick)
        self.createGameButton.clicked.connect(lambda: self.connectToServer())
        self.joinGameButton.clicked.connect(lambda: self.changeScreen(4))

    def backClick(self):
        self.changeScreen(0)
        self.main.online = False

    def connectToServer(self):
        self.changeScreen(3)
        if self.main.createGameScreen.game_code == "000000":
            try:
                self.hasCode = True
                self.main.createGameScreen.connect()
                self.thread = Thread(target=self.main.createGameScreen.gameStart)
                self.thread.start()

            except ConnectionRefusedError:
                print("Server is down")

class CreateGameScreen(TitleScreen):
    def __init__(self, widget, uiLocation, main):
        super().__init__(widget, uiLocation, main)
        self.game_code = None
        self.main.game = None
        self.main.online = True
        self.game_code = "000000"

    def initButtonActions(self):
        self.backButton.clicked.connect(lambda: self.changeScreen(2))
        self.copyCodeButton.clicked.connect(self.copyCode)

    def connect(self):
        self.game_code = self.main.game.client.connect(self.game_code)
        self.copyCodeButton.setText(self.game_code)

    def gameStart(self):
        if self.main.game.client.gameStart() and self.main.online:
            self.c = Communicate()
            self.c.closeApp.connect(self.closeScreens)
            self.c.closeApp.emit()
            self.main.game.run(self.widget.pos().x(), self.widget.pos().y())

    def copyCode(self):
        pyperclip.copy(self.game_code)

class JoinGameScreen(TitleScreen):
    def __init__(self, widget, uiLocation, main):
        super().__init__(widget, uiLocation, main)
        self.game_code = None
        self.main.game = None

    def initButtonActions(self):
        self.backButton.clicked.connect(lambda: self.changeScreen(2))
        self.connectButton.clicked.connect(lambda: self.connect())

    def connect(self):
        code = self.gameCodeText.text()
        self.gameCodeText.setText("")
        valid = self.main.game.client.connect(code)
        if valid == "!codeValid":
            self.game_code = code
            self.main.game.client.game_code = code
        if self.game_code != None:
            self.closeScreens()
            self.main.game.run(self.widget.pos().x(), self.widget.pos().y())
