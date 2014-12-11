from panda3d.core import BitMask32, Point2, Point3, Vec3, Vec4, PNMImage, Filename, GeoMipTerrain, TextureStage, VBase4, NodePath, TextNode
from panda3d.core import WindowProperties
from panda3d.physics import BaseParticleEmitter,BaseParticleRenderer
from panda3d.physics import PointParticleFactory,SpriteParticleRenderer
from panda3d.physics import LinearNoiseForce,DiscEmitter
from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletRigidBodyNode, BulletDebugNode, BulletCharacterControllerNode, BulletGhostNode
from panda3d.bullet import BulletBoxShape, BulletCapsuleShape, BulletCylinderShape, BulletPlaneShape, BulletHeightfieldShape
from panda3d.bullet import ZUp
from random import randint

from direct.gui.OnscreenText import OnscreenText

from direct.showbase.DirectObject import DirectObject
from direct.showbase.Transitions import Transitions

from DebugNode import DebugNode
from SMPlayer import SMPlayer
from SMKeyHandler import SMKeyHandler
from SMCameraDev import SMCamera
from SMCollisionHandler import SMCollisionHandler
from SMLighting import SMLighting
from SMCollect import SMCollect
from SMBall import SMBall
from SMAI import SMAI
from SMGUI import SMGUI
from SMGUICounter import SMGUICounter
from SMGUIMeter import SMGUIMeter
from SMColide import SMColide

# Global gravity constant (9.81 is for scrubs)
GRAVITY = 226
TERRAIN_SNOW = 0
TERRAIN_ICE = 1
TERRAIN_STONE = 2

class SMWorld(DirectObject):

	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Constructor
	# (Game state, Map name, Height of death plane)
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def __init__(self, mapID, tObj, aObj):

		self.mapID = mapID
		
		# EX: maps/map-1/map-1.yetimap
		metaFile = open("../maps/map" + str(self.mapID) + "/map" + str(self.mapID) + ".yetimap", 'r')
		metaLines = metaFile.readlines()
		lineCount = len(metaLines)
		self.snowflakeCount = lineCount - 2
		self.snowCount = 0
		
		# First Line: Player's starting position
		# EX: 50,50,50 (NO SPACES)
		playerLine = metaLines[0]
		playerPosList = playerLine.split(",")
		playerInitX = int(playerPosList[0])
		playerInitY = int(playerPosList[1])
		playerInitZ = int(playerPosList[2])
		self.playerStart = Point3(playerInitX, playerInitY, playerInitZ)
		
		# 2nd Line: Deathzone Height
		# ONE INTEGER
		deathHeight = int(metaLines[1])
		
		# Get dem snowflakes
		self.snowflakePositions = []
		print("Snowflake Count: " + str(self.snowflakeCount))
		for i in xrange(0, self.snowflakeCount):
			sfline = metaLines[i+2]
			sfList = sfline.split(",")
			sfx = int(sfList[0])
			sfy = int(sfList[1])
			sfz = int(sfList[2])
			self.snowflakePositions.append(Point3(sfx, sfy, sfz))
			print("New snowflake to add: (" + str(sfx) + "," + str(sfy) + "," + str(sfz) + ")")
		
		
		
		#load in controls
		ctrlFl = open("ctrConfig.txt")
		#will skip n lines where [n,]
		#makes a list of controls
		self.keymap = eval(ctrlFl.read())
		#close file
		ctrlFl.close()
		
		# Create new instances of our various objects
		self.mapName = str(mapID)
		self.audioMgr = aObj
		self.worldObj = self.setupWorld()
		self.heightMap = self.setupHeightmap(self.mapName)
		self.deathZone = self.setupDeathzone(deathHeight)
		self.debugNode = self.setupDebug()	
		
		# Player Init
		self.playerObj = SMPlayer(self.worldBullet, self.worldObj, self, self.playerStart, self.audioMgr)
		self.playerNP = self.playerObj.getNodePath()
		self.playerNP.setH(180);
		self.canUseShift = True
		self.canAirDash = True
		
		# Snowball Init
		self.ballObj = SMBall(self.worldBullet, self.worldObj, self.playerObj, self.playerNP)
		self.sbCollideFlag = False
		self.ballNP = self.ballObj.getNodePath()
		
		# Key Handler
		self.kh = SMKeyHandler()
		self.lastMousePos = self.kh.getMouse()
		
		# Collision Handler
		self.colObj = self.setupCollisionHandler()
		
		# Lighting
		self.ligObj = SMLighting(Vec4(.4, .4, .4, 1), Vec3(-5, -5, -5), Vec4(2.0, 2.0, 2.0, 1.0))
		
		# Camera
		self.camObj = SMCamera(self.playerObj, self.worldBullet, self.worldObj)
		self.cameraControl = False

		# GUI
		self.GUI = SMGUI()
		self.snowflakeCounter = SMGUICounter("snowflake", self.snowflakeCount) # Replace 3 with # of snowflakes in level.
		self.snowMeter = SMGUIMeter(100)
		self.GUI.addElement("snowflake", self.snowflakeCounter)
		self.GUI.addElement("snowMeter", self.snowMeter)
		
		#Snowy Outside
		# base.enableParticles()
		# self.p = ParticleEffect()
		# self.p.cleanup()
		# self.p = ParticleEffect()
		# self.p.loadConfig('snow.ptf')        
		# self.p.start(self.camObj.getNodePath())
		# self.p.setPos(0.00, 0.500, 0.000)

		# AI
		# self.goat1 = SMAI("../res/models/goat.egg", 75.0, self.worldBullet, self.worldObj, -70, -95, 5)
		# self.goat1.setBehavior("flee", self.playerNP)
		# self.goat2 = SMAI("../res/models/goat.egg", 75.0, self.worldBullet, self.worldObj, -80, -83, 5)
		# self.goat2.setBehavior("flee", self.playerNP)
		# print("AI Initialized")
		
		# Debug Text
		self.textObj = tObj
		self.textObj.addText("yetiPos", "Position: ")
		self.textObj.addText("yetiVel", "Velocity: ")
		self.textObj.addText("yetiFric", "Friction: ")
		self.textObj.addText("onIce", "Ice(%): ")
		self.textObj.addText("onSnow", "Snow(%): ")
		self.textObj.addText("terrHeight", "T Height: ")
		self.textObj.addText("terrSteepness", "Steepness: ")
		
		# Pause screen transition
		self.transition = Transitions(loader)

		# Method-based keybindings
		# self.accept('b', self.spawnBall)
		self.accept('escape', base.userExit)
		self.accept('enter', self.pauseUnpause)
		self.accept('f1', self.toggleDebug)
		
		self.accept('lshift-up', self.enableShiftActions)
		self.accept('mouse1', self.enableCameraControl)
		self.accept('mouse1-up', self.disableCameraControl)
		self.accept('wheel_up', self.camObj.zoomIn)
		self.accept('wheel_down', self.camObj.zoomOut)
		
		self.pauseUnpause()
		
		# Disable the mouse
		base.disableMouse()
		props = WindowProperties()
		props.setCursorHidden(True)
		base.win.requestProperties(props)
		
		# Uncomment this to see everything being rendered.
		self.printSceneGraph()
		
		# Play the BGM
		self.audioMgr.playBGM("snowmanWind")
		
		# Skybox formed
		skybox = loader.loadModel("../res/models/skybox.egg")
		# skybox.set_two_sided(true)
		skybox.setScale(200)
		skybox.setPos(0, 0, -450)
		skybox.reparentTo(render)
		
		
		#ADDED THIS STUFF BECAUSE OBJECTMAP IS TOO INACCURATE TOO PLACE ITEMS PROPERLY
		self.caveNew = loader.loadModel("../res/models/cave_new.egg")
		self.caveNew.reparentTo(render)
		self.caveNew.setScale(11)
		self.caveNew.setPos(-50, 95, -13)
		self.caveNew.setH(0)
		
		self.planeFront = loader.loadModel("../res/models/plane_front")
		self.planeFront.reparentTo(render)
		self.planeFront.setScale(8)
		self.planeFront.setPos(190,-100,-15)
		self.planeFront.setH(190)
		self.planeFront.setR(30)
		
		mountain = loader.loadModel("../res/models/mountain.egg")
		mountain.reparentTo(render)
		mountain.setPos(650,800,20)
		mountain.setScale(120)

		self.planeTail = SMColide("../res/models/plane_tail.egg", self.worldBullet, self.worldObj, -40, -130, -7, 20, 20, 15, 10)
		self.planeTail.AIModel.setH(230)		
		
		self.ropeBridge = SMColide("../res/models/rope_bridge.egg", self.worldBullet, self.worldObj, 180, 115, 30, 45, 45, 3, 6)
		self.ropeBridge.AIModel.setH(50)
		
		print("World initialized.")


	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Enables the camera to be rotated by moving the mouse horizontally.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def enableCameraControl(self):
		self.cameraControl = True
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Disables the camera control.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def disableCameraControl(self):
		self.cameraControl = False
		
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Enables the use of shift actions again.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def enableShiftActions(self):
		self.canUseShift = True
		
	def disableShiftActions(self):
		self.canUseShift = False
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Respawns the yeti's snowball.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
		
	def spawnBall(self):
		if(not(self.playerObj.getAirborneFlag())):
			self.ballObj.respawn()
		
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Toggles the pause screen
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def pauseUnpause(self):
		if taskMgr.hasTaskNamed('UpdateTask'):
			taskMgr.remove('UpdateTask')
			self.transition.fadeScreen(0.5)
		else:
			taskMgr.add(self.update, 'UpdateTask')
			self.transition.noFade()
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Sets up the world and returns a NodePath of the BulletWorld
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def setupWorld(self):
		self.worldBullet = BulletWorld()
		self.worldBullet.setGravity(Vec3(0, 0, -GRAVITY))
		self.terrSteepness = -1
		wNP = render.attachNewNode('WorldNode')
		
		self.audioMgr.loadSFX("snowCrunch01")
		self.audioMgr.loadBGM("snowmanWind")
		
		return wNP
		
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Prints all nodes that are a child of render.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def printSceneGraph(self):
		print(render.ls())
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Initializes and returns a DebugNode NodePath.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def setupDebug(self):
		debug = BulletDebugNode()
		debug.showWireframe(False) # Yeah, don't set this to true unless you want to emulate an 80's computer running Crysis on Ultra settings.
		debug.showConstraints(True)
		debug.showBoundingBoxes(True) # This is the main use I have for it.
		debug.showNormals(True)
		debugNP = render.attachNewNode(debug)
		self.worldBullet.setDebugNode(debugNP.node())
		debugNP.hide()
		return debugNP
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Initializes and returns a BulletRigidBodyNode of the terrain, which loads the map with the specified name.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def setupHeightmap(self, name):
		
		# Automatically generate a heightmap mesh from a monochrome image.
		self.hmHeight = 120
		hmPath = "../maps/map" + name + "/map" + name + "-h.png"
		imPath = "../maps/map" + name + "/map" + name + "-i.png"
		smPath = "../maps/map" + name + "/map" + name + "-s.png"
		scmPath = "../maps/map" + name + "/map" + name + "-sc.png"
		print(hmPath)
		print(imPath)
		print(smPath)
		print(scmPath)
		hmImg = PNMImage(Filename(hmPath))
		hmShape = BulletHeightfieldShape(hmImg, self.hmHeight, ZUp)
		hmNode = BulletRigidBodyNode('Terrain')
		hmNode.addShape(hmShape)
		hmNode.setMass(0)
		self.hmNP = render.attachNewNode(hmNode)
		self.worldBullet.attachRigidBody(hmNode)
		self.hmOffset = hmImg.getXSize() / 2.0 - 0.5
		self.hmTerrain = GeoMipTerrain('gmTerrain')
		self.hmTerrain.setHeightfield(hmImg)
		
		# Optimizations and fixes
		self.hmTerrain.setBruteforce(True) # I don't think this is actually needed. 
		self.hmTerrain.setMinLevel(3) # THIS is what triangulates the terrain.
		self.hmTerrain.setBlockSize(128)  # This does a pretty good job of raising FPS.
		# Level-of-detail (not yet working)
		# self.hmTerrain.setNear(40)
		# self.hmTerrain.setFar(200)
		
		self.hmTerrain.generate()
		
		self.hmTerrainNP = self.hmTerrain.getRoot()
		self.hmTerrainNP.setSz(self.hmHeight)
		self.hmTerrainNP.setPos(-self.hmOffset, -self.hmOffset, -self.hmHeight / 2.0)
		self.hmTerrainNP.flattenStrong() # This only reduces the number of nodes; nothing to do with polys.
		self.hmTerrainNP.analyze()

		# Here begins the scenery mapping
		treeModel = loader.loadModel("../res/models/tree_1.egg")
		rockModel = loader.loadModel("../res/models/rock_1.egg")
		rock2Model = loader.loadModel("../res/models/rock_2.egg")
		rock3Model = loader.loadModel("../res/models/rock_3.egg")
		caveModel = loader.loadModel("../res/models/cave_new.egg")
		planeFrontModel = loader.loadModel("../res/models/plane_front.egg")
		planeWingModel = loader.loadModel("../res/models/plane_wing.egg")
		texpk = loader.loadTexture(scmPath).peek()
		
		# GameObject nodepath for flattening
		self.objNP = render.attachNewNode("gameObjects")
		self.treeNP = self.objNP.attachNewNode("goTrees")
		self.rockNP = self.objNP.attachNewNode("goRocks")
		self.rock2NP = self.objNP.attachNewNode("goRocks2")
		self.rock3NP = self.objNP.attachNewNode("goRocks3")
		self.caveNP = self.objNP.attachNewNode("goCave")
		self.planeFrontNP = self.objNP.attachNewNode("goPlaneFront")
		self.planeWingNP = self.objNP.attachNewNode("goPlaneWing")
		
		for i in range(0, texpk.getXSize()):
			for j in range(0, texpk.getYSize()):
				color = VBase4(0, 0, 0, 0)
				texpk.lookup(color, float(i) / texpk.getXSize(), float(j) / texpk.getYSize())
				if(int(color.getX() * 255.0) == 255.0):
					newTree = self.treeNP.attachNewNode("treeNode")
					treeModel.instanceTo(newTree)
					newTree.setPos(i - texpk.getXSize() / 2, j - texpk.getYSize() / 2, self.hmTerrain.get_elevation(i, j) * self.hmHeight - self.hmHeight / 2)
					# newTree.setScale(randint(0,4))
					newTree.setScale(2)
					
				if(int(color.getX() * 255.0) == 128):
					newRock = self.rockNP.attachNewNode("newRock")
					newRock.setPos(i - texpk.getXSize() / 2, j - texpk.getYSize() / 2, self.hmTerrain.get_elevation(i, j) * self.hmHeight - self.hmHeight / 2)
					rockModel.instanceTo(newRock)
					
				if(int(color.getX() * 255.0) == 77):
					newRock2 = self.rock2NP.attachNewNode("newRock2")
					newRock2.setPos(i - texpk.getXSize() / 2, j - texpk.getYSize() / 2, self.hmTerrain.get_elevation(i, j) * self.hmHeight - self.hmHeight / 2)
					rock2Model.instanceTo(newRock2)
					
				if(int(color.getX() * 255.0) == 102):
					newRock3 = self.rock3NP.attachNewNode("newRock3")
					newRock3.setPos(i - texpk.getXSize() / 2, j - texpk.getYSize() / 2, self.hmTerrain.get_elevation(i, j) * self.hmHeight - self.hmHeight / 2)
					rock3Model.instanceTo(newRock3)
					
				if(int(color.getX() * 255.0) == 64):
					newCave = self.caveNP.attachNewNode("newCave")
					newCave.setPos(i - texpk.getXSize() / 2, j - texpk.getYSize() / 2, self.hmTerrain.get_elevation(i, j) * self.hmHeight - self.hmHeight / 2)
					newCave.setScale(5)
					newCave.setP(180)
					caveModel.instanceTo(newCave)
				
				if(int(color.getX() * 255.0) == 191):
					newPlaneFront = self.planeFrontNP.attachNewNode("newPlaneFront")
					newPlaneFront.setPos(i - texpk.getXSize() / 2, j - texpk.getYSize() / 2, self.hmTerrain.get_elevation(i, j) * self.hmHeight - self.hmHeight / 2)
					newPlaneFront.setScale(6)
					planeFrontModel.instanceTo(newPlaneFront)
					
				if(int(color.getX() * 255.0) == 179):
					newPlaneWing = self.planeWingNP.attachNewNode("newPlaneWing")
					newPlaneWing.setPos(i - texpk.getXSize() / 2, j - texpk.getYSize() / 2, self.hmTerrain.get_elevation(i, j) * self.hmHeight - self.hmHeight / 2)
					newPlaneWing.setScale(6)
					newPlaneWing.setH(250)
					newPlaneWing.setR(180)
					newPlaneWing.setP(135)
					planeWingModel.instanceTo(newPlaneWing)

		self.snowflakes = []
		
		for i in xrange(0, self.snowflakeCount):
			print("Call " + str(i))
			sf = SMCollect(self.worldBullet, self.worldObj, self.snowflakePositions[i])
			self.snowflakes.append(sf)
					
		# render.flattenStrong()
		self.hmTerrainNP.reparentTo(render)
		
		# Here begins the attribute mapping
		ts = TextureStage("stage-alpha")
		ts.setSort(0)
		ts.setPriority(1)
		ts.setMode(TextureStage.MReplace)
		ts.setSavedResult(True)
		self.hmTerrainNP.setTexture(ts, loader.loadTexture(imPath, smPath))

		ts = TextureStage("stage-stone")
		ts.setSort(1)
		ts.setPriority(1)
		ts.setMode(TextureStage.MReplace)
		self.hmTerrainNP.setTexture(ts, loader.loadTexture("../res/textures/stone_tex.png"))
		self.hmTerrainNP.setTexScale(ts, 32, 32)

		ts = TextureStage("stage-ice")
		ts.setSort(2)
		ts.setPriority(1)
		ts.setCombineRgb(TextureStage.CMInterpolate, TextureStage.CSTexture, TextureStage.COSrcColor,
						 TextureStage.CSPrevious, TextureStage.COSrcColor,
						 TextureStage.CSLastSavedResult, TextureStage.COSrcColor)
		self.hmTerrainNP.setTexture(ts, loader.loadTexture("../res/textures/ice_tex.png"))
		self.hmTerrainNP.setTexScale(ts, 32, 32)

		ts = TextureStage("stage-snow")
		ts.setSort(3)
		ts.setPriority(0)
		ts.setCombineRgb(TextureStage.CMInterpolate, TextureStage.CSTexture, TextureStage.COSrcColor,
						 TextureStage.CSPrevious, TextureStage.COSrcColor,
						 TextureStage.CSLastSavedResult, TextureStage.COSrcAlpha)
		self.hmTerrainNP.setTexture(ts, loader.loadTexture("../res/textures/snow_tex_1.png"))
		self.hmTerrainNP.setTexScale(ts, 32, 32)

		# print(self.snowflakes)
		
		return hmNode
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Sets up and returns the death zone plane (returns its NodePath) with the specified height.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def setupDeathzone(self, height):
		planeShape = BulletPlaneShape(Vec3(0, 0, 1), 1)
		planeNode = BulletRigidBodyNode('DeathZone')
		planeNode.addShape(planeShape)
		planeNP = render.attachNewNode(planeNode)
		planeNP.setPos(0, 0, height)
		self.worldBullet.attachRigidBody(planeNode)
		return planeNP
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Sets up and returns the collision handler.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def setupCollisionHandler(self):
		colHand = SMCollisionHandler(self.worldBullet)
		return colHand
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Toggles showing bounding boxes.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def toggleDebug(self):
		if self.debugNode.isHidden():
			self.debugNode.show()
		else:
			self.debugNode.hide()
	
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Returns the terrain height of coordinates x and y from the heightmap.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def getTerrainHeight(self, x, y):
		return self.hmTerrain.get_elevation(x + self.hmOffset, y + self.hmOffset) * self.hmHeight
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Handles player movement
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def playerMove(self):
	
		# Go through the collision and flag tests, and update them
		self.doPlayerTests()
		
		# Rotation and camera movement
		if self.kh.poll(self.keymap['Left']):
			self.playerObj.turn(True)
		elif self.kh.poll(self.keymap['Right']):
			self.playerObj.turn(False)
		elif(self.cameraControl):
			newMousePos = self.kh.getMouse()
			mx = newMousePos.getX()
			self.camObj.rotateCamera(mx)
		
		self.camObj.calculatePosition()
		
		# Movement
		if self.kh.poll(self.keymap['Forward']):
			self.playerObj.move(True)
			self.camObj.rotateTowards(90)
		elif self.kh.poll(self.keymap['Back']):

			self.playerObj.move(False)
		else:
			self.playerObj.stop()

		# Jump
		if(self.kh.poll(self.keymap['Space']) and self.terrSteepness < 0.25): #and not(self.ballObj.isRolling())):
			self.playerObj.jump()
		else:
			self.playerObj.resetJump()
		
		# Air Dash
		if(self.kh.poll(self.keymap['airDash'])): #and self.playerObj.getAirborneFlag() == True and self.canAirDash == True):
			self.canAirDash = False
			self.playerObj.airDash()
		
		# Shift-based actions
		if(self.kh.poll("lshift") and not(self.sbCollideFlag) and not(self.playerObj.getAirborneFlag()) and self.canUseShift):
		
			# If there's another snowball already placed
			if(self.ballObj.exists() and not(self.ballObj.isRolling())):
				self.ballObj.respawn()
				
			# If we're rolling a snowball
			elif(self.ballObj.isRolling()):
			
				# Absorb snowball
				if(self.kh.poll("v")):
					self.canUseShift = False
					snowAmt = self.ballObj.getSnowAmount()
					self.playerObj.addSnow(snowAmt)
					# self.snowMeter.fillBy(snowAmt)
					self.ballObj.destroy()
					
				# Go to iceball throwing mode
				elif(self.kh.poll("b")):
					print("TODO: Ice ball throwing mode.")
					
				# Grow the snowball
				elif(self.kh.poll("w")):
					self.ballObj.grow()
					
			# Spawn a new snowball
			elif(self.ballObj.exists() == False):
				self.ballObj.respawn()
				
		# If the player is not pressing shift
		else:
			if(self.ballObj.isRolling()):
				self.ballObj.dropBall()

		base.win.movePointer(0, 400, 300)
		
		# So updating the stats is VERY expensive.
		if (self.debugNode.isHidden() == False):
			self.updateStats()
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Various tests concerning the player flags and collisions.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def doPlayerTests(self):
		
		# self.completeLevel()
		
		# Player's position
		plPos = self.playerObj.getPosition()
		px = plPos.getX()
		py = plPos.getY()
		pz = plPos.getZ()
		
		# Raycast directly down for terrain steepness
		rayYetiA = Point3(px, py, pz)
		rayYetiB = Point3(px, py, pz - 300)
		self.downRayTest = self.worldBullet.rayTestClosest(rayYetiA, rayYetiB).getHitNormal()
		rx = self.downRayTest.getX()
		ry = self.downRayTest.getY()
		rz = self.downRayTest.getZ()
		self.terrSteepness = 1.0 - rz

		# Redo collision flags later
		tempFlag = False
		
		# Snow/Ice height adjust
		self.playerObj.updateTerrain()
		
		# Collision: Player x Terrain
		if(self.colObj.didCollide(self.playerNP.node(), self.heightMap)):
			if(self.playerObj.getAirborneFlag()):
				self.audioMgr.playSFX("snowCrunch01")
			self.playerObj.setAirborneFlag(False)
			self.canAirDash = True
			self.playerObj.setFactor(1, 1, 1)
		
		# Collision: Player x Snowball
		if(self.ballObj.exists() and self.colObj.didCollide(self.playerNP.node(), self.ballObj.getRigidbody())):
			self.sbCollideFlag = True
			self.playerObj.setAirborneFlag(False)
			self.playerObj.setFactor(1, 1, 1)
		else:
			self.sbCollideFlag = False
		
		# Collision: Player x Death Zone
		if(self.colObj.didCollide(self.playerNP.node(), self.deathZone.node())):
			print("Player confirmed #REKT")
			self.playerObj.respawn()
		
		# Out of bounds checking
		if(abs(px) > 254 or abs(py) > 254):
			print("Player out of bounds!")
			self.playerObj.respawn()
		
		# Snap to terrain if... something. I need to restructure this. Don't read it.
		if(not(self.playerObj.getAirborneFlag()) and not(self.sbCollideFlag)):
			th = self.getTerrainHeight(px, py)
			self.playerObj.snapToTerrain(th, self.hmHeight)
		
		# Collision: Player x Snowflakes
		for i in xrange(0, self.snowflakeCount):
			if(self.snowflakes[i].exists() and self.colObj.didCollide(self.playerNP.node(), self.snowflakes[i].getNode())):
				self.snowflakes[i].destroy()
				self.snowflakeCounter.increment()
				self.snowCount += 1
			
		self.snowMeter.updateSnow(self.playerObj)
		
		#Load a new map when all collectables are collected
		if(self.snowCount >= self.snowflakeCount):
			
			self.snowCount = 0
			self.snowflakeCount = 0
			self.snowflakeCounter.setValue(0)
			self.snowflakeCounter.setState(2)
			
			#Loading Screen
			loadingText=OnscreenText("Loading...",1,fg=(1,1,1,1),pos=(0,0),align=TextNode.ACenter,scale=.07,mayChange=1)
			base.graphicsEngine.renderFrame() 
			base.graphicsEngine.renderFrame() 
			base.graphicsEngine.renderFrame() 
			base.graphicsEngine.renderFrame()
			
			#destroy objects
			self.worldBullet.removeRigidBody(self.heightMap)
			self.hmTerrainNP.removeNode()
			self.objNP.removeNode()
			self.treeNP.removeNode()
			self.rockNP.removeNode()
			self.rock2NP.removeNode()
			self.rock3NP.removeNode()
			self.caveNP.removeNode()
			self.planeFrontNP.removeNode()
			self.planeWingNP.removeNode()
			self.hmNP.removeNode()
			self.ropeBridge.AIChar.setPos(-200,-300,-200)
			self.ropeBridge.AIChar.removeNode()
			self.planeFront.removeNode()
			self.planeTail.AIChar.setPos(-200,-200,-200)
			self.planeTail.AIChar.removeNode()
			self.caveNew.removeNode()
			
			self.mapID += 1
			print self.mapID
			# EX: maps/map-1/map-1.yetimap
			metaFile = open("../maps/map" + str(self.mapID) + "/map" + str(self.mapID) + ".yetimap", 'r')
			metaLines = metaFile.readlines()
			lineCount = len(metaLines)
			self.snowflakeCount = lineCount - 2
		
			# First Line: Player's starting position
			# EX: 50,50,50 (NO SPACES)
			playerLine = metaLines[0]
			playerPosList = playerLine.split(",")
			playerInitX = int(playerPosList[0])
			playerInitY = int(playerPosList[1])
			playerInitZ = int(playerPosList[2])
			self.playerObj.playerNP.setPos(playerInitX, playerInitY, playerInitZ)
			self.playerObj.startX = playerInitX
			self.playerObj.startY = playerInitY
			self.playerObj.startZ = playerInitZ
		
			# 2nd Line: Deathzone Height
			# ONE INTEGER
			deathHeight = int(metaLines[1])
		
			
			self.snowflakePositions = []
			print("Snowflake Count: " + str(self.snowflakeCount))
			for i in xrange(0, self.snowflakeCount):
				sfline = metaLines[i+2]
				sfList = sfline.split(",")
				sfx = int(sfList[0])
				sfy = int(sfList[1])
				sfz = int(sfList[2])
				self.snowflakePositions.append(Point3(sfx, sfy, sfz))
				print("New snowflake to add: (" + str(sfx) + "," + str(sfy) + "," + str(sfz) + ")")
			self.snowflakeCounter.setMaxValue(self.snowflakeCount)
			
			#load new map
			self.mapName = str(self.mapID)
			self.heightMap = self.setupHeightmap(self.mapName)
			self.deathZone = self.setupDeathzone(deathHeight)
				
			
			loadingText.cleanup() 
			
		
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Update the debug text.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def updateStats(self):
		pos = self.playerObj.getPosition()
		x = pos.getX()
		y = pos.getY()
		z = pos.getZ()
		vel = self.playerObj.getVelocity()
		vx = str(round(vel.getX(), 1))
		vy = str(round(vel.getY(), 1))
		vz = str(round(vel.getZ(), 1))
		sx = str(round(x, 1))
		sy = str(round(y, 1))
		sz = str(round(z, 1))
		rx = str(round(self.downRayTest.getX(), 2))
		ry = str(round(self.downRayTest.getY(), 2))
		rz = str(round(self.terrSteepness, 2))
		fric = str(round(self.playerObj.getFriction(), 2))
		ip = str(round(self.playerObj.getIceCoefficient(), 2))
		sp = str(round(self.playerObj.getSnowCoefficient(), 2))
		tHeight = str(round(self.getTerrainHeight(x, y), 1))
		self.textObj.editText("yetiPos", "Position: (" + sx + ", " + sy + ", " + sz + ")")
		self.textObj.editText("yetiVel", "Velocity: (" + vx + ", " + vy + ", " + vz + ")")
		self.textObj.editText("yetiFric", "Friction: " + fric)
		self.textObj.editText("onIce", "Ice(%): " + ip)
		self.textObj.editText("onSnow", "Snow(%): " + sp)
		self.textObj.editText("terrHeight", "T Height: " + tHeight)
		self.textObj.editText("terrSteepness", "Steepness: " + rz)

	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# throw Snowball
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	def throw(self):
		self.throwing = True
		size = self.ballObj.getSize()
		#zoom camera and grab pos you wish to throw
		self.camObj.aimMode()
		taskMgr.add(self.controlCamera, "camera-task")
		rotation = self.camObj.getH()
		pitch =self.camObj.getP()
		self.ballObj.throwBall(size, pitch, rotation)
		#fix camera
		#self.throwing = False
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Update the world. Called every frame.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def update(self, task):
		dt = globalClock.getDt()
		self.worldBullet.doPhysics(dt)
		# self.goat1.AIUpdate()
		# self.goat2.AIUpdate()
		self.playerMove()
		return task.cont
