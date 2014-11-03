from panda3d.core import Vec3, Point3

from math import sin, cos, pi, sqrt

MAX_DISTANCE = 50
DEG_TO_RAD = pi/180
TURN_SENSITIVITY = 5

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
		if(targ != self.angle):
			rAng = targ % 360
			d1 = 360 - rAng
			d2 = abs(0 - rAng)
			amt = min(d1, d2)
			dir = (d1 < d2)
			if(dir):
				self.angle -= amt
				if(self.angle > targ):
					self.angle = targ
			else:
				self.angle += amt
				if(self.angle < targ):
					self.angle = targ
				
		
	def setAngle(self, deg):
		self.angle = deg
		self.angle %= 360
	
	def rotateCamera(self, amt):
		self.angle += amt * 10
		self.angle %= 360
	
	def setDistance(self, dist):
		self.distance = dist
	
	def lookAtPlayer(self):
		base.cam.lookAt(self.playerNP)
	
	def calculatePosition(self):
		pos = base.cam.getPos()
		
		px = pos.getX()
		py = pos.getY()
		pz = pos.getZ()
		
		cx = cos(self.angle * TURN_SENSITIVITY * DEG_TO_RAD)
		cy = sin(self.angle * TURN_SENSITIVITY * DEG_TO_RAD)
		cz = 6
		
		base.cam.setPos(self.distance * (-cx), self.distance * (-cy), cz)
		self.lookAtPlayer()

