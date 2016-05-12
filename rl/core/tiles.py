import rl.core.tile as tile

class FloorTile(tile.Tile):
    def __init__(self):
        tile.Tile.__init__(self)
        self.type = "floor"

class ImpassableTile(tile.Tile):
    def __init__(self):
        tile.Tile.__init__(self)
        self.type = "impassable"
        self.passable = False

class WallTile(ImpassableTile):
    def __init__(self):
        ImpassableTile.__init__(self)
        self.type = "wall"
        self.blocking = True

