from direct.directbase import DirectStart
from panda3d.core import Vec3, Vec4, KeyboardButton
from pandac.PandaModules import ActorNode, ForceNode, BitMask32
from pandac.PandaModules import CardMaker
from pandac.PandaModules import PhysicsCollisionHandler, CollisionTraverser, CollisionSphere, CollisionNode, LinearVectorForce
from direct.actor.Actor import Actor
from math import sin, cos, pi
from direct.showbase.DirectObject import DirectObject

# Variables
isMoving = False
isJumping = False
forward_button = KeyboardButton.ascii_key('w')
back_button = KeyboardButton.ascii_key('s')
left_button = KeyboardButton.ascii_key('a')
right_button = KeyboardButton.ascii_key('d')
space_button = KeyboardButton.ascii_key(' ')
DEG_TO_RAD = pi/180
MOVE_SPEED = 15
TURN_SPEED = 180
JUMP_FORCE = 40

# Set the background color to black
base.win.setClearColor(Vec4(0,0,0,1))

# Load the model
yetiModel = loader.loadModel("models/yeti")
yetiModel.setH(-90)
yetiModel.reparentTo(render)

# Ignore collisions for the model itself
yetiModel.setCollideMask(BitMask32.allOff())

# Generate a flat surface we can land on
cm = CardMaker("ground")
cm.setFrame(-30, 30, -50, 50)
ground = render.attachNewNode(cm.generate())
ground.setPos(0, 0, 0)
ground.lookAt(0, 0, -1)
ground.reparentTo(render)

# Enable physics
base.enableParticles()

# Set up gravity
gravityFN = ForceNode('world-forces')
gravityFNP = render.attachNewNode(gravityFN)
gravityForce = LinearVectorForce(0, 0, -25) 
gravityFN.addForce(gravityForce)
base.physicsMgr.addLinearForce(gravityForce)
base.cTrav = CollisionTraverser()

# Uncomment if any entities are moving too fast
#base.cTrav.setRespectPrevTransform(True)
   
# The main actor handler
yetiActorNode = render.attachNewNode(ActorNode("actor"))
yetiActorNode.setZ(30)

# Player's collision handler. Type NodePath
yetiCollider = yetiActorNode.attachNewNode(CollisionNode("yetiCollisionNode"))
yetiCollider.node().addSolid(CollisionSphere(0, 0, 1.5, 3.7))  # x, y, z, radius

# Only handle collisions of the player onto the world, and not vice-versa
yetiCollider.node().setFromCollideMask(BitMask32.allOn())
yetiCollider.node().setIntoCollideMask(BitMask32.allOff())

# Uncomment to show the collision sphere
#yetiCollider.show()

# Create a collision handler to handle all the physics
collisionHandle = PhysicsCollisionHandler()
collisionHandle.addCollider(yetiCollider, yetiActorNode)

# Add the handler to the global traverser
base.cTrav.addCollider(yetiCollider, collisionHandle)
yetiModel.reparentTo(yetiActorNode)
base.physicsMgr.attachPhysicalNode(yetiActorNode.node())

# Set up the camera
base.disableMouse()
base.camera.setPos(0, -100, 10)
base.camera.lookAt(0, 0, 0)

def move(task):
	
	playerVelocity = Vec3(0, 0, 0)
	playerTurnVel = 0
	isJumping = False
	playerRotation = yetiActorNode.getH()
	
	is_down = base.mouseWatcherNode.is_button_down
	
	if is_down(forward_button): 
		playerVelocity += (MOVE_SPEED * sin(yetiActorNode.getH() * DEG_TO_RAD), -MOVE_SPEED * cos(yetiActorNode.getH() * DEG_TO_RAD), 0)
	if is_down(back_button):
		playerVelocity -= (MOVE_SPEED * sin(yetiActorNode.getH() * DEG_TO_RAD) / 2, -MOVE_SPEED * cos(yetiActorNode.getH() * DEG_TO_RAD) / 2, 0)
	if is_down(left_button):
		playerTurnVel += (TURN_SPEED)
	if is_down(right_button):
		playerTurnVel -= (TURN_SPEED)
	if is_down(space_button):
		print("jump")
	
	velocityDelta = playerVelocity * globalClock.get_dt()
	turnDelta = playerTurnVel * globalClock.get_dt()
	
	# Apply the force here:
	yetiActorNode.setPos(yetiActorNode.getPos() + velocityDelta)
	yetiActorNode.setH(yetiActorNode.getH() + turnDelta)
	
	return task.cont

taskMgr.add(move, "moveTask")
	
# run the simulation
run() 