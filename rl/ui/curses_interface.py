from rl.ui.interface import Interface
from rl.core.game import Game
import curses
import readline
import code

tiles = {"floor":".", "wall":"#"}
objects = {"player":"@", "boulder":"0", "pillar":"I", "potion":"!", "wall-":"-",
           "wall|":"|", "wall+":"+"}

class CursesInterface(Interface):
    def __init__(self):
        self.init_curses()
        self.width = curses.tigetnum("cols")
        self.height = curses.tigetnum("lines")
        self.message = curses.newpad(1, self.width)
        self.map = curses.newpad(self.height - 1, self.width)
        self.status = curses.newpad(1, self.width)
        self.player = None
        self.selection = None

    def init_curses(self):
        self.stdscr = curses.initscr()
        curses.cbreak()
        curses.noecho()
        self.stdscr.keypad(1)
    
    def shutdown_curses(self):
        self.stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def shift_selection(self, dr, dc):
        if self.selection is None:
            return
        if (0 <= self.selection[0] + dr <= self.height - 3) and \
                (0 <= self.selection[1] + dc <= self.width - 1):     
            self.selection[0] += dr
            self.selection[1] += dc
            self.__refocus()

    def interact(self):
        self.message.erase()
        c = chr(self.map.getch())
        if c == "h":
            if self.selection is None:
                return "move w"
            self.shift_selection(0, -1)
        elif c == "j":
            if self.selection is None:
                return "move s"
            self.shift_selection(1, 0)
        elif c == "k":
            if self.selection is None:
                return "move n"
            self.shift_selection(-1, 0)
        elif c == "l":
            if self.selection is None:
                return "move e"
            self.shift_selection(0, 1)
        elif c == "y":
            if self.selection is None:
                return "move nw"
            self.shift_selection(-1, -1)
        elif c == "u":
            if self.selection is None:
                return "move ne"
            self.shift_selection(-1, 1)
        elif c == "b":
            if self.selection is None:
                return "move sw"
            self.shift_selection(1, -1)
        elif c == "n":
            if self.selection is None:
                return "move se"
            self.shift_selection(1, 1)
        elif c == " ":
            self.__refresh_message()
            self.__refocus()
        elif c == ".":
            if self.selection:
                target = self.selection
                self.selection = None
                self.__refocus()
                return "pathfind %s %s" % tuple(target)
        elif c == "v":
            try:
                self.player.visibility = int(self.ask_phrase("New visibility radius: "))
            except:
                pass
        elif c == "_":
            if self.selection:
                self.selection = None
            else:
                self.selection = list(self.player.position)
            #return "pathfind"
        elif c == "q":
            return "quit"
        elif c == "~":
            try:
                self.stdscr.clear()
                self.stdscr.refresh()
                self.shutdown_curses()
                self.console.interact()
                self.init_curses()
                self.redraw()
            except:
                pass
            return None
        return None

    def update(self, player):
        self.player = player
        self.redraw()

    def animate(self, animation):
        pass

    def say(self, message):
        if len(message) > self.width:
            lines = []
            for i in range(0, len(message), self.width - 10):
                lines.append(message[i:i+self.width-10])
            for line in lines[:-1]:
                self.message.addstr(0, 0, line + " --more--")
                self.__refresh_message()
                while self.message.getch() != ord(" "):
                    pass
                self.message.erase()
                self.__refresh_message()
            message = lines[-1]
        self.message.addstr(0, 0, message)
        self.__refresh_message()
        self.__refocus()

    def ask(self, query):
        self.message.addstr(0, 0, query)
        self.__refresh_message()
        response = chr(self.message.getch())
        self.message.erase()
        self.__refresh_message()
        self.__refocus()
        return response
    
    def ask_phrase(self, query):
        self.message.addstr(0, 0, query)
        self.__refresh_message()
        response = self.message.getstr(0, len(query) + 1, 32)
        self.message.erase()
        self.__refresh_message()
        self.__refocus()
        return response

    def menu(self, items):
        return None

    def redraw(self):
        if self.player == None:
            return
        self.__refresh_message(True)
        self.status.erase()
        self.__refresh_status(True)
        map = self.player.map
        self.map.erase()
        for r in range(len(map.tiles)):
            for c in range(len(map.tiles[r])):
                tile = map.tiles[r][c]
                self.__render_tile(r, c, tile)
        self.__refocus(True)
        curses.doupdate()

    def __refresh_status(self, nout=False):
        if nout:
            self.status.noutrefresh(0, 0,
                self.height - 1, 0,
                self.height - 1, self.width - 1)
        else:
            self.status.refresh(0, 0,
                self.height - 1, 0,
                self.height - 1, self.width - 1)

    def __refresh_message(self, nout=False):
        if nout:
            self.message.noutrefresh(0, 0,
                0, 0,
                self.height - 1, self.width - 1)
        else:
            self.message.refresh(0, 0,
                0, 0,
                self.height - 1, self.width - 1)

    def __refresh_map(self, nout=False):
        if nout:
            self.map.noutrefresh(0, 0,
                1, 0,
                self.height - 1, self.width - 1)
        else:
            self.map.refresh(0, 0,
                1, 0,
                self.height - 1, self.width - 1)

    def __refocus(self, nout=False):
        if self.player == None:
            return
        if self.selection:
            self.map.move(*self.selection)
        else:
            self.map.move(self.player.position[0], self.player.position[1])
        self.__refresh_map(nout)
    
    def __render_tile(self, r, c, tile):
        if tile.known:
            character = tiles[tile.type]
            if tile.type == "floor" and not tile.visible:
                character = " "
            self.map.addch(r, c, ord(character))
            for item in tile.stack:
                if tile.visible or item.mostly_fixed:
                    self.map.addch(r, c, objects[item.type])

def run():
    interface = CursesInterface()
    game = Game(interface)
    interface.console = code.InteractiveConsole({"interface":interface, "game":game})
    try:
        game.play()
    finally:
        try:
            interface.shutdown_curses()
        except:
            pass
    return interface, game

