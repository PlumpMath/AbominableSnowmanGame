#Bullet Physics Engine
from panda3d.core import BitMask32, Vec3, Vec4, PNMImage, Filename, GeoMipTerrain, TextureStage, VBase4
from panda3d.bullet import BulletWorld, BulletRigidBodyNode, BulletDebugNode, BulletCharacterControllerNode, BulletGhostNode
from panda3d.bullet import BulletBoxShape, BulletCapsuleShape, BulletCylinderShape, BulletPlaneShape, BulletHeightfieldShape, ZUp
from direct.showbase.DirectObject import DirectObject

#Importing AI from panda3d
from panda3d.ai import *

#Importing other classes
from DebugNode import DebugNode
from SMPlayer import SMPlayer
from SMKeyHandler import SMKeyHandler
from SMCamera import SMCamera
from SMCollisionHandler import SMCollisionHandler
from SMLighting import SMLighting

class SMAI():

	# self.SMAI = SMAI(self.worldBullet, self.worldObj, self.playerNP.getX(), self.playerNP.getY(), self.playerNP.getZ(), "../res/models/goat.egg", "Flee", self.playerNP)	
	def __init__(self, world, worldNP, x, y, z, model, type, target):
		self.world = world
		self.worldNP = worldNP
		self.target = target
		
		AIModel = loader.loadModel(model)
		AIModel.setScale(1)
		AIModel.setPos(x-5, y-5, z+1)
		AIModel.reparentTo(render)
		self.setup(AIModel, model)
		self.AIUpdate()
	
	def setup(self, model, name):
		self.AIworld = AIWorld(render)
		self.AIChar = AICharacter(name, model, 100, 0.05, 5)
		self.AIworld.addAiChar(self.AIChar)
		self.AIbehaviors = self.AIChar.getAiBehaviors()

		self.AIbehaviors.seek(self.target)
		
	def AIUpdate(self):
		self.AIworld.update()
		self.AIbehaviors.seek(self.target)
		

