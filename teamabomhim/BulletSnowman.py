import direct.directbase.DirectStart
from panda3d.core import Vec3, BitMask32, Point3, KeyboardButton
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletRigidBodyNode, BulletDebugNode, BulletCharacterControllerNode
from panda3d.bullet import BulletBoxShape, BulletCapsuleShape, BulletCylinderShape, BulletPlaneShape
from panda3d.bullet import ZUp
from math import sin, cos, pi
from direct.showbase.DirectObject import DirectObject

# Constants
DEBUG = True
TURN_SPEED = 180
DEG_TO_RAD = pi/180
MAX_VEL_XY = 50
MAX_VEL_Z = 5000
GRAVITY = 25
MOVE_SPEED = 500
PNT = Point3(0,0,0)

def debugP(message):
	if(DEBUG):
		print(message)

# Keybindings
keyForward = KeyboardButton.ascii_key('w')
keyBack = KeyboardButton.ascii_key('s')
keyLeft = KeyboardButton.ascii_key('a')
keyRight = KeyboardButton.ascii_key('d')
keySpace = KeyboardButton.ascii_key(' ')
 
# World
world = BulletWorld()
world.setGravity(Vec3(0, 0, -GRAVITY))
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
yetiModel.setH(90)
yetiModel.setPos(0, 0, -1)
yetiModel.flattenLight()

# Type BulletRigidBodyNode
playerNode = BulletRigidBodyNode("Player")
playerNode.setMass(8.0)
playerNode.addShape(yetiShape)
playerNode.setAngularFactor(Vec3(0,0,0))
playerNode.setDeactivationEnabled(False) # Without this disabled, things will weld together after a certain amount of time. It's really annoying.

# Type NodePath
playerNP = worldNP.attachNewNode(playerNode)
yetiModel.reparentTo(playerNP)
playerNP.setPos(0, 0, 6)
playerNP.setH(0)
world.attachRigidBody(playerNP.node())

# Camera setup behind Yeti
base.cam.setPos(0, -40, 10)
base.cam.reparentTo(playerNP)

# Press F1 to enable debug mode.
def toggleDebug():
  if debugNP.isHidden():
    debugNP.show()
  else:
    debugNP.hide()

world.setDebugNode(debugNP.node())
debugNP.show()

def move():
	playerVelocity = playerNode.getLinearVelocity()
	isJumping = False
	playerRotation = playerNP.getH() 
	
	# TODO: Get rotation and move via camera angle
	# We will need to do more math with the movement.
	
	# Function for polling keys
	keyPressed = base.mouseWatcherNode.is_button_down
	
	# If we get a key hold, continuously apply force until we hit the max velocity
	if keyPressed(keyForward):
		debugP("forward")
		if(abs(playerVelocity.getY()) > MAX_VEL_XY):
			debugP("Y vel Capped")
			playerVelocity.setY(MAX_VEL_XY)
		else:
			playerNode.applyForce((-MOVE_SPEED * sin(playerRotation * DEG_TO_RAD), MOVE_SPEED * cos(playerRotation * DEG_TO_RAD), 0), PNT)
	elif keyPressed(keyBack):
		debugP("back")
		if(abs(playerVelocity.getY()) > MAX_VEL_XY):
			debugP("Y vel at max")
			playerVelocity.setY(-MAX_VEL_XY / 2)
		else:
			playerNode.applyForce((MOVE_SPEED * sin(playerRotation * DEG_TO_RAD) / 2, -MOVE_SPEED * cos(playerRotation * DEG_TO_RAD) / 2, 0), PNT)
	else:
		playerVelocity.setY(0) # Slow him down... somehow. This doesn't work yet.
	
	# Rotations
	if keyPressed(keyLeft):
		playerNP.setH(playerRotation + (globalClock.getDt() * TURN_SPEED))
	elif keyPressed(keyRight):
		playerNP.setH(playerRotation + (globalClock.getDt() * -TURN_SPEED))
	
	if keyPressed(keySpace):
		debugP("jump")
	
	# Set the camera accordingly
	#base.cam.setPos(playerNP.getX(), playerNP.getY() - 60, playerNP.getZ() + 10)
	base.cam.lookAt(playerNP)

# Function-based keybindings
o = DirectObject()
o.accept('f1', toggleDebug)

# Update
def update(task):
	dt = globalClock.getDt()
	world.doPhysics(dt)
	move()
	return task.cont
 
taskMgr.add(update, 'update')
run()