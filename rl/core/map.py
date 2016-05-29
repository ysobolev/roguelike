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

    def __getitem__(self, position):
        return self.get_tile(position)
    
    def __setitem__(self, position, tile):
        if position[0] < 0 or position[0] >= self.size[0]:
            raise ValueError
        if position[1] < 0 or position[1] >= self.size[1]:
            raise ValueError
        self.tiles[position[0]][position[1]] = tile

    def get_tile(self, position):
        if position[0] < 0 or position[0] >= self.size[0]:
            return tileset.ImpassableTile()
        if position[1] < 0 or position[1] >= self.size[1]:
            return tileset.ImpassableTile()
        return self.tiles[position[0]][position[1]]

    def __iter__(self):
        for r in range(0, self.size[0]):
            for c in range(0, self.size[1]):
                yield (r, c), self.get_tile((r, c))

class Direction:
    compass = {"n":(-1, 0), "s":(1, 0), "w":(0, -1), "e":(0, 1),
        "nw":(-1, -1), "ne":(-1, 1), "sw":(1, -1), "se":(1, 1)}

    cardinals = {(-1, 0):"n", (1, 0):"s", (0, -1):"w", (0, 1):"e",
        (-1, -1):"nw", (-1, 1):"ne", (1, -1):"sw", (1, 1):"se"}

    @staticmethod
    def e(position):
        return (position[0], position[1] + 1)
    
    @staticmethod
    def w(position):
        return (position[0], position[1] - 1)
    
    @staticmethod
    def n(position):
        return (position[0] - 1, position[1])
    
    @staticmethod
    def s(position):
        return (position[0] + 1, position[1])
    
    @staticmethod
    def ne(position):
        return (position[0] - 1, position[1] + 1)
    
    @staticmethod
    def nw(position):
        return (position[0] - 1, position[1] - 1)
    
    @staticmethod
    def se(position):
        return (position[0] + 1, position[1] + 1)
    
    @staticmethod
    def sw(position):
        return (position[0] + 1, position[1] - 1)

