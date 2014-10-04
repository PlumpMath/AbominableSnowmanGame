# Some of these probably aren't necessary, but we'll remove them when we need to
import direct.directbase.DirectStart
from panda3d.core import Vec3, BitMask32, Point3, KeyboardButton
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletRigidBodyNode, BulletDebugNode, BulletCharacterControllerNode
from panda3d.bullet import BulletBoxShape, BulletCapsuleShape, BulletCylinderShape, BulletPlaneShape
from panda3d.bullet import ZUp
from math import sin, cos, pi
from direct.showbase.DirectObject import DirectObject

# Constants
DEBUG = True  # Set to False to disable verbose console output.
TURN_SPEED = 180
DEG_TO_RAD = pi/180
MAX_VEL_XY = 50
MAX_VEL_Z = 5000
GRAVITY = 25
MOVE_SPEED = 500
PNT = Point3(0,0,0)  # applyForce requires a Point to be passed

# A print that will only print if DEBUG is True
def debugP(message):
	if(DEBUG):
		print(message)

# Keybindings
keyForward = KeyboardButton.ascii_key('w')
keyBack = KeyboardButton.ascii_key('s')
keyLeft = KeyboardButton.ascii_key('a')
keyRight = KeyboardButton.ascii_key('d')
keySpace = KeyboardButton.ascii_key(' ')
 
# Initialize the world and gravity
world = BulletWorld()
world.setGravity(Vec3(0, 0, -GRAVITY))
worldNP = render.attachNewNode('World')

# Shows collision boxes and other info.
debugNode = BulletDebugNode('Debug')
debugNode.showWireframe(True)
debugNode.showConstraints(True)
debugNode.showBoundingBoxes(True)
debugNode.showNormals(True)
debugNP = render.attachNewNode(debugNode)
 
# Plane (replace with a model or heightmap later)
shape = BulletPlaneShape(Vec3(0, 0, 1), 1)
planeNode = BulletRigidBodyNode('Ground')
planeNode.addShape(shape)
planeNP = render.attachNewNode(planeNode)
planeNP.setPos(0, 0, -2)
world.attachRigidBody(planeNode)
 
# Yeti
yetiHeight = 7
yetiRadius = 2
yetiShape = BulletCapsuleShape(yetiRadius, yetiHeight - 2 * yetiRadius, ZUp)
yetiModel = loader.loadModel("models/yeti")
yetiModel.setH(90)
yetiModel.setPos(0, 0, -1)
yetiModel.flattenLight()
playerNode = BulletRigidBodyNode("Player")
playerNode.setMass(8.0)
playerNode.addShape(yetiShape)

isJumping = True

# Without this set to 0,0,0, the Yeti would wobble like a Weeble and not fall down.
playerNode.setAngularFactor(Vec3(0,0,0))

# Without this disabled, things will weld together after a certain amount of time. It's really annoying.
playerNode.setDeactivationEnabled(False) 

playerNP = worldNP.attachNewNode(playerNode)
yetiModel.reparentTo(playerNP)
playerNP.setPos(0, 0, 6)
playerNP.setH(0)
world.attachRigidBody(playerNP.node())

# Place the camera behind the Yeti
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

# Calculates various forces every frame
def move():
	playerVelocity = playerNode.getLinearVelocity()
	global isJumping
	playerRotation = playerNP.getH() 
	
	# Only reset the jumping flag if the player has made contact with the ground
	contactResult = world.contactTestPair(playerNode, planeNode)
	contacts = contactResult.getContacts()
	for contact in contacts:
		c1 = contact.getNode0().getName()
		c2 = contact.getNode1().getName()
		if(c1 == playerNode.getName() and c2 == planeNode.getName()):
			isJumping = False
			playerNode.setLinearDamping(0.0)
			break
	
	
	# Function for polling keys
	keyPressed = base.mouseWatcherNode.is_button_down
	
	# If we get a key hold, continuously apply force until we hit the max velocity
	if keyPressed(keyForward):
		debugP("forward")
		
		# Cap velocity at the constant.
		if(abs(playerVelocity.getY()) > MAX_VEL_XY):
			debugP("Y vel Capped")
			playerVelocity.setY(MAX_VEL_XY)
		else:
			
			# Get the yeti to move in a relative forward based on its rotation
			playerNode.applyForce((-MOVE_SPEED * sin(playerRotation * DEG_TO_RAD), MOVE_SPEED * cos(playerRotation * DEG_TO_RAD), 0), PNT)
	
	# Same thing for backwards, but only at half speed
	elif keyPressed(keyBack):
		debugP("back")
		if(abs(playerVelocity.getY()) > MAX_VEL_XY):
			debugP("Y vel at max")
			playerVelocity.setY(-MAX_VEL_XY / 2)
		else:
			playerNode.applyForce((MOVE_SPEED * sin(playerRotation * DEG_TO_RAD) / 2, -MOVE_SPEED * cos(playerRotation * DEG_TO_RAD) / 2, 0), PNT)
	else:
		
		# When back or forward is released, dampen the momentum
		if not(isJumping):
			playerNode.setLinearDamping(0.9)
	
	# Rotate the player CCW or CW when A or D is held.
	if keyPressed(keyLeft):
		playerNP.setH(playerRotation + (globalClock.getDt() * TURN_SPEED))
	elif keyPressed(keyRight):
		playerNP.setH(playerRotation + (globalClock.getDt() * -TURN_SPEED))
	
	# Make the player jump
	if keyPressed(keySpace):
		debugP("jump")
		if(isJumping == False):
			isJumping = True
			playerNode.applyForce((0, 0, 14000), PNT)
	
	# Set the camera accordingly
	base.cam.lookAt(playerNP)

# Function-based keybindings
o = DirectObject()
o.accept('f1', toggleDebug)

# Update
def update(task):
	dt = globalClock.getDt()
	world.doPhysics(dt)  # Best name ever.
	move()
	
	# This is needed for it to call every frame
	return task.cont

taskMgr.add(update, 'update')
run()