from rl.core.object import Item
from rl.core.object import Feature
from rl.core.object import ImpassableFeature

class Boulder(ImpassableFeature):
	def __init__(self):
		ImpassableFeature.__init__(self)
		self.type = "boulder"
		self.pushable = True
		self.blocking = True

class SeeThroughBoulder(ImpassableFeature):
	def __init__(self):
		ImpassableFeature.__init__(self)
		self.type = "boulder"
		self.pushable = True
		self.blocking = False

class Pillar(ImpassableFeature):
	def __init__(self):
		ImpassableFeature.__init__(self)
		self.type = "pillar"
		self.movable = False
		self.pushable = False
		self.blocking = True

class SeeThroughWall(ImpassableFeature):
	def __init__(self):
		ImpassableFeature.__init__(self)
		self.type = "wall"
		self.movable = False
		self.pushable = False
		self.blocking = False

class SeeThroughWallMinus(ImpassableFeature):
	def __init__(self):
		ImpassableFeature.__init__(self)
		self.type = "wall-"
		self.movable = False
		self.pushable = False
		self.blocking = False

class SeeThroughWallPipe(ImpassableFeature):
	def __init__(self):
		ImpassableFeature.__init__(self)
		self.type = "wall|"
		self.movable = False
		self.pushable = False
		self.blocking = False

class SeeThroughWallPlus(ImpassableFeature):
	def __init__(self):
		ImpassableFeature.__init__(self)
		self.type = "wall+"
		self.movable = False
		self.pushable = False
		self.blocking = False

class Potion(Item):
	def __init__(self):
		Item.__init__(self)
		self.type = "potion"

