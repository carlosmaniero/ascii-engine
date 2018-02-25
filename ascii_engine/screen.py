from ascii_engine.colors import BLANK_COLOR


class Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def render(self):
        return [[BLANK_COLOR] * self.get_width()] * self.get_height()
