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

    def maze_fill(self):
        return
        graph = {}
        for i in range(1, 21, 2):
            for j in range(1, 79, 2):
                if isinstance(self.tiles[i][j], tileset.WallTile):
                    graph[(i, j)] = []
        for tile in graph:
            i, j = tile
            if (i+2, j) in graph:
                graph[(i, j)].append(((i+2, j), random.randint(1,5)))
                graph[(i+2, j)].append(((i, j), random.randint(1,5)))
            if (i, j+2) in graph:
                graph[(i, j)].append(((i, j+2), random.randint(1,5)))
                graph[(i, j+2)].append(((i, j), random.randint(1,5)))
        tree = find_minimal_spanning_tree(graph, (5, 5))
        for vertex in tree:
            i1, j1 = vertex
            if tree[vertex] is None:
                self.tiles[i1][j1] = tileset.FloorTile()
                continue
            i2, j2 = tree[vertex]
            self.tiles[i2][j2] = tileset.FloorTile()
            self.tiles[(i1+i2)/2][(j1+j2)/2] = tileset.FloorTile()

class Direction:
    compass = {"n":(-1, 0), "s":(1, 0), "w":(0, -1), "e":(0, 1),
        "nw":(-1, -1), "ne":(-1, 1), "sw":(1, -1), "se":(1, 1)}

    cardinals = {(-1, 0):"n", (1, 0):"s", (0, -1):"w", (0, 1):"e",
        (-1, -1):"nw", (-1, 1):"ne", (1, -1):"sw", (1, 1):"se"}
