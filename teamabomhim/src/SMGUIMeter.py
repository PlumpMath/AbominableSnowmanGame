from panda3d.core import TransparencyAttrib, Vec2, TextNode
from direct.gui.OnscreenText import OnscreenText

class SMGUIMeter():
	
	def __init__(self, maxValue):
		meterImg = None
		self.value = 0.0
		self.maxValue = maxValue
		self.text = OnscreenText(text = "0", style = 1, fg = (0,0,0,1), pos = (-1.2, -0.95), align = TextNode.ALeft, scale = .2)

	def fillBy(self, amt):
		if(self.value + amt > self.maxValue):
			self.value = self.maxValue
		else:
			self.value += amt
		
	def emptyBy(self, amt):
		if(self.value - amt < 0):
			self.value = self.maxValue
		else:
			self.value = 0
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Returns the GUI element type.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def getGUIType(self):
		return 2
		
	def updateGUI(self):
		self.text.setText(str(self.value))