from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, QObject

from titleScreen import TitleScreen
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
        self.joinGameButton.clicked.connect(self.joinGameButtonFunc)

    def backClick(self):
        self.changeScreen(0)
        self.main.online = False

    def joinGameButtonFunc(self):
        self.changeScreen(4)
        self.main.joinGameScreen.gameCodeText.setPlaceholderText("Game Code")

    def connectToServer(self):
        self.changeScreen(3)
        if self.main.createGameScreen.game_code == "!gameCodeStart":
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
        self.game_code = "!gameCodeStart"

        self.copyCodeButton.installEventFilter(self)
        self.copyLabel.setText("")

    def initButtonActions(self):
        self.backButton.clicked.connect(self.backButtonFunc)
        self.copyCodeButton.clicked.connect(self.copyCode)

    def eventFilter(self, obj, event):
        if obj == self.copyCodeButton and event.type() == QtCore.QEvent.HoverEnter:
            self.onHovered()
        if obj == self.copyCodeButton and event.type() == QtCore.QEvent.HoverLeave:
            self.offHover()
        return super().eventFilter(obj, event)

    def onHovered(self):
        self.copyLabel.setText("copy")

    def offHover(self):
        self.copyLabel.setText("")

    def connect(self):
        self.game_code = self.main.game.client.connect(self.game_code)
        self.copyCodeButton.setText(self.game_code)

    def gameStart(self):
        try:
            start = self.main.game.client.gameStart()
            if start and self.main.online:
                self.c = Communicate()
                self.c.closeApp.connect(self.closeScreens)
                self.c.closeApp.emit()
                self.main.game.run(self.widget.pos().x(), self.widget.pos().y())
        except:
            pass

    def backButtonFunc(self):
        self.game_code = "!gameCodeStart"
        self.changeScreen(2)
        self.main.game.client.resetSocket()

    def copyCode(self):
        pyperclip.copy(self.game_code)

class JoinGameScreen(TitleScreen):
    def __init__(self, widget, uiLocation, main):
        super().__init__(widget, uiLocation, main)
        self.game_code = None
        self.main.game = None

    def initButtonActions(self):
        self.backButton.clicked.connect(self.backButtonFunc)
        self.connectButton.clicked.connect(lambda: self.connect())

    def backButtonFunc(self):
        self.changeScreen(2)
        self.main.game.client.resetSocket()

    def connect(self):
        code = self.gameCodeText.text()
        self.gameCodeText.setText("")
        valid = self.main.game.client.connect(code)
        if valid == "!codeNotValid":
            self.gameCodeText.setPlaceholderText("Invalid Code")
        if valid == "!codeValid":
            self.game_code = code
            self.main.game.client.game_code = code
        if self.game_code != None:
            self.closeScreens()
            self.main.game.run(self.widget.pos().x(), self.widget.pos().y())
