from rl.core.creature import Creature
from rl.core.map import Map

class Player(Creature):
	def __init__(self):
		Creature.__init__(self)
		self.map = Map()
		self.position = (5, 5)
		self.type = "player"
		self.visibility = 75
