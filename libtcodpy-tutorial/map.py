import libtcodpy as libtcod
import config
from tile import Tile
from rect import Rect


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

    def is_blocked(self, x, y):
        
        return self.tiles[x][y].is_blocked

    def is_sight_blocked(self, x, y):

        return self.tiles[x][y].is_sight_blocked

    def draw(self):
        
        for y in range(self.height):
            for x in range(self.width):
                if self.is_blocked(x, y):
                    libtcod.console_set_char_background(config.console, x, y, config.color_dark_wall, libtcod.BKGND_SET)
                else:
                    libtcod.console_set_char_background(config.console, x, y, config.color_dark_ground, libtcod.BKGND_SET)
    
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

    def _create_room(self, rect):
        
        # Leave borders as walls
        for y in range(rect.y1 + 1, rect.y2):
            for x in range(rect.x1 + 1, rect.x2):
                self.tiles[x][y].is_blocked = False
                self.tiles[x][y].is_sight_blocked = False

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

