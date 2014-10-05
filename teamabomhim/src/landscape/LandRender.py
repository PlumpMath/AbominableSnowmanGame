from panda3d.core import GeoMipTerrain
from direct.showbase.ShowBase import ShowBase

class LandRender(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        terrain = self.genTerrain("res/heightmap.png", "res/colormap.png")
        root = terrain.getRoot()
        root.reparentTo(render)
        root.setScale(0.05, 0.05, 0.05)
        root.setPos(-25, 25, -10)
        root.setSz(5)

    def genTerrain(self, heightmap, colormap):
        terrain = GeoMipTerrain("worldTerrain")
        terrain.setHeightfield(heightmap)
        terrain.setColorMap(colormap)
        terrain.setBruteforce(True)
        terrain.generate()
        return terrain

app = LandRender()
app.run()
