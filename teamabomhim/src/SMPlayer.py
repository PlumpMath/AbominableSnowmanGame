from panda3d.core import Vec3, VBase3, Vec4, BitMask32, Point3, KeyboardButton, Filename, PNMImage, GeoMipTerrain, VBase4
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import LightRampAttrib, AmbientLight, DirectionalLight
from direct.actor.Actor import Actor
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletRigidBodyNode, BulletDebugNode, BulletCharacterControllerNode
from panda3d.bullet import BulletBoxShape, BulletCapsuleShape, BulletCylinderShape, BulletPlaneShape, BulletHeightfieldShape
from panda3d.bullet import ZUp
from math import sin, cos, pi, sqrt

# Physics attributes
MASS = 200.0
TURN_SPEED = 95
DEG_TO_RAD = pi/180
MAX_VEL_XY = 70
MAX_VEL_Z = 5000
MOVE_SPEED = 85.0 * 100000
JUMP_FORCE = 7.0 * 100000
STOP_DAMPING = 10
JMP_STOP_DAMPING = 0.88
TURN_DAMPING = 0.92
SLIP_THRESHOLD = 0.30
JUMP_CONTROL_TIME = 0.20
PNT = Point3(0,0,0)

# Snow-based Actions
MAX_SNOW = 100.0
COST_DOUBLE_JUMP = 0.0
COST_AIR_DASH = 10.0

# Smooth this out later
SNOW_HEIGHT = -3.8
SOLID_HEIGHT = -2.5

# Terrain enumeration
TERRAIN_SNOW = 0
TERRAIN_ICE = 1
TERRAIN_STONE = 2

# Animation IDs
ANIM_IDLE = 0
ANIM_WALK = 1
ANIM_JUMP = 2
ANIM_FALL = 3
ANIM_ROLL = 4


class SMPlayer():
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Constructor
	# (BulletWorld, NodePath of BulletWorld, Point3, AudioManager object)
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def __init__(self, wrld, wNP, smWrld, startPos, audMgr):
		self.bulletWorld = wrld
		self.worldNP = wNP
		self.smWorld = smWrld
		self.startX = startPos.getX()
		self.startY = startPos.getY()
		self.startZ = startPos.getZ()
		self.audioMgr = audMgr
		self.playerNP = self.setupPlayer(self.startX, self.startY, self.startZ)
		self.isAirborne = True
		self.jumpDown = False
		self.doubleJumping = False
		self.doubleJumpCount = 0
		self.rollingSnowball = False
		self.terrainType = -1
		self.velocity = Vec3(0,0,0)
		self.rotation = self.playerNP.getH()
		self.sc = 0.00
		self.ic = 0.00
		self.fric = 0.45
		self.snowAbsorbed = 0
		self.currentAnimation = ANIM_IDLE
		
		# Stuff for reading and displaying information from the maps.
		map = self.smWorld.mapName
		self.FPK = loader.loadTexture('../maps/map' + map + "/map" + map + '-f.png').peek()
		self.IPK = loader.loadTexture('../maps/map' + map + "/map" + map + '-i.png').peek()
		self.SPK = loader.loadTexture('../maps/map' + map + "/map" + map + '-s.png').peek()
		self.FX = self.FPK.getXSize()
		self.FY = self.FPK.getYSize()
		self.IX = self.IPK.getXSize()
		self.IY = self.IPK.getYSize()
		self.SX = self.SPK.getXSize()
		self.SY = self.SPK.getYSize()
		self.CALC_COF = lambda x: 0.4 * x + 0.05
		self.CALC_SINK = lambda x: 1.5 * x - 0.3
		self.updateTerrain()
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
		
		modelPrefix = "../res/models/yeti_"
		self.yetiModel = Actor("../res/models/yeti.egg", {"idle":"../res/models/yeti_idle.egg", "walk":"../res/models/yeti_walking.egg"})
		self.yetiModel.setH(90)
		self.yetiModel.setPos(0, 0, SNOW_HEIGHT)

		playerNode = BulletRigidBodyNode("Player")
		playerNode.setMass(MASS)
		playerNode.addShape(yetiShape)
		
		# Without this set to 0,0,0, the Yeti would wobble like a Weeble but not fall down.
		playerNode.setAngularFactor(Vec3(0,0,0))

		# Without this disabled, things will weld together after a certain amount of time. It's really annoying.
		playerNode.setDeactivationEnabled(False)
		
		playerNP = self.worldNP.attachNewNode(playerNode)
		playerNP.setPos(x, y, z)
		playerNP.setH(270)
		
		self.yetiModel.reparentTo(playerNP)
		
		self.bulletWorld.attachRigidBody(playerNP.node())
		
		# Hopefully Brandon will get those animation files to me so I can convert them.
		# self.setAnimation('idle')
		
		return playerNP
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Returns the player's BulletRigidBodyNode (may cause a crash; haven't looked into it).
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def getPlayerNode(self):
		return playerNode
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Adds snow to the snow meter.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def addSnow(self, amt):
		if(self.snowAbsorbed + amt >= MAX_SNOW):
			self.snowAbsorbed = MAX_SNOW
		else:
			self.snowAbsorbed += amt
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Sets the snow meter to a specified amount.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def setSnow(self, value):
		self.snowAbsorbed = value
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Returns the amount of snow the player has collected.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def getSnow(self):
		return self.snowAbsorbed
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Resets the jump flag.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def resetJump(self):
		self.jumpDown = False
	
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Makes the player jump if they are not already jumping, or double jump if they have enough Mahou Shoujo power.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def jump(self):
	
		# This line is long. 
		if((self.snowAbsorbed >= COST_DOUBLE_JUMP * (self.doubleJumpCount + 1)) and self.isAirborne == True and self.jumpDown == False and self.doubleJumpCount < 2):
			self.jumpDown = True
			self.doubleJumping = False
			self.doubleJumpCount += 1
			self.snowAbsorbed -= (COST_DOUBLE_JUMP * self.doubleJumpCount)
			
			# The closer to 0, the more force, otherwise, it's less.
			vz = self.getVelocity().getZ()
			if(vz < 0.1):
				vz = 0.1
			zForce = 3 / sqrt(abs(vz))
			if (zForce > 1.0):
				zForce = 1.0
			self.applyForce(Vec3(0, 0, JUMP_FORCE * zForce))
			
		elif(self.isAirborne == False and self.jumpDown == False):
			self.doubleJumpCount = 0
			self.jumpDown = True
			self.doubleJumping = False
			self.jumpTime = JUMP_CONTROL_TIME
			v = self.getVelocity()
			self.setAirborneFlag(True)
			self.setFactor(1, 1, 1)
			self.setVelocity(Vec3(v.getX(), v.getY(), 0))
			self.applyForce(Vec3(0, 0, JUMP_FORCE))
		elif(self.jumpTime > 0 and self.jumpDown == True and self.doubleJumping == False):
			dt = globalClock.getDt()
			self.applyForce(Vec3(0, 0, JUMP_FORCE * dt * self.jumpTime * 30))
			self.jumpTime -= dt
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Performs an air dash.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def airDash(self):
		if(self.snowAbsorbed >= COST_AIR_DASH):
			self.snowAbsorbed -= COST_AIR_DASH
			fx = -sin(self.getRotation() * DEG_TO_RAD)
			fy = cos(self.getRotation() * DEG_TO_RAD)
			self.setVelocity(Vec3(MAX_VEL_XY * fx * 8, MAX_VEL_XY * fy * 8, -5))
	
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
	# Updates various things to do with the terrain type.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def updateTerrain(self):
		
		# Prevent this from happening if we're airborne
		if(self.isAirborne == False):
		
			# Stone
			if(self.sc <= 0.2 and self.ic <= 0.2):
				self.setTerrain(TERRAIN_STONE)
			else:
				
				# Ice (takes priority over snow)
				if(self.ic >= self.sc):
					self.setTerrain(TERRAIN_ICE)
				else:
					self.setTerrain(TERRAIN_SNOW)
					
			# Set player height accordingly
			mpos = self.yetiModel.getPos()
			mx = mpos.getX()
			my = mpos.getY()
			h = self.CALC_SINK(self.sc)
			self.yetiModel.setPos(mx, my, SOLID_HEIGHT - h)

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
		
		fr = VBase4(0, 0, 0, 0)
		self.FPK.lookup(fr, (self.playerNP.getX() + self.FX / 2) / self.FX, (self.playerNP.getY() + self.FY / 2) / self.FY)
		
		ice = VBase4(0, 0, 0, 0)
		self.IPK.lookup(ice, (self.playerNP.getX() + self.IX / 2) / self.IX, (self.playerNP.getY() + self.IY / 2) / self.IY)
		
		snow = VBase4(0, 0, 0, 0)
		self.SPK.lookup(snow, (self.playerNP.getX() + self.SX / 2) / self.SX, (self.playerNP.getY() + self.SY / 2) / self.SY)
		
		# Here is where you would use CALC_COF(color.getX()) to set the ground friction
		self.fric = self.CALC_COF(fr.getX())
		self.ic = ice.getX()
		self.sc = snow.getX()
		self.updateTerrain()

	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Prevents DHP (Dukes of Hazard Phenomenon)
	# (h = Terrain height at X,y; th = terrain z coord)
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def snapToTerrain(self, z):
		pos = self.getPosition()
		x = pos.getX()
		y = pos.getY()
		self.playerNP.setPos(x, y, z + 5)
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Slows down and stops the player's horizontal movement.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def stop(self):
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
		self.updateTerrain()
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Sets the player's position to the spawn position.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def respawn(self):
		self.fric = 0.45
		self.playerNP.setPos(self.startX, self.startY, self.startZ + 1)
		self.setVelocity(Vec3(0,0,0))
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Returns true if the player is rolling a snowball.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def hasSnowball(self):
		return self.rollingSnowball
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Sets the rolling snowball state.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def setRolling(self, roll):
		self.rollingSnowball = roll
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Gets the snow coefficient of the player's (x,y)
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def getSnowCoefficient(self):
		return self.sc
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Gets the ice coefficient of the player's (x,y)
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def getIceCoefficient(self):
		return self.ic
	
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
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def setAnimation(self, anim):
		self.yetiModel.stop()
		self.yetiModel.loop(anim)
		
