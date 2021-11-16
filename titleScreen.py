import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import QThread
from gameClient import OnlineGame
from twoPlayersGameWindow import TpgWindow

class TitleScreen(QMainWindow):
    def __init__(self, widget, uiLocation, main):
        super().__init__()
        loadUi(uiLocation, self)
        self.widget = widget
        self.main = main
        self.main.online = False
        self.show()
        self.initButtonActions()

    def initButtonActions(self):
        self.onePlayerButton.clicked.connect(lambda: self.changeScreen(1))
        self.onlineButton.clicked.connect(self.onlineClick)
        self.twoPlayersButton.clicked.connect(self.__twoPlayersGame)

    def onlineClick(self):
        self.changeScreen(2)
        self.main.game = OnlineGame()
        self.main.online = True

    def changeScreen(self, screen):
        self.widget.setCurrentIndex(screen)

    def __twoPlayersGame(self):
        self.closeScreens()
        self.main.game = TpgWindow(self.widget.pos().x(), self.widget.pos().y())

    def closeScreens(self):
        self.main.app.closeAllWindows()