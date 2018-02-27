from collections import namedtuple


class Coords:
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def add_x(self, x):
        return Coords(self.x + x, self.y)

    def add_y(self, y):
        return Coords(self.x, self.y + y)


CoordinatedElement = namedtuple('CoordinatedElement', ['coords', 'element'])
