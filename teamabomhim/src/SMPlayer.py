from panda3d.core import Vec3, VBase3, Vec4, BitMask32, Point3, KeyboardButton, Filename, PNMImage, GeoMipTerrain, VBase4
from direct.gui.OnscreenText import OnscreenText
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
SLIP_THRESHOLD = 0.30
PNT = Point3(0,0,0)
SNOW_HEIGHT = -2.1
SOLID_HEIGHT = -1.8

# Stuff for reading and displaying information from the friction map.
# FRICTION_LBL = OnscreenText(text = 'coefficient of friction: ', pos = (0, 0), scale = 0.1)
TEXPK = loader.loadTexture('../maps/map01-f.png').peek()
TXX = TEXPK.getXSize()
TXY = TEXPK.getYSize()
CALC_COF = lambda x: 0.4 * x + 0.05

class SMPlayer():
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Constructor
	# (BulletWorld, NodePath of BulletWorld, int, int, int)
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def __init__(self, wrld, wNP, smWrld, startX, startY, startZ, audMgr):
		self.bulletWorld = wrld
		self.worldNP = wNP
		self.smWorld = smWrld
		self.startX = startX
		self.startY = startY
		self.startZ = startZ
		self.audioMgr = audMgr
		self.playerNP = self.setupPlayer(self.startX, self.startY, self.startZ)
		self.isAirborne = True
		self.terrainType = -1
		self.velocity = Vec3(0,0,0)
		self.rotation = self.playerNP.getH()
		self.rollingSnowball = False
		self.fric = 0.45
		print("Player initialized.")
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Returns the player class' NodePath
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def getNodePath(self):
		return self.playerNP
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Sets up and spawns the player at the specified coordinates. 
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def setupPlayer(self, x, y, z):
		yetiHeight = 7
		yetiRadius = 2
		yetiShape = BulletCapsuleShape(yetiRadius, yetiHeight - 2 * yetiRadius, ZUp)
		yetiModel = loader.loadModel("../res/models/yeti.egg")
		yetiModel.setH(90)
		yetiModel.setPos(0, 0, SNOW_HEIGHT) # This is NOT the actual player position. Use playerNP instead.
		yetiModel.flattenLight()
		playerNode = BulletRigidBodyNode("Player")
		playerNode.setMass(MASS)
		playerNode.addShape(yetiShape)
		
		# Without this set to 0,0,0, the Yeti would wobble like a Weeble but not fall down.
		playerNode.setAngularFactor(Vec3(0,0,0))

		# Without this disabled, things will weld together after a certain amount of time. It's really annoying.
		playerNode.setDeactivationEnabled(False)
		
		playerNP = self.worldNP.attachNewNode(playerNode)
		playerNP.setPos(x, y, z)
		playerNP.setH(0)
		yetiModel.reparentTo(playerNP)
		self.bulletWorld.attachRigidBody(playerNP.node())
		return playerNP
	
	
	def getPlayerNode(self):
		return playerNode
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Makes the player jump if they are not already jumping.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def jump(self):
		# if(abs(self.getVelocity().getZ()) < 10):
			# self.setAirborneFlag(True)
		if(self.isAirborne == False):
			v = self.getVelocity()
			self.setAirborneFlag(True)
			# print("Jump successful")
			self.setFactor(1, 1, 1)
			self.setVelocity(Vec3(v.getX(), v.getY(), 0))
			# self.audioMgr.playSFX("yetiJump01")
			self.applyForce(Vec3(0, 0, JUMP_FORCE))
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Returns the airborne flag.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def getAirborneFlag(self):
		return self.isAirborne
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Sets the airborne flag.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def setAirborneFlag(self, flag):
		self.isAirborne = flag
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Sets the terrain type.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def setTerrain(self, terID):
		self.terrainType = terID
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Turns the player
	# (direction True = CCW; False = CW)
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def turn (self, dir):
		t = globalClock.getDt() * TURN_SPEED
		self.setFactor(0, 0, 1)
		if(dir == False):
			t = t * -1
		self.setRotation(self.getRotation() + t)
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Moves the player forward or backward relative to their rotation.
	# (direction True = Forward; False = Backward)
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def move(self, dir):
		global MOVE_SPEED
		
		self.stop()
		
		if((self.getSpeed().getY() <= MAX_VEL_XY) and (self.getSpeed().getX() <= MAX_VEL_XY)):
			xFactor = sin(self.getRotation() * DEG_TO_RAD)
			yFactor = cos(self.getRotation() * DEG_TO_RAD)
			self.setFactor(1, 1, 1)
			if(dir):
				self.applyForce(Vec3((-MOVE_SPEED * globalClock.getDt()) * xFactor, (MOVE_SPEED * globalClock.getDt()) * yFactor, 0))
			else:
				self.applyForce(Vec3((MOVE_SPEED * globalClock.getDt()) * xFactor / 2, (-MOVE_SPEED * globalClock.getDt()) * yFactor / 2, 0))
		
		
		color = VBase4(0, 0, 0, 0)
		TEXPK.lookup(color, (self.playerNP.getX() + TXX / 2) / TXX, (self.playerNP.getY() + TXY / 2) / TXY)
		
		# Here is where you would use CALC_COF(color.getX()) to set the ground friction
		# Note, the use of the label really slows down drawing.
		# FRICTION_LBL.setText('coefficient of friction: ' + str(CALC_COF(color.getX())))
		self.fric = CALC_COF(color.getX())
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Prevents DHP (Dukes of Hazard Phenomenon)
	# (h = Terrain height at X,y; th = terrain z coord)
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def snapToTerrain(self, h, th):
		pos = self.getPosition()
		x = pos.getX()
		y = pos.getY()
		self.playerNP.setPos(x, y, (h - (th / 2)) + 4.5)
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Slows down and stops the player's horizontal movement.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def stop(self):
		# print(self.getTerrainHeight())
		vx = self.getVelocity().getX()
		vy = self.getVelocity().getY()
		vz = self.getVelocity().getZ()
		if(not(self.isAirborne)):
			vz = 0
		dt = globalClock.getDt()
		if(self.fric < SLIP_THRESHOLD and self.getSpeed() > 5.0):
			self.setFactor(1, 1, 1)
			self.setVelocity(Vec3((vx - (vx * dt)), (vy - (vy * dt)), vz))
		else:
			self.setFactor(0, 0, 1)
			self.setVelocity(Vec3((vx - (vx * STOP_DAMPING * dt)), (vy - (vy * STOP_DAMPING * dt)), vz))
	
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Sets the player's position to the spawn position.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def respawn(self):
		self.fric = 0.45
		self.playerNP.setPos(self.startX, self.startY, self.startZ)
		self.setVelocity(Vec3(0,0,0))
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Returns true if the player is rolling a snowball.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def hasSnowball(self):
		return self.rollingSnowball
	
	def setRolling(self, roll):
		self.rollingSnowball = roll
	
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Gets the player's friction value at its position.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def getFriction(self):
		return self.fric
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Gets the player's current Point3 position.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def getPosition(self):
		return self.playerNP.getPos()
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Sets the player's current Point3 position.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def setPosition(self, pos):
		x = pos.getX()
		y = pos.getY()
		z = pos.getZ()
		self.playerNP.setPos(x, y, z)
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Sets the player's movement factors
	# 0 < x/y/z < 1; 0 = No movement; 1 = Full movement
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def setFactor(self, x, y, z):
		self.playerNP.node().setLinearFactor(Vec3(x, y, z))
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Applies a force vector.
	# (Vec3 force)
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def applyForce(self, force):
		self.playerNP.node().applyForce(force, PNT)
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Gets the player's current velocity as a Vec3
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def getVelocity(self):
		return self.playerNP.node().getLinearVelocity()
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Sets the player's current velocity with the specified Vec3
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def setVelocity(self, vel):
		self.playerNP.node().setLinearVelocity(vel)
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Gets the player's speed Vec3.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def getSpeed(self):
		x = abs(self.getVelocity().getX())
		y = abs(self.getVelocity().getY())
		z = abs(self.getVelocity().getZ())
		return Vec3(x, y, z)
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Gets the player's rotation.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def getRotation(self):
		return self.playerNP.getH()
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Sets the player's rotation.
	# -359 < angle < 359
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def setRotation(self, angle):
		self.playerNP.setH(angle)
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Sets the player's animation loop.
	# WORK IN PROGRESS.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def setAnimation(self, id):
		print("[!] Not yet implemented!")
