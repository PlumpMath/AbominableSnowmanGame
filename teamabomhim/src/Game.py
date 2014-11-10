import direct.directbase.DirectStart
from panda3d.core import TextNode, NodePath
from direct.showbase.DirectObject import DirectObject
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *

from SMWorld import SMWorld
from SMText import SMText
from SMAudioManager import SMAudioManager

class Game(DirectObject):

	gameState = -1

	def __init__(self):
		print("LINK START")
		self.textObj = SMText()
		self.textObj.addText("test", "abom20141109")
		
		self.audioMgr = SMAudioManager()

		self.title = OnscreenText(text = "The Abominable Snowman of the Himalayas",
									   pos = (0.0, 0.5), scale = 0.1,fg=(1,0.5,0.5,1),
									   align=TextNode.ACenter,mayChange=1)

		self.continueBtn = DirectButton(text = "New Game", scale = 0.1,
										command = self.newGame)

		self.newBtn = DirectButton(text = "Continue Game", scale= 0.1,
								   command = self.continueGame)
		self.newBtn.setPos(0.0, 0.0, -0.2)

		self.quitBtn = DirectButton(text = "Quit", scale = 0.1,
									command = self.quitGame)
		self.quitBtn.setPos(0.0, 0.0, -0.4)

		self.accept('escape', base.userExit)

        def newGame(self):
                self.hideMenu()
                # Loading screens will be added here in place of direct map invocation.
                self.world = SMWorld(self.gameState, "map01", -30, self.textObj, self.audioMgr)

        def continueGame(self):
                # When saving game state is implemented it will be added here.
                print("Continue Game")

        def quitGame(self):
                base.userExit()

        def hideMenu(self):
                self.title.hide()
                self.newBtn.hide()
                self.continueBtn.hide()
                self.quitBtn.hide()

        def showMenu(self):
                self.title.show()
                self.newBtn.show()
                self.continueBtn.show()
                self.quitBtn.show()

# PStatClient.connect()
base.setFrameRateMeter(True)
g = Game()
run()
