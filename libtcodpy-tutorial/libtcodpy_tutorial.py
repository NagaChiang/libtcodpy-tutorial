import libtcodpy as libtcod
import config
from map import Rect

def render_all():

    config.map.draw()
    for object in config.objects:
        object.draw()

    libtcod.console_blit(config.console, 0, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT, 0, 0, 0)

def clear_all():

    for object in config.objects:
        object.clear()

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
        config.recompute_fov_flag = True
    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        config.player.move(0, 1)
        config.recompute_fov_flag = True
    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        config.player.move(-1, 0)
        config.recompute_fov_flag = True
    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        config.player.move(1, 0)
        config.recompute_fov_flag = True

    return False

def main():

    libtcod.console_set_custom_font('fonts/arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(config.SCREEN_WIDTH, config.SCREEN_HEIGHT, 'python/libtcod tutorial', False)
    libtcod.sys_set_fps(config.LIMIT_FPS)

    while not libtcod.console_is_window_closed():

        render_all()
        libtcod.console_flush()
        clear_all()

        is_exit = handle_inputs()
        if is_exit:
            break

if __name__ == "__main__":
    main()