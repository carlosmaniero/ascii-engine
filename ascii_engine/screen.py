from ascii_engine.pixel import BLANK_PIXEL
from ascii_engine.coords import Coords, CoordinatedElement


class Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.elements = []

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def add_element(self, element, coords=Coords(0, 0, 0)):
        self.elements.append(CoordinatedElement(coords, element))

    def render(self):
        fragment = ScreenFragment(self.get_width(), self.get_height())
        for coords, element in self.elements:
            fragment.add_element(element, coords)
        return fragment.get_screen()


class ScreenFragment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = self._create_blank_screen()

    def add_element(self, element, coords):
        for line_index, line in enumerate(element.get_pixels()):
            for pixel_index, pixel in enumerate(line):
                pixel_coords = coords.add_y(line_index).add_x(pixel_index)
                self.add_pixel(pixel_coords, pixel)

    def add_pixel(self, coords, pixel):
        try:
            self.screen[coords.get_y()][coords.get_x()] = pixel
        except IndexError:
            pass

    def get_screen(self):
        return self.screen

    def _create_empty_line(self):
        return [BLANK_PIXEL] * self.width

    def _create_blank_screen(self):
         return [self._create_empty_line() for _ in range(self.height)]
