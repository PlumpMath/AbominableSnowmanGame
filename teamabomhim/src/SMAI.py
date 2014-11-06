
from panda3d.core import BitMask32, Vec3, Vec4, PNMImage, Filename, GeoMipTerrain, TextureStage, VBase4, Point3
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

from math import sin, cos, pi

#Globals for converting between radians
DEG_TO_RAD = pi/180
PNT = Point3(0,0,0)

class SMAI():
	#This constructs the nods tree needed for an AIChar object.
	#Takes in a model as a string, a speed double, a world object, a bullet physics world and n x, y and z positions
	def __init__(self, model, speed, world, worldNP, x, y, z):
		self.AISpeed = 80000
		self.maxSpeed = speed
		self.AIX = x
		self.AIY = y
		self.AIZ = z
		self.worldNP = worldNP
		bulletWorld = world
		self.type = ""
		self.AIModel = loader.loadModel(model)
		# self.AIModel.setScale(1)
		self.AIModel.reparentTo(render)
		
		AIShape = BulletBoxShape(Vec3(2, 2, 2))
		self.AINode = BulletRigidBodyNode('AIChar')
		self.AINode.setMass(100)
		self.AINode.addShape(AIShape)
		
		self.AINode.setDeactivationEnabled(False)
		self.AINode.setAngularFactor(Vec3(0,0,0))
		render.attachNewNode(self.AINode)
		
		self.AIChar = self.worldNP.attachNewNode(self.AINode)
		self.AIModel.reparentTo(self.AIChar)
		self.AIChar.setPos(x, y, z)
		bulletWorld.attachRigidBody(self.AIChar.node())

	#This method needs to be called on your AIChar object to determine what type of AI you want.
	#Takes in a type string; either flee or seek and also a target object.
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
		if(self.AIChar.getDistance(self.target) < 40.0):
			if(self.AINode.getLinearVelocity() > self.maxSpeed):
				self.AIChar.setH(self.target.getH())
				h = self.AIChar.getH()
				hx = sin(h * DEG_TO_RAD) * 10
				hy = cos(h * DEG_TO_RAD) * 10
				self.AINode.applyForce(Vec3(-hx * self.AISpeed * globalClock.getDt(), hy * self.AISpeed * globalClock.getDt(), 0), PNT)

	def seek(self):
		if(self.AIChar.getDistance(self.target) > 20.0):
			if(self.AINode.getLinearVelocity() > self.maxSpeed):
				self.AIChar.lookAt(self.target)
				h = self.AIChar.getH()
				hx = sin(h * DEG_TO_RAD) * 10
				hy = cos(h * DEG_TO_RAD) * 10
				self.AINode.applyForce(Vec3(-hx * self.AISpeed * globalClock.getDt(), hy * self.AISpeed * globalClock.getDt(), 0), PNT)
		
	def moveToRun(self):
		self.seek()
		# if(self.target.getX()+5 <= self.AIChar.getX() and self.target.getX()-5 >= self.AIChar.getX() and self.target.getY()+5 <= self.AIChar.getY() and self.target.getY()-5 >= self.AIChar.getY()):
			# print("It's stopped!")
			# self.AIChar.clearForces()
			# self.AIChar.setLinearVelocity(0)
		# else:
			# self.AINode.clearForces()
			# self.AIChar.lookAt(self.target)
			# self.AINode.setLinearVelocity(self.AISpeed)
	
	#Gets called on every AIChar in the world's update method to allow the AI to function at all.
	def AIUpdate(self):
		if(self.moveTo == True):
			self.moveToRun()
			
		if(self.type == "seek"):
			self.seek()
		elif(self.type == "flee"):
			self.flee()
		else:
			print("Error @ No AI Type")
	