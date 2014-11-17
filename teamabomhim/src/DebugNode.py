from panda3d.bullet import BulletDebugNode

class DebugNode():
	
	def __init__(self):
		debugNode = BulletDebugNode('DebugNode')
		debugNode.showWireframe(True)
		debugNode.showConstraints(True)
		debugNode.showBoundingBoxes(True)
		debugNode.showNormals(True)
		self.debugNP = render.attachNewNode(debugNode)
		
	def getDebugNode(self):
		return self.debugNP