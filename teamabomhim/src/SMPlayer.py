from panda3d.core import Vec3, VBase3, Vec4, BitMask32, Point3, KeyboardButton, Filename, PNMImage, GeoMipTerrain
from panda3d.core import LightRampAttrib, AmbientLight, DirectionalLight
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletRigidBodyNode, BulletDebugNode, BulletCharacterControllerNode
from panda3d.bullet import BulletBoxShape, BulletCapsuleShape, BulletCylinderShape, BulletPlaneShape, BulletHeightfieldShape
from panda3d.bullet import ZUp
from math import sin, cos, pi

MASS = 200.0
TURN_SPEED = 180
DEG_TO_RAD = pi/180
MAX_VEL_XY = 50
MAX_VEL_Z = 5000
MOVE_SPEED = 50.0 * 100000
JUMP_FORCE = 8.0 * 100000
STOP_DAMPING = 5
JMP_STOP_DAMPING = 0.88
TURN_DAMPING = 0.92
PNT = Point3(0,0,0)
	
class SMPlayer():
	
	def __init__(self, wrld, wNP, startX, startY, startZ):
		self.wrld = wrld
		self.wNP = wNP
		self.playerNP = self.setupPlayer(startX, startY, startZ)
		self.isAirborne = True
		self.velocity = Vec3(0,0,0)
		self.rotation = self.playerNP.getH()
		print("Player initialized.")
		
	def getNodePath(self):
		return self.playerNP
	
	def setupPlayer(self, x, y, z):
		yetiHeight = 7
		yetiRadius = 2
		yetiShape = BulletCapsuleShape(yetiRadius, yetiHeight - 2 * yetiRadius, ZUp)
		yetiModel = loader.loadModel("../res/models/yeti.egg")
		yetiModel.setH(90)
		yetiModel.setPos(0, 0, -1) # This is NOT the actual player position. Use playerNP instead.
		yetiModel.flattenLight()
		playerNode = BulletRigidBodyNode("Player")
		playerNode.setMass(MASS)
		playerNode.addShape(yetiShape)
		
		# Without this set to 0,0,0, the Yeti would wobble like a Weeble but not fall down.
		playerNode.setAngularFactor(Vec3(0,0,0))

		# Without this disabled, things will weld together after a certain amount of time. It's really annoying.
		playerNode.setDeactivationEnabled(False) 
		
		playerNP = self.wNP.attachNewNode(playerNode)
		playerNP.setPos(x, y, z)
		playerNP.setH(0)
		yetiModel.reparentTo(playerNP)
		self.wrld.attachRigidBody(playerNP.node())
		return playerNP
	
	def jump(self):
		if(self.getVelocity().getZ() > 5):
			self.setAirborneFlag(True)
		elif(self.isAirborne == False):
			self.setAirborneFlag(True)
			print("Jump successful")
			self.applyForce(Vec3(0, 0, JUMP_FORCE))
	
	def setAirborneFlag(self, flag):
		self.isAirborne = flag
	
	# True = forward, False = backward
	def move(self, dir):
		x = 0
		y = 0
		if(self.getSpeed().getY() > MAX_VEL_XY):
			y = 0
		elif(self.getSpeed().getX() > MAX_VEL_XY):
			x = 0
		else:
			if(dir):
				self.applyForce(Vec3((-MOVE_SPEED * globalClock.getDt()) * sin(self.getRotation() * DEG_TO_RAD), (MOVE_SPEED * globalClock.getDt()) * cos(self.getRotation() * DEG_TO_RAD), 0))
			else:
				self.applyForce(Vec3((MOVE_SPEED * globalClock.getDt()) * sin(self.getRotation() * DEG_TO_RAD) / 2, (-MOVE_SPEED * globalClock.getDt()) * cos(self.getRotation() * DEG_TO_RAD) / 2, 0))
	
	def stop(self):
		vx = self.getVelocity().getX()
		vy = self.getVelocity().getY()
		vz = self.getVelocity().getZ()
		dt = globalClock.getDt()
		self.setVelocity(Vec3((vx - (vx * STOP_DAMPING * dt)), (vy - (vy * STOP_DAMPING * dt)), vz))
	
	# True = CCW, False = CW
	def turn (self, dir):
		t = globalClock.getDt() * TURN_SPEED
		if(dir == False):
			t = t * -1
		self.setRotation(self.getRotation() + t)
	
	def getPosition(self):
		return self.playerNP.getPos()
	
	def applyForce(self, force):
		self.playerNP.node().applyForce(force, PNT)
		
	def getVelocity(self):
		return self.playerNP.node().getLinearVelocity()
		
	def setVelocity(self, vel):
		self.playerNP.node().setLinearVelocity(vel)
	
	def getSpeed(self):
		x = abs(self.getVelocity().getX())
		y = abs(self.getVelocity().getY())
		z = abs(self.getVelocity().getZ())
		return Vec3(x, y, z)
	
	def getRotation(self):
		return self.playerNP.getH()
	
	def setRotation(self, angle):
		self.playerNP.setH(angle)
	
	def setAnimation(self, id):
		print("TODO: set animation.")
