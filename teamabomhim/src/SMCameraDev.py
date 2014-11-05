from panda3d.core import Vec3, Point3

from math import sin, cos, pi, sqrt

MAX_DISTANCE = 50
DEG_TO_RAD = pi/180
TURN_SENSITIVITY = 40
RESET_SPEED = 8

class SMCamera():
	
	def __init__(self, pObj):
		self.playerObj = pObj
		self.playerNP = pObj.getNodePath()
		self.distance = 50
		self.angle = 90
		base.cam.reparentTo(self.playerNP)
		self.calculatePosition()
	
	def getAngle(self):
		return self.angle
	
	def rotateTowards(self, targ):
		self.normalizeAngle()
		if(targ != self.angle):
			print("Angle: " + str(self.angle))
			rAng = targ % 360
			d1 = targ - self.angle
			print("d1: " + str(d1))
			d2 = 360 - d1
			print("d2: " + str(d2))
			amt = min(d1, d2)
			print("Change: " + str(amt))
			dir = (amt > 0)
			print(dir)
			dt = globalClock.getDt()
			self.angle += (amt * dt * RESET_SPEED / 2)
			if(dir):
				if(round(self.angle, 2) > targ - 0.01):
					self.angle = targ
			else:
				if(round(self.angle, 2) < targ + 0.01):
					self.angle = targ
			self.calculatePosition()
				
		
	def setAngle(self, deg):
		self.angle = deg
		self.normalizeAngle()
	
	def rotateCamera(self, amt):
		self.angle += amt * TURN_SENSITIVITY
	
	def setDistance(self, dist):
		self.distance = dist
	
	def normalizeAngle(self):
		if(self.angle > 0):
			self.angle %= 360
		else:
			self.angle = (360 - self.angle) % 360
	
	def lookAtPlayer(self):
		base.cam.lookAt(self.playerNP)
	
	def calculatePosition(self):
		# self.normalizeAngle()
		
		pos = base.cam.getPos()
		
		px = pos.getX()
		py = pos.getY()
		pz = pos.getZ()
		
		cx = cos(self.angle * DEG_TO_RAD)
		cy = sin(self.angle * DEG_TO_RAD)
		cz = 6
		
		base.cam.setPos(self.distance * (-cx), self.distance * (-cy), cz)
		self.lookAtPlayer()

