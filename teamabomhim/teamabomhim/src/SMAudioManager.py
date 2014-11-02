from panda3d.core import FilterProperties

# WE HAVE REVERB NATIVELY SUPPORTED !!
# https://www.panda3d.org/apiref.php?page=FilterProperties


class SMAudioManager():
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Refer to the sound/bgm with the filename.
	# audioMgr.loadBGM("yetiMusic01")
	# audioMgr.playBGM("yetiMusic01")
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def __init__(self):
		print("Sound manager initialized.")
		self.filterProps = FilterProperties()
		# self.filterProps.addReverb(0.6, 0.5, 0.1, 0.1, 0.1)
		self.bgms = {}
		self.sfxs = {}
		self.currentBGM = "null"
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Loads background music that will loop while played.
	# loadBGM("name", "filename")
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def loadBGM(self, file):
		snd = loader.loadSfx("../res/ambient/" + str(file) + ".ogg")
		snd.setLoop(1)
		snd.setVolume(0.5)
		self.bgms[file] = snd
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Loads a sound effect.
	# loadSFX("name", "filename")
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def loadSFX(self, file):
		self.sfxs[file] = loader.loadSfx("../res/sound/" + str(file) + ".ogg")
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Plays a BGM by name.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def playBGM(self, name):
	
		# If the passed BGM isn't currently playing and the sound is loaded
		if(self.bgms.has_key(name)):
			if (not(self.currentBGM == name)):
				self.currentBGM = name
				snd = self.bgms[name]
				snd.play()
			else:
				print("BGM doesn't exist.")
		else:
			print("BGM not loaded!")
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Stops the currently playing BGM.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def stopBGM(self):
		if(self.currentBGM != "null"):
			snd = self.bgms[self.currentBGM]
			snd.stop()
		else:
			print("No BGM is currently playing.")
			
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Plays a sound effect.
	#------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def playSFX(self, name):
		snd = self.sfxs[name]
		snd.play()
