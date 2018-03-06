from ascii_engine.pixel import Pixel


class LineFragment:
    def __init__(self, line, background_color, foreground_color):
        self.line = line
        self.width = len(line)
        self.background_color = background_color
        self.foreground_color = foreground_color

    def to_pixels(self):
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
        return self.to_pixels()

    def __getitem__(self, item):
        if isinstance(item, slice):
            line = self.line[item]
            return LineFragment(
                line,
                self.background_color,
                self.foreground_color
            )

    def __repr__(self):
        return repr([repr(pixel) for pixel in self.to_pixels()])


class ElementFragment:
    def __init__(self, lines, width, height,
                 background_color, foreground_color):
        self.lines = lines
        self.width = width
        self.height = height
        self.background_color = background_color
        self.foreground_color = foreground_color

    def to_pixels(self):
        for line in self.lines:
            line_fragment = LineFragment(
                line,
                self.background_color,
                self.foreground_color
            )
            yield line_fragment

    def __iter__(self):
        return self.to_pixels()

    def __getitem__(self, item):
        if isinstance(item, slice):
            lines = self.lines[item]
            return ElementFragment(
                lines,
                self.width,
                len(lines),
                self.background_color,
                self.foreground_color
            )


class ContainerLineFragment:
    def __init__(self, line_fragment, width,
                 background_color, foreground_color):
        self.line_fragment = line_fragment
        self.width = width
        self.background_color = background_color
        self.foreground_color = foreground_color

    def to_pixels(self):
        for pixel in self.line_fragment[:self.width]:
            if pixel.get_background_color() is None:
                pixel = Pixel(
                    pixel.get_char(),
                    background_color=self.background_color,
                    foreground_color=pixel.get_foreground_color()
                )
            yield pixel

        if self.line_fragment.width < self.width:
            total_of_blank_chars = self.width - self.line_fragment.width
            fill_with = ' ' * total_of_blank_chars
            for pixel in LineFragment(
                    fill_with,
                    self.background_color,
                    self.foreground_color):
                yield pixel

    def __iter__(self):
        return self.to_pixels()

    def __getitem__(self, item):
        return self.to_pixels()


class VerticalFragment:
    def __init__(self, fragments, width, height,
                 background_color, foreground_color):
        self.fragments = fragments
        self.width = width
        self.height = height
        self.background_color = background_color
        self.foreground_color = foreground_color

    def to_pixels(self):
        total_of_lines = 0
        for fragment in self.fragments:
            for line_fragment in fragment:
                total_of_lines += 1
                yield ContainerLineFragment(
                    line_fragment,
                    self.width,
                    self.background_color,
                    self.foreground_color
                )

        if total_of_lines < self.height:
            for _ in range(self.height - total_of_lines):
                yield LineFragment(
                    ' ' * self.width,
                    self.background_color,
                    self.foreground_color
                )

    def __iter__(self):
        return self.to_pixels()

    def __getitem__(self, item):
        return self.to_pixels()
