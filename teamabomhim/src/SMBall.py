#this could be slimmed down but im lazy
import direct.directbase.DirectStart
from panda3d.core import Vec3, VBase3, Vec4, BitMask32, Point3, KeyboardButton, Filename, PNMImage, GeoMipTerrain
from panda3d.core import LightRampAttrib, AmbientLight, DirectionalLight
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletRigidBodyNode, BulletDebugNode, BulletCharacterControllerNode
from panda3d.bullet import BulletBoxShape, BulletCapsuleShape, BulletCylinderShape, BulletPlaneShape, BulletHeightfieldShape
from panda3d.bullet import ZUp
from math import sin, cos, pi
from direct.showbase.DirectObject import DirectObject
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletSphereShape

MAXSCALE = 10

class SMBall():
	def __init__(self, wrld, wNP, startX, startY, startZ):
		
		self.wrld = wrld
		self.wNP = wNP
		self.ballNP = self.setupball(startX, startY, startZ)
		self.numSnoBall = 0
		print("ball initialized.")
		
	def getNodePath(self):
		return self.ballNP
	
	def setupball(self, x, y, z):
		ballShape = BulletSphereShape(1)
		ballModel = loader.loadModel("../res/models/sphere.egg.pz")
		ballModel.setH(90)
		ballModel.setPos(0, 0, -1) # This is NOT the actual player position. Use playerNP instead.
		ballModel.flattenLight()
		ballNode = BulletRigidBodyNode("Sphere")
		ballNode.setMass(8.0)
		ballNode.addShape(ballShape)
		#SNOWBALL!!!!!
		ballNP = self.wNP.attachNewNode(ballNode)
		ballNP.setPos(x, (y+1), z)
		ballNP.setH(0)
		ballModel.reparentTo(ballNP)
		self.wrld.attachRigidBody(ballNP.node())
		return ballNP
	
	#changing the size
	#def setScale(self, s):
	#	if(s < MAXSCALE)
	#		self.bulletRigidBody.setScale(s,s,s)
	
	#Destroy SSNOWBALL!!!!
	def destroy(self):
		for m in self.set1.getChildren():
			m.destroy()
			self.set1.removeNode()
			self.numSnoBall= self.numSnoBall- 1
	
	def create(self, x, y, z):
		#only want 1 snowball or no snowball
		self.numSnoBall= self.numSnoBall + 1
		if(self.numSnoBall <= 2):	
			ballShape = BulletSphereShape(1)
		
			ballModel = loader.loadModel("../res/models/sphere.egg.pz")
			ballModel.setH(90)
			ballModel.setPos(0, 0, -1) # This is NOT the actual ball position. Use playerNP instead.
			ballModel.flattenLight()
		
			ballNode = BulletRigidBodyNode("Sphere")
			ballNode.setMass(8.0)
			ballNode.addShape(ballShape)
			ballNP = self.wNP.attachNewNode(ballNode)
			ballNP.setPos(x, (y+1), z)
			ballNP.setH(0)
			ballModel.reparentTo(ballNP)
			self.wrld.attachRigidBody(ballNP.node())
	
	#because players make snowballs		
	#SetParent(SMPlayer)
	