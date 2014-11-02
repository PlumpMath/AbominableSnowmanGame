#Bullet Physics Engine
from panda3d.core import BitMask32, Vec3, Vec4, PNMImage, Filename, GeoMipTerrain, TextureStage, VBase4
from panda3d.bullet import BulletWorld, BulletRigidBodyNode, BulletDebugNode, BulletCharacterControllerNode, BulletGhostNode
from panda3d.bullet import BulletBoxShape, BulletCapsuleShape, BulletCylinderShape, BulletPlaneShape, BulletHeightfieldShape, ZUp
# from direct.showbase.DirectObject import DirectObject

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
		self.bulletWorld = world
		self.worldNP = worldNP
		self.target = target
		self.panicDistance = BulletGhostNode('Distance')
		shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
		self.panicDistance.addShape(shape)
		# self.panicDistance.setPos(x-10, y-1, z+1)
		
		self.AIModel = loader.loadModel(model)
		self.AIModel.setScale(0.5)
		self.AIModel.setPos(x-10, y-1, z+1)
		self.AIModel.reparentTo(render)
		
		self.bulletWorld.attachGhost(self.panicDistance)
		AIChar = self.worldNP.attachNewNode(self.physics(model))
		self.AIModel.reparentTo(AIChar)
		# AIChar.attachGhost(self.panicDistance)
		
	def physics(self, AIModel):
		AIShape = BulletCapsuleShape(0.1, 0.1, ZUp)
		AINode = BulletRigidBodyNode("AIChar")
		AINode.setMass(200)
		AINode.addShape(AIShape)
		self.bulletWorld.attachRigidBody(AINode)
		AINode.setDeactivationEnabled(False)
		AINode.setAngularFactor(Vec3(0,0,0))
		return AINode

	# def setup(self, model, name):
		self.AIworld = AIWorld(render)
		self.AIChar = AICharacter(name, model, 100, 0.05, 5)
		self.AIworld.addAiChar(self.AIChar)
		self.AIbehaviors = self.AIChar.getAiBehaviors()
		self.AIbehaviors.flee(self.target, 5.0, 10.0, 1)
		
	def AIUpdate(self):
		nodes = self.panicDistance.getOverlappingNodes()
		print(nodes)
		

