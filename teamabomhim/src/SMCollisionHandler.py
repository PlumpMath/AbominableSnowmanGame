from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletRigidBodyNode, BulletDebugNode, BulletCharacterControllerNode
from panda3d.bullet import BulletBoxShape, BulletCapsuleShape, BulletCylinderShape, BulletPlaneShape, BulletHeightfieldShape

class SMCollisionHandler():

	def __init__(self, wrld):
		self.world = wrld

	def didCollide(self, no1, no2):
		contactTest = self.world.contactTestPair(no1, no2)
		contactList = contactTest.getContacts()
		for c in contactList:
			c1 = c.getNode0().getName()
			c2 = c.getNode1().getName()
			if(c1 == no1.getName() and c2 == no2.getName()):
				return True
		return False