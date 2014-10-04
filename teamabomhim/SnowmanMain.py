# Some of these probably aren't necessary, but we'll remove them when we need to
import direct.directbase.DirectStart
from panda3d.core import Vec3, VBase3, Vec4, BitMask32, Point3, KeyboardButton, Filename, PNMImage, GeoMipTerrain
from panda3d.core import LightRampAttrib, AmbientLight, DirectionalLight
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletRigidBodyNode, BulletDebugNode, BulletCharacterControllerNode
from panda3d.bullet import BulletBoxShape, BulletCapsuleShape, BulletCylinderShape, BulletPlaneShape, BulletHeightfieldShape
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
START_POS_X = -5
START_POS_Y = -8
START_POS_Z = 40
DEATH_HEIGHT = -20

# Damping values (less is more damping)
STOP_DAMPING = 0.80
JMP_STOP_DAMPING = 0.88
TURN_DAMPING = 0.92
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
 
# Heightmap Terrain
hmHeight = 40
hmImg = PNMImage(Filename("models/debugHeightMap.png")) # Currently 129x129. Must be (2^n) + 1 height and width.
hmShape = BulletHeightfieldShape(hmImg, hmHeight, ZUp)
hmNode = BulletRigidBodyNode('Terrain')
hmNode.addShape(hmShape)
hmNode.setMass(0)
hmNP = render.attachNewNode(hmNode)
world.attachRigidBody(hmNode)

hmOffset = hmImg.getXSize() / 2.0 - 0.5
hmTerrain = GeoMipTerrain('gmTerrain')
hmTerrain.setHeightfield(hmImg)
hmTerrain.generate()

hmTerrainNP = hmTerrain.getRoot()
hmTerrainNP.setSz(hmHeight)
hmTerrainNP.setPos(-hmOffset, -hmOffset, -hmHeight / 2.0)
hmTerrainNP.reparentTo(render)

# Death Zone plane
planeShape = BulletPlaneShape(Vec3(0, 0, 1), 1)
planeNode = BulletRigidBodyNode('DeathZone')
planeNode.addShape(planeShape)
planeNP = render.attachNewNode(planeNode)
planeNP.setPos(0, 0, DEATH_HEIGHT)
world.attachRigidBody(planeNode)
 
# Yeti
yetiHeight = 7
yetiRadius = 2
yetiShape = BulletCapsuleShape(yetiRadius, yetiHeight - 2 * yetiRadius, ZUp)
yetiModel = loader.loadModel("models/yeti")
yetiModel.setH(90)
yetiModel.setPos(0, 0, -1) # This is NOT the actual player position. Use playerNP instead.
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
playerNP.setPos(START_POS_X, START_POS_Y, START_POS_Z)
playerNP.setH(0)
world.attachRigidBody(playerNP.node())

# Place the camera behind the Yeti
base.cam.setPos(0, -40, 10)
base.cam.reparentTo(playerNP)

# Prettyful Lighting
render.setShaderAuto()
render.setAttrib(LightRampAttrib.makeHdr1())
ambientLight = AmbientLight("ambientLight")
ambientLight.setColor(Vec4(.4, .4, .4, 1))
directionalLight = DirectionalLight("directionalLight")
directionalLight.setDirection(Vec3(-5, -5, -5))
directionalLight.setColor(Vec4(2.0, 2.0, 2.0, 1.0))
directionalLight.setSpecularColor(Vec4(2.0, 2.0, 2.0, 1))
render.setLight(render.attachNewNode(ambientLight))
render.setLight(render.attachNewNode(directionalLight))

# Press F1 to enable debug mode. WARNING: This will SEVERELY lag your computer. I'm talking 0.5 FPS.
# Only enable this for debug purposes or if you have 4 GTX Titans in Quad SLI and an Extreme Edition CPU overclocked to 14GHz. AT LEAST.
def toggleDebug():
  if debugNP.isHidden():
    debugNP.show()
  else:
    debugNP.hide()

world.setDebugNode(debugNP.node())
debugNP.hide()

# Calculates various forces every frame
def move():
	playerVelocity = playerNode.getLinearVelocity()
	global isJumping
	playerRotation = playerNP.getH()
	cameraPitch = 10
	cameraTargetHeight = 6.0
	cameraDistance = 50
	
	# Contacts between the player and terrain
	contactTerrain = world.contactTestPair(playerNode, hmNode)
	contactsTer = contactTerrain.getContacts()
	
	# Contacts between the player and the death zone
	contactPlane = world.contactTestPair(playerNode, planeNode)
	contactsPla = contactPlane.getContacts()
	
	# If the player and terrain make contact, reset the jump flag.
	for contact in contactsTer:
		c1 = contact.getNode0().getName()
		c2 = contact.getNode1().getName()
		if(c1 == playerNode.getName() and c2 == hmNode.getName()):
			isJumping = False
			break
	
	# If the player and the death zone make contact, negate all forces and respawn the player.
	for contact in contactsPla:
		c1 = contact.getNode0().getName()
		c2 = contact.getNode1().getName()
		if(c1 == playerNode.getName() and c2 == planeNode.getName()):
			playerVelocity = Vec3(0,0,0)
			playerNP.setPos(START_POS_X, START_POS_Y, START_POS_Z)
			print("DEAD")
			break
	
	# Mouse camera control
	if base.mouseWatcherNode.hasMouse():
		md = base.win.getPointer(0)
		x = md.getX()
		y = md.getY()
		deltaX = md.getX() - 200
		deltaY = md.getY() - 200
		base.win.movePointer(0, 200, 200)
		playerNP.setH(playerNP.getH() - 0.3 * deltaX)
		cameraPitch = cameraPitch + 0.1 * deltaY
		if (cameraPitch < -60): cameraPitch = -60
		if (cameraPitch >  80): cameraPitch =  80
		base.camera.setHpr(0, cameraPitch, 0)
		base.camera.setPos(0, 0, cameraTargetHeight/2)
		base.camera.setY(base.camera, cameraDistance)
	
	# Function for polling keys
	keyPressed = base.mouseWatcherNode.is_button_down
	
	# If we get a key hold, continuously apply force until we hit the max velocity
	if keyPressed(keyForward):
		
		# Cap velocity at the constant.
		if(abs(playerVelocity.getY()) > MAX_VEL_XY):
			playerVelocity.setY(MAX_VEL_XY)
		elif(abs(playerVelocity.getX()) > MAX_VEL_XY):
			playerVelocity.setX(MAX_VEL_XY)
		else:
		
			# Get the yeti to move in a relative forward based on its rotation
			playerNode.applyForce((-MOVE_SPEED * sin(playerRotation * DEG_TO_RAD), MOVE_SPEED * cos(playerRotation * DEG_TO_RAD), 0), PNT)
		
	
	# Same thing for backwards, but only at half speed
	elif keyPressed(keyBack):
		if(abs(playerVelocity.getY()) > MAX_VEL_XY / 2):
			playerVelocity.setY(MAX_VEL_XY / 2)
		elif(abs(playerVelocity.getX()) > MAX_VEL_XY / 2):
			playerVelocity.setX(MAX_VEL_XY / 2)
		else:
			playerNode.applyForce((MOVE_SPEED * sin(playerRotation * DEG_TO_RAD) / 2, -MOVE_SPEED * cos(playerRotation * DEG_TO_RAD) / 2, 0), PNT)
			
	else:
		
		if(isJumping):
			# If the player is in the middle of a jump and releases the jump key, reduce the velocity
			playerNode.setLinearVelocity(Vec3(playerVelocity.getX() * JMP_STOP_DAMPING, playerVelocity.getY() * JMP_STOP_DAMPING, playerVelocity.getZ()))
			
		else:
			# When back or forward is released, stop movement.
			playerNode.setLinearVelocity(Vec3(playerVelocity.getX() * STOP_DAMPING, playerVelocity.getY() * STOP_DAMPING, playerVelocity.getZ()))
	
	# Rotate the player CCW or CW when A or D is held.
	if keyPressed(keyLeft):
		playerNP.setH(playerRotation + (globalClock.getDt() * TURN_SPEED))
		playerNode.setLinearVelocity(Vec3(playerVelocity.getX() * TURN_DAMPING, playerVelocity.getY() * TURN_DAMPING, playerVelocity.getZ()))
	elif keyPressed(keyRight):
		playerNP.setH(playerRotation + (globalClock.getDt() * -TURN_SPEED))
		playerNode.setLinearVelocity(Vec3(playerVelocity.getX() * TURN_DAMPING, playerVelocity.getY() * TURN_DAMPING, playerVelocity.getZ()))
	
	# Prevent super-bounces with steep slopes
	if playerVelocity.getZ() > 5:
		isJumping = True
	
	# Make the player jump
	if keyPressed(keySpace):
		if(isJumping == False):
			isJumping = True
			playerNode.applyForce((0, 0, 14000), PNT)
	
	# Set the camera accordingly
	base.cam.lookAt(playerNP)

# Function-based keybindings
o = DirectObject()
o.accept('f1', toggleDebug)
o.accept('escape', base.userExit)

# Update
def update(task):
	dt = globalClock.getDt()
	world.doPhysics(dt)  # Best name ever.
	move()
	
	# This is needed for it to call every frame
	return task.cont

taskMgr.add(update, 'update')
run()