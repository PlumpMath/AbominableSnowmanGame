from panda3d.core import TransparencyAttrib, Vec2, TextNode
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage

POS_RIGHT = 1.2
POS_TOP = 1.1
COUNT_OFFSET_X = 0.5
COUNT_OFFSET_Y = -0.035

MIN_PEEK_HEIGHT = 0.85  # Bottom of peek
MAX_PEEK_HEIGHT = 1.20  # Top of peek
PEEK_TIME = 2.5
PEEK_RATE = 1

ST_IDLE = 0
ST_PEEK_IN = 1
ST_PEEK_OUT = 2
ST_PEEK_WAIT = 3

class SMGUICounter():

	def __init__(self, icon, maxValue):
		self.value = 0
		self.life = 0.0
		self.basePos = Vec2(0.7, POS_TOP)
		self.maxValue = maxValue   # Must be 1 or higher to activate.
		self.iconImg = OnscreenImage(image = ("../res/icons/gui_" + str(icon) + ".png"), pos = (self.basePos.getX(), 0, self.basePos.getY()), scale = 0.1)
		self.iconImg.setTransparency(TransparencyAttrib.MAlpha)
		strValue = str(self.value)
		if(self.maxValue > 0):
			strValue += ("/" + str(self.maxValue))
		self.textObj = OnscreenText(text = strValue, style = 1, fg = (0,0,0,1), pos = (self.basePos.getX() + COUNT_OFFSET_X, self.basePos.getY() + COUNT_OFFSET_Y), align = TextNode.ARight, scale = .2)
		self.state = ST_IDLE
		
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Returns the GUI element type.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
		
	def getGUIType(self):
		return 1
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Summons a 100-foot tall unicorn with chainsaws strapped to its back.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def updateGUI(self):
		dt = globalClock.getDt()
		state = self.state
		
		# State-based control
		if(state == ST_PEEK_IN):
			y = self.getYPos()
			if(y <= MIN_PEEK_HEIGHT):
				self.setState(ST_PEEK_WAIT)
			else:
				self.setYPos(y - PEEK_RATE * dt)
		elif(state == ST_PEEK_OUT):
			y = self.getYPos()
			if(y >= MAX_PEEK_HEIGHT):
				self.setState(ST_IDLE)
				self.life = 0.0
			else:
				self.setYPos(y + PEEK_RATE * dt)
		elif(state == ST_PEEK_WAIT):
			if(self.getLife() > PEEK_TIME):
				self.setState(ST_PEEK_OUT)
			else:
				self.addLife()
		self.updateText()
		self.updatePos()
	
	def updatePos(self):
		x = self.basePos.getX()
		y = self.basePos.getY() 
		self.iconImg.setX(x)
		self.iconImg.setZ(y)
		self.textObj.setX(x + COUNT_OFFSET_X)
		self.textObj.setY(y + COUNT_OFFSET_Y)
		
	def updateText(self):
		txt = str(self.value)
		if(self.maxValue > 0):
			txt += ("/" + str(self.maxValue))
		self.textObj.setText(txt)
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Returns the peek state as an integer.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def getState(self):
		return self.state
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Sets the peek state.
	# setState(int a {0 - 3})
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def setState(self, state):
		self.state = state;
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Adds 1 to the peek life counter.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def addLife(self):
		self.life += globalClock.getDt()
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Resets the peek life counter to 0.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def resetLife(self):
		self.life = 0.0
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Makes this class get a freaking life and stop sitting on its lazy a- Wait, what? Oh, returns the current peek life.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def getLife(self):
		return self.life
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Gets the value of the tracked variable.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def getValue(self):
		return self.value
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Changes the variable behind the scenes with no peeking.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def setValue(self, value):
		self.value = value
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Adds a value to the tracked variable and peeks the counter out. Use negatives to subtract.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def increment(self):
		self.setState(ST_PEEK_IN)
		self.value += 1
		
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Returns the OnScreenText object.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def getTextObj(self):
		return self.textObj
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Gets the vertical position of the text.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def getYPos(self):
		return self.basePos.getY()
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Sets the Y position of both the label and value.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def setYPos(self, ypos):
		self.basePos = Vec2(self.basePos.getX(), ypos)
