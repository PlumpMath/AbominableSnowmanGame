class SMGUIMeter():
	
	def __init__(self, maxValue):
		meterImg = None
	
	
	
	
	def fillBy(self, amt):
		self.value += amt
		
	def emptyBy(self, amt):
		self.value -= amt
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Returns the GUI element type.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def getGUIType(self):
		return 2