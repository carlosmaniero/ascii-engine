"""
This module provide a Coord system that should be used in relative elements
like screen.
"""
from collections import namedtuple


class Coord:
    """
    A coordinate composed by (x, y and z)
    """
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y

    def get_x(self):
        """
        Get the x position
        """
        return self.x

    def get_y(self):
        """
        Get the y position
        """
        return self.y

    def add_x(self, delta_x):
        """
        Given a delta x, it will return a new Coord with the x equals
        x + delta_x
        """
        return Coord(self.x + delta_x, self.y)

    def add_y(self, delta_y):
        """
        Given a delta y, it will return a new Coord with the y equals
        y + delta_y
        """
        return Coord(self.x, self.y + delta_y)


CoordinatedElement = namedtuple('CoordinatedElement', ['coords', 'element'])
