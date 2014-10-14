from panda3d.core import BitMask32, Vec3, Vec4, PNMImage, Filename, GeoMipTerrain, TextureStage, VBase4
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletRigidBodyNode, BulletDebugNode, BulletCharacterControllerNode, BulletGhostNode
from panda3d.bullet import BulletBoxShape, BulletCapsuleShape, BulletCylinderShape, BulletPlaneShape, BulletHeightfieldShape
from panda3d.bullet import ZUp
from direct.showbase.DirectObject import DirectObject

from DebugNode import DebugNode
from SMPlayer import SMPlayer
from SMKeyHandler import SMKeyHandler
from SMCamera import SMCamera
from SMCollisionHandler import SMCollisionHandler
from SMLighting import SMLighting

GRAVITY = 96
GHOST_NODE = None

class SMWorld(DirectObject):

		
	def __init__(self, gameState, mapName, deathHeight):
	
		self.worldObj = self.setupWorld()
		self.debugNode = self.setupDebug()
		self.heightMap = self.setupHeightmap(mapName)
		self.deathZone = self.setupDeathzone(deathHeight)
		self.playerObj = SMPlayer(self.worldBullet, self.worldObj, -5, -8, 40)
		self.playerNP = self.playerObj.getNodePath()
		self.kh = SMKeyHandler()
		self.colObj = self.setupCollisionHandler()
		self.ligObj = SMLighting(Vec4(.4, .4, .4, 1), Vec3(-5, -5, -5), Vec4(2.0, 2.0, 2.0, 1.0))
		
		self.camObj = SMCamera(0, 0, 0, self.playerObj.getNodePath())
		self.camObj.setPos(0, -40, 10)
		self.camObj.reparentTo(self.playerNP)
		
		self.accept('z', self.fire)
		
		
		taskMgr.add(self.update, 'UpdateTask')
		
		print("World initialized.")

	
	def setupWorld(self):
		self.worldBullet = BulletWorld()
		self.worldBullet.setGravity(Vec3(0, 0, -GRAVITY))
		wNP = render.attachNewNode('WorldNode')
		return wNP
	
    #pressing the z button will spawn a block of snow where the snowman is
	def fire(self):
		pos = self.playerObj.getPosition()
		shape = BulletBoxShape(Vec3(12, 12, 3))
		ghostNode = BulletGhostNode('Box')
		
		ghostNode.addShape(shape)
		snowNode = render.attachNewNode(ghostNode)
		snowNode.setPos(pos)
		snowNode.setCollideMask(BitMask32(0x0f))
		self.worldBullet.attachGhost(ghostNode)
		visualSN = loader.loadModel("../res/models/snow.egg")
		visualSN.reparentTo(snowNode)
		
		global GHOST_NODE 
		GHOST_NODE = ghostNode
		
		
	def printSceneGraph(self):
		print(render.ls())
	
	def setupDebug(self):
		debug = DebugNode()
		debugNP = debug.getDebugNode()
		self.worldBullet.setDebugNode(debugNP.node())
		debugNP.hide()
		return debugNP
	
	def setupHeightmap(self, name):
		hmHeight = 80
		hmPath = "../maps/" + name + "-h.png"
		imPath = "../maps/" + name + "-i.png"
		smPath = "../maps/" + name + "-s.png"
		scmPath = "../maps/" + name + "-sc.png"
		hmImg = PNMImage(Filename(hmPath))
		hmShape = BulletHeightfieldShape(hmImg, hmHeight, ZUp)
		hmNode = BulletRigidBodyNode('Terrain')
		hmNode.addShape(hmShape)
		hmNode.setMass(0)
		self.hmNP = render.attachNewNode(hmNode)
		self.worldBullet.attachRigidBody(hmNode)

		hmOffset = hmImg.getXSize() / 2.0 - 0.5
		hmTerrain = GeoMipTerrain('gmTerrain')
		hmTerrain.setHeightfield(hmImg)
		hmTerrain.setBruteforce(True)
		hmTerrain.generate()

		hmTerrainNP = hmTerrain.getRoot()
		hmTerrainNP.setSz(hmHeight)
		hmTerrainNP.setPos(-hmOffset, -hmOffset, -hmHeight / 2.0)
		hmTerrainNP.reparentTo(render)

		# Here begins the scenery mapping
		tree = loader.loadModel("../res/models/tree_1.egg")
		rock = loader.loadModel("../res/models/yeti.egg")
		texpk = loader.loadTexture(scmPath).peek()
		for i in range(0, texpk.getXSize()):
                        for j in range(0, texpk.getYSize()):
                                color = VBase4(0, 0, 0, 0)
                                texpk.lookup(color, float(i) / texpk.getXSize(), float(j) / texpk.getYSize())
                                if(int(color.getX() * 255) == 255):
                                        newTree = render.attachNewNode("newTree")
                                        newTree.setPos(i - texpk.getXSize() / 2, j - texpk.getYSize() / 2, hmTerrain.get_elevation(i, j) * hmHeight - hmHeight / 2)
                                        # newTree.setScale can add some nice randomized scaling here.
                                        tree.instanceTo(newTree)
                                if(int(color.getX() * 255) == 128):
                                        newRock = render.attachNewNode("newRock")
                                        newRock.setPos(i - texpk.getXSize() / 2, j - texpk.getYSize() / 2, hmTerrain.get_elevation(i, j) * hmHeight - hmHeight / 2)
                                        rock.instanceTo(newRock)

                # Here begins the attribute mapping
                ts = TextureStage("stage-alpha")
                ts.setSort(0)
                ts.setPriority(1)
                ts.setMode(TextureStage.MReplace)
                ts.setSavedResult(True)
                hmTerrainNP.setTexture(ts, loader.loadTexture(imPath, smPath))
        
                ts = TextureStage("stage-stone")
                ts.setSort(1)
                ts.setPriority(1)
                ts.setMode(TextureStage.MReplace)
                hmTerrainNP.setTexture(ts, loader.loadTexture("../../textures/stone_tex.png"))
                hmTerrainNP.setTexScale(ts, 32, 32)

                ts = TextureStage("stage-ice")
                ts.setSort(2)
                ts.setPriority(1)
                ts.setCombineRgb(TextureStage.CMInterpolate, TextureStage.CSTexture, TextureStage.COSrcColor,
                                 TextureStage.CSPrevious, TextureStage.COSrcColor,
                                 TextureStage.CSLastSavedResult, TextureStage.COSrcColor)
                hmTerrainNP.setTexture(ts, loader.loadTexture("../../textures/ice_tex.png"))
                hmTerrainNP.setTexScale(ts, 32, 32)

                ts = TextureStage("stage-snow")
                ts.setSort(3)
                ts.setPriority(0)
                ts.setCombineRgb(TextureStage.CMInterpolate, TextureStage.CSTexture, TextureStage.COSrcColor,
                                 TextureStage.CSPrevious, TextureStage.COSrcColor,
                                 TextureStage.CSLastSavedResult, TextureStage.COSrcAlpha)
                hmTerrainNP.setTexture(ts, loader.loadTexture("../../textures/snow_tex_1.png"))
                hmTerrainNP.setTexScale(ts, 32, 32)

		return hmNode

	def setupDeathzone(self, height):
		planeShape = BulletPlaneShape(Vec3(0, 0, 1), 1)
		planeNode = BulletRigidBodyNode('DeathZone')
		planeNode.addShape(planeShape)
		planeNP = render.attachNewNode(planeNode)
		planeNP.setPos(0, 0, height)
		self.worldBullet.attachRigidBody(planeNode)
		return planeNP
	
	def setupCollisionHandler(self):
		colHand = SMCollisionHandler(self.worldBullet)
		return colHand
	
	def playerMove(self):
	
		self.doPlayerTests()
	
		if self.kh.poll('w'):
			self.playerObj.move(True)
		elif self.kh.poll('s'):
			self.playerObj.move(False)
		else:
			self.playerObj.stop()
		
		if self.kh.poll('a'):
			self.playerObj.turn(True)
		elif self.kh.poll('d'):
			self.playerObj.turn(False)
		
		if self.kh.poll(' '):
			self.playerObj.jump()
		self.camObj.lookAt(self.playerObj.getNodePath())
		
		#adjusts player movement if in deep snow
		if self.playerObj.isSnow:
			self.playerObj.MAX_VEL_XY = 25
			self.playerObj.MAX_VEL_Z = 25
		else:
			self.playerObj.MAX_VEL_XY = 50
			self.playerObj.MAX_VEL_Z = 5000
		
	
	def doPlayerTests(self):
		if(self.colObj.didCollide(self.playerNP.node(), self.heightMap)):
			self.playerObj.setAirborneFlag(False)
		else:
			self.playerObj.setAirborneFlag(True)
		
		#test if player is colliding with snow, update appropriatly
		if(GHOST_NODE != None):
			if(self.colObj.didCollide(self.playerNP.node(), GHOST_NODE)):
				self.playerObj.setSnow(True)
				print "hi"
			else:
				self.playerObj.setSnow(False)
				print "mew"

		
	
	def update(self, task):
		dt = globalClock.getDt()
		self.worldBullet.doPhysics(dt)
		self.playerMove()
		return task.cont

