from panda3d.core import TextNode
from direct.gui.OnscreenText import OnscreenText

TEXT_MARGIN = 0.05
TEXT_LEFT = -1.32
TEXT_RIGHT = 1.32
TEXT_TOP = 0.95
TEXT_BOTTOM = -0.95

# Add text like this from the SMWorld class:
# self.textObj.addText("textReferenceName", "The message you want to display")

class SMText():
	
	def __init__(self):
		
		self.textLine = 0
		self.text = {}
	
	def addText(self, name, message):
		textObj = OnscreenText(text = message, style = 1, fg = (0,0,0,1), pos = (TEXT_LEFT, TEXT_TOP - (TEXT_MARGIN * self.textLine)), align = TextNode.ALeft, scale = .05)
		self.textLine += 1
		self.text[name] = textObj
		
	def editText(self, name, message):
		textObj = self.text[name]
		textObj.setText(message)
	
	def removeText(self, name):
		textObj = self.text[name]
		del self.text[name]
		textObj.destroy()
		self.textLine -= 1
	
	def addNormalText(self, id, message, time):
		print("TODO: Add this in later if needed.")