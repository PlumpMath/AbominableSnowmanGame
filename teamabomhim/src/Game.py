import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from SMWorld import SMWorld

# import SMWorld

class Game(DirectObject):
	
	gameState = -1
	
	def __init__(self):
		print("LINK START")
		self.world = SMWorld(self.gameState, "map01", -20)
		
g = Game()
run()