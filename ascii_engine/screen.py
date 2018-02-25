from ascii_engine.pixel import BLANK_PIXEL


class Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def render(self):
        return [[BLANK_PIXEL] * self.get_width()] * self.get_height()
