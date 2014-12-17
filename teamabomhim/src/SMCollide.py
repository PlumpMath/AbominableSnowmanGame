from panda3d.core import BitMask32, Vec3, VBase4, Point3, TransformState
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletTriangleMesh, BulletTriangleMeshShape
from panda3d.bullet import ZUp
from direct.showbase.DirectObject import DirectObject

class SMCollide():

	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Creates a new collision-enabled gameObject.
	# Args:	model - Model path
	#		world - bulletWorld instance
	#		worldNP - world's NodePath
	#		pos - Point3 position
	#		scale - int scale
	#		hpr - Vec3(Heading, Pitch, Rotation)
	#------------------------------------------------------------------------------------------------------------------------------------------------------------

	def __init__(self, model, world, worldNP, pos, scale, hpr):
		self.worldNP = worldNP
		bulletWorld = world
		
		# Initialize the model.
		self.AIModel = loader.loadModel(model)
		self.AINode = BulletRigidBodyNode('AIChar')
		self.AIModel.setScale(scale)
		self.AIModel.flattenLight() # Combines all geom nodes into one geom node.

		# Build the triangle mesh shape and attach it with the transform.
		geom = self.AIModel.findAllMatches('**/+GeomNode').getPath(0).node().getGeom(0)
		mesh = BulletTriangleMesh()
		mesh.addGeom(geom)
		shape = BulletTriangleMeshShape(mesh, dynamic=False)
		self.AINode.addShape(shape, TransformState.makePosHprScale(Point3(0,0,0), hpr, scale))
		self.AINode.setMass(0)
		bulletWorld.attachRigidBody(self.AINode)
		
		# Apply the same transforms on the model being rendered.
		self.AIModel.reparentTo(render)
		self.AIModel.setH(hpr.getX())
		self.AIModel.setP(hpr.getY())
		self.AIModel.setR(hpr.getZ())
		self.AINode.setAngularFactor(Vec3(0,0,0))
		
		# Attach it to the world.
		self.AIChar = self.worldNP.attachNewNode(self.AINode)
		self.AIModel.reparentTo(self.AIChar)
		self.AIChar.setPos(pos)
