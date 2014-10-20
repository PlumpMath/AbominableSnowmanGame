from panda3d.core import Vec3, VBase3, Vec4, BitMask32, Point3, KeyboardButton, Filename, PNMImage, GeoMipTerrain
from panda3d.core import LightRampAttrib, AmbientLight, DirectionalLight

class SMLighting():

	def __init__(self, aCol, dDir, dCol):
		render.setAttrib(LightRampAttrib.makeHdr1())
		ambientLight = AmbientLight("ambientLight")
		ambientLight.setColor(aCol)
		directionalLight = DirectionalLight("directionalLight")
		directionalLight.setDirection(dDir)
		directionalLight.setColor(dCol)
		directionalLight.setSpecularColor(Vec4(2.0, 2.0, 2.0, 0))
		render.setLight(render.attachNewNode(ambientLight))
		render.setLight(render.attachNewNode(directionalLight))
