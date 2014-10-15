from panda3d.core import KeyboardButton

class SMKeyHandler():
	
	def poll(self, keyChar):
		keyPressed = base.mouseWatcherNode.is_button_down
		key = KeyboardButton.ascii_key(keyChar)
		if keyPressed(key):
			return True
		else:
			return False
