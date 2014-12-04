from panda3d.core import BitMask32, Vec3, Vec4, PNMImage, Filename, GeoMipTerrain, TextureStage, VBase4
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletRigidBodyNode, BulletDebugNode, BulletCharacterControllerNode, BulletGhostNode
from panda3d.bullet import BulletBoxShape, BulletCapsuleShape, BulletCylinderShape, BulletPlaneShape, BulletHeightfieldShape
from panda3d.bullet import ZUp
from direct.showbase.DirectObject import DirectObject

from DebugNode import DebugNode
from SMPlayer import SMPlayer
from SMKeyHandler import SMKeyHandler
from SMCollisionHandler import SMCollisionHandler
from SMLighting import SMLighting

class SMCollect():
	def __init__(self, world, worldNP, sPos):
		self.world = world
		self.worldNP = worldNP
		self.collected = False
		self.collectShape = BulletBoxShape(Vec3(3, 3, 3))
		self.collectGN = BulletGhostNode('Box')
		self.collectGN.addShape(self.collectShape)
		self.collectNP = self.create(sPos, self.collectGN)
		print("Collectable Initialized")
	
	def exists(self):
		return not(self.collected)
	
	def getNode(self):
		return self.collectGN
	
	def create(self, pos, ghostNode):
		collectNode = render.attachNewNode(ghostNode)
		collectNode.setPos(pos)
		collectNode.setCollideMask(BitMask32(0x0f))
		self.world.attachGhost(ghostNode)
		visualCN = loader.loadModel("../res/models/snowflake.egg")
		visualCN.reparentTo(collectNode)
		visualCN.setScale(2)
		return collectNode
		
	def destroy(self):
		self.collected = True
		self.world.removeGhost(self.collectGN)
		self.collectNP.removeNode()
		
