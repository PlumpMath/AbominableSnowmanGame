from panda3d.core import BitMask32, Vec3, Vec4, PNMImage, Filename, GeoMipTerrain, TextureStage, VBase4, Point3
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletRigidBodyNode, BulletDebugNode, BulletCharacterControllerNode, BulletGhostNode
from panda3d.bullet import BulletBoxShape, BulletCapsuleShape, BulletCylinderShape, BulletPlaneShape, BulletHeightfieldShape
from panda3d.bullet import ZUp
from direct.showbase.DirectObject import DirectObject
from direct.showbase.Transitions import Transitions

from math import sin, cos, pi

class SMColide():

	def __init__(self, model, world, worldNP, x, y, z, sizeX, sizeY, sizeZ, scale):
		self.AIX = x
		self.AIY = y
		self.AIZ = z
		self.worldNP = worldNP
		bulletWorld = world
		self.AIModel = loader.loadModel(model)
		self.AIModel.setScale(scale)
		self.AIModel.reparentTo(render)
		
		AIShape = BulletBoxShape(Vec3(sizeX, sizeY, sizeZ))
		self.AINode = BulletRigidBodyNode('AIChar')
		self.AINode.setMass(0)
		self.AINode.addShape(AIShape)
		
		self.AINode.setDeactivationEnabled(False)
		self.AINode.setAngularFactor(Vec3(0,0,0))
		render.attachNewNode(self.AINode)
		
		self.AIChar = self.worldNP.attachNewNode(self.AINode)
		self.AIModel.reparentTo(self.AIChar)
		self.AIChar.setPos(x, y, z)
		bulletWorld.attachRigidBody(self.AIChar.node())