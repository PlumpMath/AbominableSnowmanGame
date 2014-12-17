from panda3d.core import BitMask32, Vec3, Vec4, PNMImage, Filename, GeoMipTerrain, TextureStage, VBase4, Point3, TransformState
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletRigidBodyNode, BulletDebugNode, BulletCharacterControllerNode, BulletGhostNode
from panda3d.bullet import BulletBoxShape, BulletCapsuleShape, BulletCylinderShape, BulletPlaneShape, BulletHeightfieldShape, BulletTriangleMesh, BulletTriangleMeshShape
from panda3d.bullet import ZUp
from direct.showbase.DirectObject import DirectObject
from direct.showbase.Transitions import Transitions

from math import sin, cos, pi

class SMCollide():

	def __init__(self, model, world, worldNP, x, y, z, sizeX, sizeY, sizeZ, scale, rot):
		# self.AIX = x
		# self.AIY = y
		# self.AIZ = z
		self.worldNP = worldNP
		bulletWorld = world
		
		self.AIModel = loader.loadModel(model)
		self.AINode = BulletRigidBodyNode('AIChar')
		self.AIModel.setScale(scale)
		self.AIModel.flattenLight()
		
		# for gnp in self.AIModel.findAllMatches('**/+GeomNode'):
			# print("Match")
			# gnode = gnp.node()
			# ts = TransformState.makePosHprScale(Point3(x, y, z), Vec3(rot, 0, 0), Vec3(scale, scale, scale))
			# geom = gnode.getGeom(0)
			# mesh = BulletTriangleMesh()
			# mesh.addGeom(geom, True)
			# shape = BulletTriangleMeshShape(mesh, dynamic=False)
			# self.AINode.addShape(shape, ts)
			
		geom = self.AIModel.findAllMatches('**/+GeomNode').getPath(0).node().getGeom(0)
		mesh = BulletTriangleMesh()
		mesh.addGeom(geom)
		shape = BulletTriangleMeshShape(mesh, dynamic=False)
		self.AINode.addShape(shape, TransformState.makePosHprScale(Point3(0,0,0), Vec3(rot,0,0), scale))
		self.AINode.setMass(0)
		bulletWorld.attachRigidBody(self.AINode)
		
		
		self.AIModel.reparentTo(render)
		self.AIModel.setH(rot)
		
		
		# AIShape = BulletBoxShape(Vec3(sizeX, sizeY, sizeZ))
		# self.AINode.addShape(AIShape)
		
		self.AINode.setAngularFactor(Vec3(0,0,0))
		# render.attachNewNode(self.AINode)
		
		self.AIChar = self.worldNP.attachNewNode(self.AINode)
		self.AIModel.reparentTo(self.AIChar)
		# self.AIChar.setCollideMask(BitMask32.allOn())
		self.AIChar.setPos(x, y, z)