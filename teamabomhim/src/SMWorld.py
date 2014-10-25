from panda3d.core import BitMask32, Vec3, Vec4, PNMImage, Filename, GeoMipTerrain, TextureStage, VBase4
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletRigidBodyNode, BulletDebugNode, BulletCharacterControllerNode, BulletGhostNode
from panda3d.bullet import BulletBoxShape, BulletCapsuleShape, BulletCylinderShape, BulletPlaneShape, BulletHeightfieldShape
from panda3d.bullet import ZUp
from direct.showbase.DirectObject import DirectObject
from direct.showbase.Transitions import Transitions

from DebugNode import DebugNode
from SMPlayer import SMPlayer
from SMKeyHandler import SMKeyHandler
from SMCamera import SMCamera
from SMCollisionHandler import SMCollisionHandler
from SMLighting import SMLighting
from SMCollect import SMCollect
from SMBall import SMBall
from SMAI import SMAI

GRAVITY = 96

class SMWorld(DirectObject):

	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Constructor
	# (Game state, Map name, Height of death plane)
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def __init__(self, gameState, mapName, deathHeight, tObj):
	
		self.worldObj = self.setupWorld()
		self.debugNode = self.setupDebug()
		self.playerObj = SMPlayer(self.worldBullet, self.worldObj, self, -5, -8, 40)
		self.playerNP = self.playerObj.getNodePath()
		self.heightMap = self.setupHeightmap(mapName)
		self.deathZone = self.setupDeathzone(deathHeight)
		
		self.ballObj = SMBall(self.worldBullet, self.worldObj, self.playerNP)
		self.ballNP = self.ballObj.getNodePath()
		
		self.kh = SMKeyHandler()
		self.colObj = self.setupCollisionHandler()
		self.ligObj = SMLighting(Vec4(.4, .4, .4, 1), Vec3(-5, -5, -5), Vec4(2.0, 2.0, 2.0, 1.0))
		
		self.camObj = SMCamera(0, 0, 0, self.playerObj.getNodePath())
		self.camObj.setPos(0, -40, 10)
		self.camObj.reparentTo(self.playerNP)
		
		self.collectObj = SMCollect(self.worldBullet, self.worldObj, self.playerNP.getX(), self.playerNP.getY(), self.playerNP.getZ())
		self.collectNP = self.collectObj.getNodePath()
		
		self.SMAI = SMAI(self.worldBullet, self.worldObj, self.playerNP.getX(), self.playerNP.getY(), self.playerNP.getZ(), "../res/models/goat.egg", "Flee", self.playerNP)	
		print("AI Initialized")
		
		self.textObj = tObj
		self.textObj.addText("yetiPos", "Position: ")
		self.textObj.addText("yetiVel", "Velocity: ")
		self.textObj.addText("yetiFric", "Friction: ")
		self.textObj.addText("terrHeight", "T Height: ")
		
		self.accept('b', self.spawnBall)

                self.transition = Transitions(loader)

		self.accept('escape', base.userExit)
		self.accept('enter', self.pauseUnpause)
		
		self.pauseUnpause()
		
		print("World initialized.")


	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Toggles the pause screen
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	def spawnBall(self):
		pos = self.playerObj.getPosition()
		x = pos.getX()
		y = pos.getY()
		z = pos.getZ()
		self.ballObj.create(x,y,z)
	
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
		wNP = render.attachNewNode('WorldNode')
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
		debug = DebugNode()
		debugNP = debug.getDebugNode()
		self.worldBullet.setDebugNode(debugNP.node())
		debugNP.hide()
		return debugNP
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Initializes and returns a BulletRigidBodyNode of the terrain, which loads the map with the specified name.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def setupHeightmap(self, name):
		self.hmHeight = 80
		hmPath = "../maps/" + name + "-h.png"
		imPath = "../maps/" + name + "-i.png"
		smPath = "../maps/" + name + "-s.png"
		scmPath = "../maps/" + name + "-sc.png"
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
		self.hmTerrain.setBruteforce(True)
		self.hmTerrain.setMinLevel(3) # 3 seems to be a nice balance between quality and minimal clipping.
		self.hmTerrain.generate()
		
		# Let's improve performance, eh?
		self.hmTerrain.getRoot().flattenStrong()
		self.hmTerrain.getRoot().analyze()
		
		self.hmTerrainNP = self.hmTerrain.getRoot()
		self.hmTerrainNP.setSz(self.hmHeight)
		self.hmTerrainNP.setPos(-self.hmOffset, -self.hmOffset, -self.hmHeight / 2.0)
		self.hmTerrainNP.reparentTo(render)

		# Here begins the scenery mapping
		tree = loader.loadModel("../res/models/tree_1.egg")
		rock = loader.loadModel("../res/models/rock_1.egg")
		texpk = loader.loadTexture(scmPath).peek()
		for i in range(0, texpk.getXSize()):
			for j in range(0, texpk.getYSize()):
				color = VBase4(0, 0, 0, 0)
				texpk.lookup(color, float(i) / texpk.getXSize(), float(j) / texpk.getYSize())
				if(int(color.getX() * 255) == 255):
					newTree = render.attachNewNode("newTree")
					newTree.setPos(i - texpk.getXSize() / 2, j - texpk.getYSize() / 2, self.hmTerrain.get_elevation(i, j) * self.hmHeight - self.hmHeight / 2)
					# newTree.setScale can add some nice randomized scaling here.
					tree.instanceTo(newTree)
				if(int(color.getX() * 255) == 128):
					newRock = render.attachNewNode("newRock")
					newRock.setPos(i - texpk.getXSize() / 2, j - texpk.getYSize() / 2, self.hmTerrain.get_elevation(i, j) * self.hmHeight - self.hmHeight / 2)
					rock.instanceTo(newRock)

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
	# Returns the terrain height of coordinates x and y from the heightmap.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def getTerrainHeight(self, x, y):
		return self.hmTerrain.get_elevation(x + self.hmOffset, y + self.hmOffset) * self.hmHeight
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Handles player movement
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def playerMove(self):
	
		self.doPlayerTests()
		
		if self.kh.poll('a'):
			self.playerObj.turn(True)
		elif self.kh.poll('d'):
			self.playerObj.turn(False)
		
		if self.kh.poll('w'):
			self.playerObj.move(True)
		elif self.kh.poll('s'):
			self.playerObj.move(False)
		else:
			self.playerObj.stop()
		
		
		if self.kh.poll(' '):
			self.playerObj.jump()
		
		self.camObj.lookAt(self.playerObj.getNodePath())
		self.updateStats()
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Various tests concerning the player flags and collisions.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def doPlayerTests(self):
		
		# TODO: Add out-of-bounds tests here.
		
		if(self.colObj.didCollide(self.playerNP.node(), self.heightMap)):
			# print("col ground")
			self.playerObj.setAirborneFlag(False)
			self.playerObj.setFactor(1, 1, 1)
		
		if(self.colObj.didCollide(self.playerNP.node(), self.deathZone.node())):
			self.playerObj.respawn()
		
		if(not(self.playerObj.getAirborneFlag())):
			playerPos = self.playerObj.getPosition()
			px = playerPos.getX()
			py = playerPos.getY()
			th = self.getTerrainHeight(px, py)
			self.playerObj.snapToTerrain(th, self.hmHeight)
		
		if(self.colObj.didCollide(self.playerNP.node(), self.collectNP)):
			self.collectObj.destroy()

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
		fric = str(round(self.playerObj.getFriction(), 2))
		tHeight = str(round(self.getTerrainHeight(x, y), 1))
		self.textObj.editText("yetiPos", "Position: (" + sx + ", " + sy + ", " + sz + ")")
		self.textObj.editText("yetiVel", "Velocity: (" + vx + ", " + vy + ", " + vz + ")")
		self.textObj.editText("yetiFric", "Friction: " + fric)
		self.textObj.editText("terrHeight", "T Height: " + tHeight)

	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Update the world. Called every frame.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def update(self, task):
		dt = globalClock.getDt()
		self.worldBullet.doPhysics(dt)
		self.SMAI.AIUpdate()
		self.playerMove()
		return task.cont

