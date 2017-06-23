class Rect:
    
    def __init__(self, x, y, width, height):

        # Top-left
        self.x1 = x
        self.y1 = y

        # Bottom-right
        self.x2 = x + width
        self.y2 = y + height

        # Center
        self.center_x = (self.x1 + self.x2) / 2
        self.center_y = (self.y1 + self.y2) / 2

    def is_intersected(self, other):

        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)



