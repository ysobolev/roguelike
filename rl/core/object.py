class Object:
    blocking = False
    mostly_fixed = False
    movable = True
    passable = True
    pushable = False
    stack_order = 0
    type = ""

    def __init__(self):
        pass

class Item(Object):
    pass

class Feature(Object):
    mostly_fixed = True
    stack_order = 1

class ImpassableFeature(Feature):
    passable = False
    stack_order = 2

