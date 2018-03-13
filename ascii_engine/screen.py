"""
This module provide the screen representation.

A screen is a where all to render elements should stay.
"""

from ascii_engine.pixel import BLANK_PIXEL
from ascii_engine.coord import Coord, CoordinatedElement


class Screen:
    """
    This is the screen where elements should be rendered given a coordinate.

    You can get a screen by calling the render_interface.create_empty_screen.

    >>> from ascii_engine.interfaces.curses_interface.render import (
    >>>     CursesRender
    >>> )
    >>> render = CursesRender()
    >>> render.create_empty_screen()
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.elements = []

    def add_element(self, element, coord=Coord(0, 0, 0)):
        """
        Add a element to the given position

        >>> screen = Screen(20, 10)
        >>> screen.add_element(Text("My Test"), Coord(0, 1))
        >>> screen.add_element(Text("My Test"), Coord(0, 1))
        """
        self.elements.append(CoordinatedElement(coord, element))

    def render(self):
        """
        This method is called by interface to get the pixels to be rendered
        in the screen.
        """
        fragment = _ScreenFragment(self.get_width(), self.get_height())
        for coord, element in self.elements:
            fragment.add_element(element, coord)
        return fragment.to_pixels()

    def get_width(self):
        """
        Return the screen width
        """
        return self.width

    def get_height(self):
        """
        Return the screen height
        """
        return self.height


class _ScreenFragment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = self._create_blank_screen()

    def add_element(self, element, coords):
        render_height = self.height - coords.y
        render_width = self.width - coords.x

        pixels = element.to_pixels()[:render_height]

        for line_index, line in enumerate(pixels):
            for pixel_index, pixel in enumerate(line[:render_width]):
                pixel_coords = coords.add_y(line_index).add_x(pixel_index)
                self.add_pixel(pixel_coords, pixel)

    def add_pixel(self, coords, pixel):
        self.screen[coords.get_y()][coords.get_x()] = pixel

    def to_pixels(self):
        return self.screen

    def _create_empty_line(self):
        return [BLANK_PIXEL] * self.width

    def _create_blank_screen(self):
        return [self._create_empty_line() for _ in range(self.height)]
