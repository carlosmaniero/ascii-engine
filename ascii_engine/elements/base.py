class BaseElement:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.background_color = None
        self.foreground_color = None

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def set_foreground_color(self, color):
        self.foreground_color = color

    def set_background_color(self, color):
        self.background_color = color
