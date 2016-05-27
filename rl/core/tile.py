from rl.core.creature import Creature

class Tile:
    def __init__(self):
        self.type = ""
        self.passable = True
        self.visible = True
        self.known = False
        self.blocking = False
        self.stack = []

    def is_occupied(self):
        for object in self.stack:
            if not object.passable:
                return True
        return False

    def get_occupier(self):
        for object in self.stack:
            if not object.passable:
                return object
        return None

    def is_blocking(self):
        if self.blocking:
            return True
        for object in self.stack:
            if object.blocking:
                return True
        return False

    def update_stack(self):
        self.stack.sort(key=lambda x: x.stack_order)

