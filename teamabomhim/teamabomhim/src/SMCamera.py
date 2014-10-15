
class SMCamera():
	
	def __init__(self, sx, sy, sz, parent):
		self.parent = parent
		base.cam.setPos(sx, sy, sz)
		base.cam.reparentTo(self.parent)
		
		self.cameraPitch = 10
		cameraTargetHeight = 6.0
		self.cameraDistance = 50
		print("Camera initialized.")
		
	def lookAt(self, node):
		base.cam.lookAt(node)
	
	def getPitch(self):
		return self.cameraPitch
	
	def setPitch(self, p):
		self.cameraPitch = p
		
	def reparentTo(self, nodePath):
		base.cam.reparentTo(nodePath)
	
	def setPos(self, x, y, z):
		base.cam.setPos(x, y, z)