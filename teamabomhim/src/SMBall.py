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
	def __init__(self, wrld, wNP, playerNP):
		self.playerNP = playerNP 
		self.wrld = wrld
		self.wNP = wNP
		ballShape = BulletSphereShape(1)
		self.ballModel = loader.loadModel("../res/models/sphere.egg.pz")
		self.ballModel.setH(90)
		self.ballModel.setPos(0, 0, -1) # This is NOT the actual player position. Use playerNP instead.
		self.ballModel.flattenLight()
		self.ballNode = BulletRigidBodyNode("Sphere")
		self.ballNode.setMass(1.0)
		self.ballNode.addShape(ballShape)
		#SNOWBALL!!!!!
		self.ballNP = self.wNP.attachNewNode(self.ballNode)
		self.ballNP.setH(0)
		self.numSnoBall = 0
		
		self.wrld.attachRigidBody(self.ballNP.node())
		# Without this set to 0,0,0, the Yeti would wobble like a Weeble but not fall down.
		self.ballNode.setAngularFactor(Vec3(0,0,0))
	
		# Without this disabled, things will weld together after a certain amount of time. It's really annoying.
		self.ballNode.setDeactivationEnabled(False)
		print("ball initialized.")
			
	def getNodePath(self):
		return self.ballNP
	
	

	
	def create(self, x, y, z):
		print(x,y,z)
		self.ballNP.setPos(x, y, z)
		self.ballModel.reparentTo(self.ballNP)
	
	