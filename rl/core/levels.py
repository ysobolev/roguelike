from rl.core.map import Map
from rl.core.tile import Tile
import rl.core.tiles as tileset
from rl.core.prim import find_minimal_spanning_tree
import random

def create_maze(map, region=None):
    if region is None:
        region = ((0, map.size[0] - 1), (0, map.size[1] - 1))
    fill_region(map, region, tileset.WallTile)
    graph = {}
    for i in range(*region[0])[::2]:
        for j in range(*region[1])[::2]:
            graph[(i, j)] = []
    for tile in graph:
        i, j = tile
        if (i+2, j) in graph:
            graph[(i, j)].append(((i+2, j), random.randint(1,2)))
            graph[(i+2, j)].append(((i, j), random.randint(1,2)))
        if (i, j+2) in graph:
            graph[(i, j)].append(((i, j+2), random.randint(1,2)))
            graph[(i, j+2)].append(((i, j), random.randint(1,2)))
    tree = find_minimal_spanning_tree(graph)
    for vertex in tree:
        i1, j1 = vertex
        if tree[vertex] is None:
            map.tiles[i1][j1] = tileset.FloorTile()
            continue
        i2, j2 = tree[vertex]
        map.tiles[i2][j2] = tileset.FloorTile()
        map.tiles[(i1+i2)/2][(j1+j2)/2] = tileset.FloorTile()

def fill_region(map, region=None, tile_class=None):
    if region is None:
        region = ((0, map.size[0] - 1), (0, map.size[1] - 1))
    if tile_class is None:
        tile_class = tileset.FloorTile
    for i in range(*region[0]):
        for j in range(*region[1]):
            map.tiles[i][j] = tile_class()

def create_room(map, region=None):
    if region is None:
        region = ((0, map.size[0] - 1), (0, map.size[1] - 1))
    for i in range(*region[0]):
        for j in range(*region[1]):
            if i in (region[0][0], region[0][1] - 1) or \
               j in (region[1][0], region[1][1] - 1):
                map.tiles[i][j] = tileset.WallTile()
            else:
                map.tiles[i][j] = tileset.FloorTile()

def create_empty(map, region=None):
    return fill_region(map, region)

