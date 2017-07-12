class Tile:
    
    def __init__(self, is_blocked, is_sight_blocked = None):

        self.is_explored = False
        self.is_blocked = is_blocked
        self.is_sight_blocked = is_sight_blocked

        # Tile that blocks would also blocks sight
        if is_sight_blocked is None:
            self.is_sight_blocked = is_blocked


