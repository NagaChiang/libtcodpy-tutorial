import libtcodpy as libtcod
import config

class Object:
    
    def __init__(self, x, y, char, name, color, blocks):

        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.color = color
        self.blocks = blocks

    def move(self, dx, dy):

        if config.map.is_blocked(self.x + dx, self.y + dy):
            return

        self.x += dx
        self.y += dy

    def draw(self):
        libtcod.console_set_default_foreground(config.console, self.color)
        libtcod.console_put_char(config.console, self.x, self.y, self.char, libtcod.BKGND_NONE)

    def clear(self):
        libtcod.console_put_char(config.console, self.x, self.y, ' ', libtcod.BKGND_NONE)

