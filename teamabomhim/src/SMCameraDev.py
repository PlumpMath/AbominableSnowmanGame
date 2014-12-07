from panda3d.core import Vec3, Point3, NodePath
from panda3d.bullet import BulletRigidBodyNode, BulletSphereShape, ZUp
from math import sin, cos, pi, sqrt

MIN_DISTANCE = 10.0
MAX_DISTANCE = 80.0
ZOOM_RATE = 50.0
DEG_TO_RAD = pi/180
TURN_SENSITIVITY = 40
RESET_SPEED = 8
COL_RADIUS = 2

class SMCamera():
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Default constructor
	# SMCamera(SMPlayer object, BulletWorld object, World NodePath)
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def __init__(self, pObj, bwObj, wObj):
		self.playerObj = pObj
		self.worldObj = wObj
		self.bulletWorld = bwObj
		self.playerNP = pObj.getNodePath()
		self.distance = 50.0
		self.angle = 90.0
		self.aimMode=False

		# Set up camera physics
		camShape = BulletSphereShape(COL_RADIUS)
		camRB = BulletRigidBodyNode("cameraRB")
		camRB.setMass(1.0)
		camRB.addShape(camShape)
		camRB.setAngularFactor(Vec3(0,0,0))
		camRB.setDeactivationEnabled(False)
		
		self.camNP = self.worldObj.attachNewNode(camRB)
		self.bulletWorld.attachRigidBody(camRB)
		
		base.cam.reparentTo(self.camNP)
		self.camNP.reparentTo(self.playerObj.getNodePath())
		self.calculatePosition()
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Returns the camera's angle relative to the player.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def getAngle(self):
		return self.angle
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Gradually rotates the camera to the specified angle.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def rotateTowards(self, targ):
		self.normalizeAngle()
		if(targ != self.angle):
			rAng = targ % 360
			d1 = targ - self.angle
			d2 = 360 - d1
			amt = min(d1, d2)
			dir = (amt > 0)
			dt = globalClock.getDt()
			self.angle += (amt * dt * RESET_SPEED / 2)
			if(dir):
				if(round(self.angle, 2) > targ - 0.01):
					self.angle = targ
			else:
				if(round(self.angle, 2) < targ + 0.01):
					self.angle = targ
			self.calculatePosition()
				
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Sets the camera's angle.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def setAngle(self, deg):
		self.angle = deg
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Zoom the camera in.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def zoomIn(self):
		if(self.distance > MIN_DISTANCE):
			self.distance -= (ZOOM_RATE * globalClock.getDt())
		else:
			self.distance = MIN_DISTANCE
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Zoom the camera out.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def zoomOut(self):
		if(self.distance < MAX_DISTANCE):
			self.distance += (ZOOM_RATE * globalClock.getDt())
		else:
			self.distance = MAX_DISTANCE
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Moves the camera along a circle around the player.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def rotateCamera(self, amt):
		self.angle += amt * TURN_SENSITIVITY
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Sets the camera's distance from the player.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def setDistance(self, dist):
		self.distance = dist
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Sets the angle to something equivalent from 0 to 360.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def normalizeAngle(self):
		if(self.angle > 0):
			self.angle %= 360
		else:
			self.angle = (360 - self.angle) % 360
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Makes the camera look at the player.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def lookAtPlayer(self):
		#if(self.aimMode==False):
			base.cam.lookAt(self.playerNP)
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Set the camera's position based on its distance, and the player's rotation.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def calculatePosition(self):
		pos = self.camNP.getPos()
		
		px = pos.getX()
		py = pos.getY()
		pz = pos.getZ()
		
		cx = cos(self.angle * DEG_TO_RAD)
		cy = sin(self.angle * DEG_TO_RAD)
		cz = ((1000 / ((self.distance + 10) / 2))) - 20
		
		self.camNP.setPos(self.distance * (-cx), self.distance * (-cy), cz)
		self.lookAtPlayer()
		
	def getNodePath(self):
		return self.camNP

	def aimMode(self):
		self.aimMode = True
		self.setDistance(25.0)