import libtcodpy as libtcod
import config

class Object:
    
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx, dy):

        if config.map[self.x + dx][self.y + dy].is_blocked:
            return

        self.x += dx
        self.y += dy

    def draw(self, target_console):
        libtcod.console_set_default_foreground(target_console, self.color)
        libtcod.console_put_char(target_console, self.x, self.y, self.char, libtcod.BKGND_NONE)

    def clear(self, target_console):
        libtcod.console_put_char(target_console, self.x, self.y, ' ', libtcod.BKGND_NONE)

