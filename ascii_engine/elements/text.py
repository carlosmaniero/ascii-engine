from ascii_engine.pixel import Pixel


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
        default_pixel = self._create_pixel(' ')
        pixels = [[default_pixel] * self.get_width()
                  for _ in range(self.get_height())]

        for line_index, line in enumerate(self.lines):
            for char_index, char in enumerate(line):
                pixels[line_index][char_index] = self._create_pixel(char)

        return pixels

    def _create_pixel(self, char):
        return Pixel(
            char=char,
            foreground_color=self.foreground_color,
            background_color=self.background_color
        )
