
from panda3d.core import BitMask32, Vec3, Vec4, PNMImage, Filename, GeoMipTerrain, TextureStage, VBase4
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletRigidBodyNode, BulletDebugNode, BulletCharacterControllerNode, BulletGhostNode
from panda3d.bullet import BulletBoxShape, BulletCapsuleShape, BulletCylinderShape, BulletPlaneShape, BulletHeightfieldShape
from panda3d.bullet import ZUp
from direct.showbase.DirectObject import DirectObject
from direct.showbase.Transitions import Transitions

from DebugNode import DebugNode
from SMPlayer import SMPlayer
from SMKeyHandler import SMKeyHandler
from SMCamera import SMCamera
from SMCollisionHandler import SMCollisionHandler
from SMLighting import SMLighting
from SMCollect import SMCollect
from SMBall import SMBall
from SMGUI import SMGUI
from SMGUIElement import SMGUIElement


class SMAI():

	def __init__(self, model, speed, world, worldNP, x, y, z):
		self.AISpeed = speed
		self.AIX = x
		self.AIY = y
		self.AIZ = z
		self.worldNP = worldNP
		bulletWorld = world
		self.type = ""
		# self.moveTo = False
		self.AIModel = loader.loadModel(model)
		self.AIModel.setScale(2)
		# self.AIModel.setPos(x-15, y-15, z-15)
		self.AIModel.reparentTo(render)
		
		AIShape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
		self.AINode = BulletRigidBodyNode('AIChar')
		self.AINode.setMass(200)
		self.AINode.addShape(AIShape)
		
		self.AINode.setDeactivationEnabled(False)
		self.AINode.setAngularFactor(Vec3(0,0,0))
		render.attachNewNode(self.AINode)
		
		self.AIChar = self.worldNP.attachNewNode(self.AINode)
		self.AIModel.reparentTo(self.AIChar)
		self.AIChar.setPos(x, y, z)
		bulletWorld.attachRigidBody(self.AIChar.node())
		# return self.AIChar

	def setBehavior(self, type, target):
		if(type == "flee"):
			self.type = type
			self.target = target
			print("Type set to flee")
		elif(type == "seek"):
			self.type = type
			self.target = target
			print("Type set to seek")
		else:
			print("Error @ Incorrect Type!")

	def moveTo(self, target):
		self.moveTo = True
		self.target = target
			
	def flee(self):
		# print("fleeing")
		self.X0 = self.target.getX()
		self.X1 = self.AIChar.getX()
		self.Y0 = self.target.getY()
		self.Y1 = self.AIChar.getY()
		if(self.AIChar.getDistance(self.target) < 32.0):
			# print("Flee!")
			# print(Vec3.forward())
			# self.AIChar.lookAt(self.target)
			self.AIChar.setH(self.target.getH())
			# self.AIChar.setAngularVelocity(self.AISpeed)
			# self.AINode.setLinearVelocity(Vec3.forward())
		
		
	def seek(self):
		print("seeking")
		self.X0 = self.target.getX()
		self.X1 = self.AIChar.getX()
		self.Y0 = self.target.getY()
		self.Y1 = self.AIChar.getY()
		
	def moveToRun(self):
		# if(self.target.getX()+5 <= self.AIChar.getX() and self.target.getX()-5 >= self.AIChar.getX() and self.target.getY()+5 <= self.AIChar.getY() and self.target.getY()-5 >= self.AIChar.getY()):
			print("It's stopped!")
			# self.AIChar.clearForces()
			# self.AIChar.setLinearVelocity(0)
		# else:
			# self.AINode.clearForces()
			# self.AIChar.lookAt(self.target)
			# self.AINode.setLinearVelocity(self.AISpeed)
		
	def AIUpdate(self):
		if(self.moveTo == True):
			self.moveToRun()
			
		if(self.type == "seek"):
			self.seek()
		elif(self.type == "flee"):
			self.flee()
		else:
			print("Error @ No AI Type")
	