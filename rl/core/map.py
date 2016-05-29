from rl.core.tile import Tile
import rl.core.tiles as tileset
from rl.core.prim import find_minimal_spanning_tree
import random

class Map:
    def __init__(self, size=None):
        if size == None:
            size = (22, 80)
        self.size = size
        self.tiles = [[tileset.FloorTile() for i in range(size[1])] for j in range(size[0])]

    def get_tile(self, position):
        if position[0] < 0 or position[0] >= self.size[0]:
            return tileset.ImpassableTile()
        if position[1] < 0 or position[1] >= self.size[1]:
            return tileset.ImpassableTile()
        return self.tiles[position[0]][position[1]]

class Direction:
    compass = {"n":(-1, 0), "s":(1, 0), "w":(0, -1), "e":(0, 1),
        "nw":(-1, -1), "ne":(-1, 1), "sw":(1, -1), "se":(1, 1)}

    cardinals = {(-1, 0):"n", (1, 0):"s", (0, -1):"w", (0, 1):"e",
        (-1, -1):"nw", (-1, 1):"ne", (1, -1):"sw", (1, 1):"se"}
