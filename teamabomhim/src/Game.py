import direct.directbase.DirectStart
from panda3d.core import TextNode, NodePath
from direct.showbase.DirectObject import DirectObject
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TransparencyAttrib
from direct.gui.DirectGui import *

from SMWorld import SMWorld
from SMText import SMText
from SMAudioManager import SMAudioManager

class Game(DirectObject):

	def __init__(self):
		print("LINK START")
		self.textObj = SMText()
		self.textObj.addText("test", "abom20141207")
		
		self.audioMgr = SMAudioManager()

		#Print out Logo
		self.title = OnscreenImage(image = "../res/icons/logo.png", pos = (0.0, -70.0, 0.45), scale = (1.1, 0.9, 0.5))
									   
		#Allow Transparencies of PNG
		self.title.setTransparency(TransparencyAttrib.MAlpha)
									   
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
				
                # Loading screen
				loadingText=OnscreenText("Loading...",1,fg=(1,1,1,1),pos=(0,0),align=TextNode.ACenter,scale=.07,mayChange=1)
				base.graphicsEngine.renderFrame() 
				base.graphicsEngine.renderFrame() 
				base.graphicsEngine.renderFrame() 
				base.graphicsEngine.renderFrame()
				
				self.world = SMWorld(1, self.textObj, self.audioMgr)
				
				loadingText.cleanup()

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

base.setFrameRateMeter(True)
g = Game()
run()

# I-It's not like I wanted you to look at the source code or anything! B... Baka!