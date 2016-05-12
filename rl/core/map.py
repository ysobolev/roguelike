from rl.core.tile import Tile
import rl.core.tiles as tileset

class Map:
	def __init__(self, size=None):
		if size == None:
			size = (22, 80)
		self.size = size
		self.tiles = [[tileset.WallTile() for i in range(size[1])] for j in range(size[0])]
		for i in range(1, 21):
			for j in range(1, 79):
				self.tiles[i][j] = tileset.FloorTile()

	def get_tile(self, position):
		if position[0] < 0 or position[0] >= self.size[0]:
			return tileset.ImpassableTile()
		if position[1] < 0 or position[1] >= self.size[1]:
			return tileset.ImpassableTile()
		return self.tiles[position[0]][position[1]]

class Direction:
	compass = {"n":(-1, 0), "s":(1, 0), "w":(0, -1), "e":(0, 1),
		"nw":(-1, -1), "ne":(-1, 1), "sw":(1, -1), "se":(1, 1)}

