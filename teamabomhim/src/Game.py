import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from SMWorld import SMWorld
from SMText import SMText

class Game(DirectObject):
	
	gameState = -1
	
	def __init__(self):
		print("LINK START")
		self.textObj = SMText()
		self.textObj.addText("test", "abom20141025")
		
		self.world = SMWorld(self.gameState, "map01", -30, self.textObj)
		
g = Game()
run()