from titleScreen import TitleScreen
from onePlayerGameWindow import OpgWindow
from botLogic import EasyBot, MediumBot, HardBot

class OnePlayerScreen(TitleScreen):
    def __init__(self, widget, uiLocation, main):
        super().__init__(widget, uiLocation, main)

    def initButtonActions(self):

        self.backButton.clicked.connect(lambda: self.changeScreen(0))
        self.easyButton.clicked.connect(lambda: self.setDifficulty(EasyBot()))
        self.mediumButton.clicked.connect(lambda: self.setDifficulty(MediumBot()))
        self.hardButton.clicked.connect(lambda: self.setDifficulty(HardBot()))

    def setDifficulty(self, diff):
        self.main.game = OpgWindow(diff, self.widget.pos().x(), self.widget.pos().y())
        self.closeScreens()
