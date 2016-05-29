from rl.core.map import Map
from rl.core.map import Direction
from rl.core.player import Player
from rl.core.objects import *
import copy
from rl.core.astar import a_star
from collections import defaultdict
import time

from rl.core.levels import create_empty, create_maze, create_room

class GameExit(Exception):
    pass

class Game:
    def __init__(self, interface):
        self.interface = interface
        self.player = Player()
        self.map = Map()
        #self.map.maze_fill()
        create_room(self.map, ((10, 16), (10, 16)))
        create_maze(self.map, ((10, 16), (17, 30)))
        self.map.tiles[5][5].stack.append(self.player)
        #self.map.tiles[5][7].stack.append(Boulder())
        #self.map.tiles[5][8].stack.append(Boulder())
        #self.map.tiles[7][7].stack.append(Pillar())
        #self.map.tiles[10][20].stack.append(Potion())
        """
        mapdata = open("/home/yury/map", "r")
        i = 1
        for line in mapdata.readlines():
            j = 1
            for char in line:
                obj = None
                if char == "-":
                    obj = SeeThroughWallMinus()
                elif char == "|":
                    obj = SeeThroughWallPipe()
                elif char == "+":
                    obj = SeeThroughWallPlus()
                elif char == "0":
                    obj = SeeThroughBoulder()
                elif char == "@":
                    obj = self.player
                    self.player.position = (i, j)
                if obj:
                    self.map.tiles[i][j].stack.append(obj)
                j += 1
            i += 1
        """
        self.levels = []
        self.time = 0
        self.update_map()
        self.interface.update(self.player)
        self.interface.say("Welcome to Yury's roguelike!")

    def play(self):
        while True:
            command = self.interface.interact()
            try:
                self.handle_command(command)
            except GameExit:
                self.exit = True
                return
            except Exception, e:
                self.last_error = e
                raise

    def handle_command(self, command):
        try:
            tokens = command.split()
        except:
            return
        if len(tokens) == 0:
            return
        if tokens[0] == "move":
            if len(tokens) != 2:
                return
            direction = tokens[1]
            self.handle_move(direction)
            self.interface.update(self.player)
        elif tokens[0] == "pathfind":
            self.pathfind()
        elif tokens[0] == "quit":
            response = self.interface.ask("Quit? (y/N) ")
            if response.lower() == "y":
                raise GameExit()
    
    def handle_move(self, direction):
        source = self.player.position
        dr = Direction.compass[direction][0]
        dc = Direction.compass[direction][1]
        target = (source[0] + dr, source[1] + dc)
        source_tile = self.map.get_tile(source)
        target_tile = self.map.get_tile(target)
        if target_tile.passable:
            if not target_tile.is_occupied():
                self.move(self.player, source, target)
            else:
                self.handle_displacement(direction)
        elif target_tile.is_occupied():
            self.handle_displacement(direction)
        self.update_map()

    def pathfind(self):
        map = self.player.map
        known = defaultdict(list)
        for r in range(1, map.size[0] - 1):
            for c in range(1, map.size[1] - 1):
                if not map.tiles[r][c].known or not map.tiles[r][c].passable:
                    continue
                if map.tiles[r+1][c].known and map.tiles[r+1][c].passable:
                    known[(r, c)].append(((r+1, c), 1))
                    known[(r+1, c)].append(((r, c), 1))
                if map.tiles[r][c+1].known and map.tiles[r][c+1].passable:
                    known[(r, c)].append(((r, c+1), 1))
                    known[(r, c+1)].append(((r, c), 1))
        def heuristic(x, y):
            return abs(x[0] - y[0]) + abs(x[1] - y[1])
        path = a_star(known, self.player.position, (5, 5), heuristic)
        if path == None:
            return
        path.pop(0)
        for element in path:
            position = self.player.position
            direction = ""
            if position[0] > element[0]:
                direction = "n"
            elif position[0] < element[0]:
                direction = "s"
            elif position[1] > element[1]:
                direction = "w"
            elif position[1] < element[1]:
                direction = "e"
            self.handle_command("move %s" % direction)

    def handle_displacement(self, direction):
        """Attempt to displace target."""
        source = self.player.position
        self.push(source, direction)

    def move(self, object, source, target):
        source_tile = self.map.get_tile(source)
        target_tile = self.map.get_tile(target)
        source_tile.stack.remove(object)
        target_tile.stack.append(object)
        target_tile.update_stack()
        object.position = target

    def push(self, source, direction):
        dr = Direction.compass[direction][0]
        dc = Direction.compass[direction][1]
        target = (source[0] + dr, source[1] + dc)
        source_tile = self.map.get_tile(source)
        target_tile = self.map.get_tile(target)
        source_object = source_tile.get_occupier()
        target_object = target_tile.get_occupier()
        if target_object.pushable:
            next = (target[0] + dr, target[1] + dc)
            next_tile = self.map.get_tile(next)
            if next_tile.passable and not next_tile.is_occupied():
                self.move(target_object, target, next)
                self.move(source_object, source, target)

    def tick(self):
        """Increment time by one."""
        self.time += 1

    def generate_line(self, source, target):
        points = []
        distance = (abs(target[1] - source[1])**2 + abs(target[0] - source[0])**2)**(0.5)
        granularity = int(2 * distance)
        if granularity == 0:
            return []
        x = source[0]
        y = source[1]
        dx = float(target[0] - source[0]) / float(granularity)
        dy = float(target[1] - source[1]) / float(granularity)
        for i in range(granularity):
            x += dx
            y += dy
            point = (int(round(x)), int(round(y)))
            if point != source and point != target and point not in points:
                points.append(point)
        return points

    def update_map(self):
        """Update visible tiles, creatures, and objects."""
        source = self.player.position
        row = source[0]
        col = source[1]
        map = self.player.map
        for r in range(map.size[0]):
            for c in range(map.size[1]):
                if (abs(row - r) * 1)**2 + abs(col - c)**2 > self.player.visibility:
                    map.tiles[r][c].visible = False
                else:
                    map.tiles[r][c] = copy.copy(self.map.tiles[r][c])
                    path_blocked = False
                    for point in self.generate_line((r, c), (row, col)):
                        if self.map.tiles[point[0]][point[1]].is_blocking():
                            path_blocked = True
                            break
                    if path_blocked:
                        map.tiles[r][c].visible = False
                    else:
                        map.tiles[r][c].visible = True
                        self.map.tiles[r][c].known = True
                        map.tiles[r][c].known = True

