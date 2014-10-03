import direct.directbase.DirectStart
from panda3d.core import Vec3, BitMask32, Point3, VBase3
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletRigidBodyNode, BulletDebugNode, BulletCharacterControllerNode
from panda3d.bullet import BulletBoxShape, BulletCapsuleShape, BulletCylinderShape, BulletPlaneShape
from panda3d.bullet import ZUp
from direct.showbase.DirectObject import DirectObject

# Camera setup
base.cam.setPos(8, -30, 8)
base.cam.lookAt(0, 0, 0)
 
# World
world = BulletWorld()
world.setGravity(Vec3(0, 0, -50))
worldNP = render.attachNewNode('World')

# This is actually really useful. It shows collision boxes and other info.
debugNode = BulletDebugNode('Debug')
debugNode.showWireframe(True)
debugNode.showConstraints(True)
debugNode.showBoundingBoxes(True)
debugNode.showNormals(True)
debugNP = render.attachNewNode(debugNode)
 
# Plane
shape = BulletPlaneShape(Vec3(0, 0, 1), 1)
node = BulletRigidBodyNode('Ground')
node.addShape(shape)
np = render.attachNewNode(node)
np.setPos(0, 0, -2)
world.attachRigidBody(node)
 
# Yeti
yetiHeight = 7
yetiRadius = 2

yetiShape = BulletCapsuleShape(yetiRadius, yetiHeight - 2 * yetiRadius, ZUp)

yetiModel = loader.loadModel("models/yeti")
yetiModel.setH(-90)
yetiModel.setPos(0, 0, -1)
yetiModel.flattenLight()

playerNode = BulletRigidBodyNode("Player")
playerNode.setMass(8.0)
playerNode.addShape(yetiShape)
playerNode.setAngularFactor(Vec3(0,0,0))
playerNode.setDeactivationEnabled(False) # Without this disabled, things will weld together after a certain amount of time. It's really annoying.
#playerNode.setLinearDamping(0.9) # We can use this for ice.

playerNP = worldNP.attachNewNode(playerNode)
yetiModel.reparentTo(playerNP)
playerNP.setPos(0, 0, 6)
playerNP.setH(0)

world.attachRigidBody(playerNP.node())
 

# Press F1 to enable debug mode.
def toggleDebug():
  if debugNP.isHidden():
    debugNP.show()
  else:
    debugNP.hide()

# Still working on this.
def move(x, y, pressed):
	if(pressed):
		playerNode.applyForce(Vec3(x, y, 0), Point3(0,0,0))
	else:
		print("up")
		playerNode.applyForce(Vec3(-x, -y, 0), Point3(0,0,0))

# A jump of sorts...
def doJump():
	playerNode.applyForce(Vec3(0, 0, 24000), Point3(0,0,0))
	
world.setDebugNode(debugNP.node())
debugNP.show()

# Keybindings
o = DirectObject()
o.accept('f1', toggleDebug)
o.accept('space', doJump)
o.accept('w', move, [0, 8000, True])
o.accept('s', move, [0, -8000, True])
o.accept('a', move, [-8000, 0, True])
o.accept('d', move, [8000, 0, True])
o.accept('w-up', move, [0, 0, False])
o.accept('s-up', move, [0, 0, False])
o.accept('a-up', move, [0, 0, False])
o.accept('d-up', move, [0, 0, False])

# Update
def update(task):

	

	dt = globalClock.getDt()
	world.doPhysics(dt)
	return task.cont
 
taskMgr.add(update, 'update')
run()