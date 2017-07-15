import libtcodpy as libtcod
import config
from tile import Tile
from rect import Rect
from object import Object

class Map:

    def __init__(self, width, height, room_size_min, room_size_max, max_rooms):
        
        self.width = width
        self.height = height
        self.room_size_min = room_size_min
        self.room_size_max = room_size_max
        self.max_rooms = max_rooms

        self.tiles = [[ Tile(True)
            for y in range(height) ]
                for x in range(width) ]
 
        self.rooms = []
        self._generate()

        # FOV map
        self.fov_map = libtcod.map_new(self.width, self.height)
        for y in range(self.height):
            for x in range(self.width):
                libtcod.map_set_properties(self.fov_map, x, y, not self.is_sight_blocked(x, y), not self.is_blocked(x, y))

    def is_blocked(self, x, y):
        
        # Check map
        if self.tiles[x][y].is_blocked:
            return True

        # Check objects
        for obj in config.objects:
            if obj.blocks and obj.x == x and obj.y == y:
                return True

        return False

    def is_sight_blocked(self, x, y):

        return self.tiles[x][y].is_sight_blocked

    def draw(self):
        
        self._recompute_fov()
        self._draw_map()

    def _recompute_fov(self):
        
        if config.recompute_fov_flag:
            config.recompute_fov_flag = False
            libtcod.map_compute_fov(self.fov_map, config.player.x, config.player.y,
                                    config.TORCH_RADIUS, config.FOV_LIGHT_WALLS, config.FOV_ALGO)

    def _draw_map(self):

        for y in range(self.height):
            for x in range(self.width):
                visible = libtcod.map_is_in_fov(self.fov_map, x, y)
                blocked = self.is_blocked(x, y)
                if not visible:
                    if not self._is_explored(x, y):
                        continue
                    if blocked:
                        libtcod.console_put_char_ex(config.console, x, y, '#', libtcod.white, config.color_dark_wall)
                    else:
                        libtcod.console_put_char_ex(config.console, x, y, '.', libtcod.white, config.color_dark_ground)
                else: # Visible
                    self._explore(x, y)
                    if blocked:
                        libtcod.console_put_char_ex(config.console, x, y, '#', libtcod.white, config.color_light_wall)
                    else:
                        libtcod.console_put_char_ex(config.console, x, y, '.', libtcod.white, config.color_light_ground)
    
    def _generate(self):

        for room in range(self.max_rooms):

            # Ramdom width and height
            width = libtcod.random_get_int(0, self.room_size_min, self.room_size_max)
            height = libtcod.random_get_int(0, self.room_size_min, self.room_size_max)

            # Random position
            x = libtcod.random_get_int(0, 0, self.width - width - 1)
            y = libtcod.random_get_int(0, 0, self.height - height - 1)

            # Test intersection
            new_room = Rect(x, y, width, height)
            if self._is_interected_with_existing_rooms(new_room):
                continue

            # Create new room
            self._create_room(new_room)
            num_rooms = len(self.rooms)
            if num_rooms == 0:
                # Put player in the first room
                config.player.x = new_room.center_x
                config.player.y = new_room.center_y
            else:
                # Connect new room to previous room
                prev_room = self.rooms[num_rooms - 1]
                if libtcod.random_get_int(0, 0, 1) == 1: # Flip coin
                    # Horizontal, vertical
                    self._create_horizontal_tunnel(prev_room.center_x, new_room.center_x, prev_room.center_y)
                    self._create_vertical_tunnel(prev_room.center_y, new_room.center_y, new_room.center_x)
                else:
                    # Vertical, horizontal
                    self._create_vertical_tunnel(prev_room.center_y, new_room.center_y, prev_room.center_x)
                    self._create_horizontal_tunnel(prev_room.center_x, new_room.center_x, new_room.center_y)

            self.rooms.append(new_room)

    def _create_room(self, room_rect):
        
        # Leave borders as walls
        for y in range(room_rect.y1 + 1, room_rect.y2):
            for x in range(room_rect.x1 + 1, room_rect.x2):
                self.tiles[x][y].is_blocked = False
                self.tiles[x][y].is_sight_blocked = False

        self._populate_room(room_rect)

    def _populate_room(self, room_rect):

        num_monsters = libtcod.random_get_int(0, 0, config.MAX_ROOM_MONSTERS)
        for i in range(num_monsters):

            # Random position
            pos = room_rect.get_random_position()
            while self.is_blocked(*pos):
                pos = room_rect.get_random_position()

            monster = self._create_monster(*pos)
            config.objects.append(monster)
    
    def _create_monster(self, x, y):

        monster = None
        if libtcod.random_get_int(0, 0, 100) < 80:  # 80% chance of getting an orc
            # Orc
            monster = Object(x, y, 'o', 'Orc', libtcod.desaturated_green, True)
        else:
            # Troll
            monster = Object(x, y, 'T', 'Troll', libtcod.darker_green, True)

        return monster

    def _create_horizontal_tunnel(self, x1, x2, y):

        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].is_blocked = False
            self.tiles[x][y].is_sight_blocked = False

    def _create_vertical_tunnel(self, y1, y2, x):

        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].is_blocked = False
            self.tiles[x][y].is_sight_blocked = False

    def _is_interected_with_existing_rooms(self, new_room):

        is_intersected = False
        for room in self.rooms:
            if new_room.is_intersected(room):
                is_intersected = True
                break
        
        return is_intersected

    def _explore(self, x, y):

        self.tiles[x][y].is_explored = True

    def _is_explored(self, x, y):

        return self.tiles[x][y].is_explored

