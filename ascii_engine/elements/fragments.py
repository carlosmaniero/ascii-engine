from ascii_engine.pixel import Pixel


class LineFragment:
    def __init__(self, line, width, background_color, foreground_color):
        self.line = line
        self.width = width
        self.background_color = background_color
        self.foreground_color = foreground_color

    def get_pixels(self):
        for char in self._normalize_line():
            yield self._create_pixel(char)

    def _normalize_line(self):
        total_of_blank_chars = self.width - len(self.line)
        blank_chars = ' ' * total_of_blank_chars

        return self.line + blank_chars

    def _create_pixel(self, char):
        return Pixel(
            char=char,
            foreground_color=self.foreground_color,
            background_color=self.background_color
        )

    def __iter__(self):
        return self.get_pixels()


class ElementFragment:
    def __init__(self, lines, width, height,
                 background_color, foreground_color):
        self.lines = lines
        self.width = width
        self.height = height
        self.background_color = background_color
        self.foreground_color = foreground_color

    def get_pixels(self):
        for line in self.lines:
            line_fragment = LineFragment(
                line,
                self.width,
                self.background_color,
                self.foreground_color
            )
            yield line_fragment

    def __iter__(self):
        return iter(self.get_pixels())

    def __eq__(self, other):
        other_list = list(other)
        for other_line, line in zip(other_list, self.get_pixels()):
            if other_line != list(line):
                return False
        return True
