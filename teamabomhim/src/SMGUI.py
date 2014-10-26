
MIN_PEEK_HEIGHT = 0.85  # Bottom of peek
MAX_PEEK_HEIGHT = 1.20  # Top of peek
PEEK_RATE = 1

ST_IDLE = 0
ST_PEEK_IN = 1
ST_PEEK_OUT = 2
ST_PEEK_WAIT = 3

class SMGUI():
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Constructor
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def __init__(self):
		self.elements = {}
		taskMgr.add(self.updateGUI, "guiUpdateTask")
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Adds a GUI element to the handler.
	# addElement(String name, SMGUIElement element)
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def addElement(self, name, element):
		self.elements[name] = element
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Updates the GUI
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def updateGUI(self, task):
		
		# Update the GUI
		for m in self.elements.values():
			
			dt = globalClock.getDt()
			state = m.getState()
			
			# State-based control
			if(state == ST_PEEK_IN):
				y = m.getYPos()
				if(y <= MIN_PEEK_HEIGHT):
					m.setState(ST_PEEK_WAIT)
				else:
					m.setYPos(y - PEEK_RATE * dt)
			elif(state == ST_PEEK_OUT):
				y = m.getYPos()
				if(y >= MAX_PEEK_HEIGHT):
					m.setState(ST_IDLE)
				else:
					m.setYPos(y + PEEK_RATE * dt)
			elif(state == ST_PEEK_WAIT):
				if(m.getLife() > 120):
					m.setState(ST_PEEK_OUT)
				else:
					m.addLife()

	
		return task.cont