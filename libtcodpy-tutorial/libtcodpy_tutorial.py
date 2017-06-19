import libtcodpy as libtcod
import config
from object import Object
from tile import Tile

def make_map():
 
    config.map = [[ Tile(False)
            for y in range(config.MAP_HEIGHT) ]
                for x in range(config.MAP_WIDTH) ]
 
    # Place two pillars to test the map
    config.map[30][22].is_blocked = True
    config.map[30][22].is_sight_blocked = True
    config.map[50][22].is_blocked = True
    config.map[50][22].is_sight_blocked = True

def render_all():

    for y in range(config.MAP_HEIGHT):
        for x in range(config.MAP_WIDTH):
            is_wall = config.map[x][y].is_blocked
            if is_wall:
                libtcod.console_set_char_background(config.console, x, y, config.color_dark_wall, libtcod.BKGND_SET)
            else:
                libtcod.console_set_char_background(config.console, x, y, config.color_dark_ground, libtcod.BKGND_SET)

    for object in objects:
            object.draw(config.console)

    libtcod.console_blit(config.console, 0, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT, 0, 0, 0)

def clear_all():

    for object in objects:
            object.clear(config.console)

def handle_inputs():
    global player_x, player_y

    # Window
    key = libtcod.console_wait_for_keypress(True) # Block!
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit
        return True

    # Movement
    if libtcod.console_is_key_pressed(libtcod.KEY_UP):
        config.player.move(0, -1)
    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        config.player.move(0, 1)
    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        config.player.move(-1, 0)
    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        config.player.move(1, 0)

    return False

def main():

    libtcod.console_set_custom_font('fonts/arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(config.SCREEN_WIDTH, config.SCREEN_HEIGHT, 'python/libtcod tutorial', False)
    libtcod.sys_set_fps(config.LIMIT_FPS)

    # map
    make_map()

    # Create object representing the player
    config.player = Object(config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2, '@', libtcod.white)
 
    # Create an NPC
    npc = Object(config.SCREEN_WIDTH/2 - 5, config.SCREEN_HEIGHT/2, '@', libtcod.yellow)
 
    # The list of objects with those two
    global objects
    objects = [npc, config.player]

    while not libtcod.console_is_window_closed():

        render_all()
        libtcod.console_flush()
        clear_all()

        is_exit = handle_inputs()
        if is_exit:
            break

if __name__ == "__main__":
    main()