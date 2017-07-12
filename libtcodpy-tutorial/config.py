import libtcodpy as libtcod
from map import Map
from tile import Tile
from object import Object

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
MAP_WIDTH = 80
MAP_HEIGHT = 45
LIMIT_FPS = 20

ROOM_SIZE_MIN = 6
ROOM_SIZE_MAX = 10
MAX_ROOMS = 30

FOV_ALGO = 0
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10

color_dark_wall = libtcod.Color(0, 0, 100)
color_light_wall = libtcod.Color(130, 110, 50)
color_dark_ground = libtcod.Color(50, 50, 150)
color_light_ground = libtcod.Color(200, 180, 50)

console = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
player = Object(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, '@', libtcod.white)
#npc = Object(SCREEN_WIDTH / 2 - 5, SCREEN_HEIGHT / 2, '@', libtcod.yellow)
objects = [player]

recompute_fov_flag = True
map = Map(MAP_WIDTH, MAP_HEIGHT, ROOM_SIZE_MIN, ROOM_SIZE_MAX, MAX_ROOMS)
