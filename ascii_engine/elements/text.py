from ascii_engine.elements.fragments import ElementFragment


class Text:
    def __init__(self, text):
        self.lines = text.split('\n')
        self.width = self._get_biggest_line_size()
        self.height = len(self.lines)
        self.foreground_color = None
        self.background_color = None

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def _get_biggest_line_size(self):
        return max([len(line) for line in self.lines])

    def set_foreground_color(self, color):
        self.foreground_color = color

    def set_background_color(self, color):
        self.background_color = color

    def get_pixels(self):
        return ElementFragment(
            self.lines,
            self.get_width(),
            self.get_height(),
            self.background_color,
            self.foreground_color
        )
