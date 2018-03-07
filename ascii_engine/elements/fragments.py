from ascii_engine.pixel import Pixel


class StringLineToPixelFragment:
    def __init__(self, line, foreground_color=None, background_color=None):
        self.__line = line
        self.__background_color = background_color
        self.__foreground_color = foreground_color

    def __iter__(self):
        for char in self.__line:
            yield self.__create_pixel(char)

    def __create_pixel(self, char):
        return Pixel(
            char=char,
            foreground_color=self.__foreground_color,
            background_color=self.__background_color
        )

    def __getitem__(self, item):
        if isinstance(item, slice):
            line = self.__line[item]
            return StringLineToPixelFragment(
                line,
                self.__foreground_color,
                self.__background_color
            )
        elif isinstance(item, int):
            return self.__create_pixel(self.__line[item])

        raise IndexError

    def __len__(self):
        return len(self.__line)


class MultiLineStringToPixelFragment:
    def __init__(self, lines, foreground_color=None, background_color=None):
        self.__lines = lines
        self.__background_color = background_color
        self.__foreground_color = foreground_color

    def __iter__(self):
        for line in self.__lines:
            yield self.__create_line_fragment(line)

    def __create_line_fragment(self, line):
        return StringLineToPixelFragment(
            line=line,
            background_color=self.__background_color,
            foreground_color=self.__foreground_color
        )

    def __getitem__(self, item):
        if isinstance(item, slice):
            lines = self.__lines[item]
            return MultiLineStringToPixelFragment(
                lines,
                self.__foreground_color,
                self.__background_color
            )
        elif isinstance(item, int):
            return self.__create_line_fragment(self.__lines[item])

        raise IndexError

    def __len__(self):
        return len(self.__lines)


class BlockPixelLineFragment:
    def __init__(self, line_fragment, width,
                 foreground_color=None, background_color=None):
        self.__line_fragment = line_fragment
        self.__width = width
        self.__background_color = background_color
        self.__foreground_color = foreground_color

    def __iter__(self):
        for pixel in self.__line_fragment[:self.__width]:
            yield self.__format_pixel(pixel)

        for pixel in self.__complete_line():
            yield pixel

    def __complete_line(self):
        if len(self.__line_fragment) < self.__width:
            total_of_blank_chars = self.__width - len(self.__line_fragment)
            fill_with = ' ' * total_of_blank_chars
            for pixel in StringLineToPixelFragment(
                    fill_with,
                    self.__foreground_color,
                    self.__background_color):
                yield pixel

    def __format_pixel(self, pixel):
        if pixel.get_background_color() is None:
            pixel = Pixel(
                pixel.get_char(),
                background_color=self.__background_color,
                foreground_color=pixel.get_foreground_color()
            )
        if pixel.get_foreground_color() is None:
            pixel = Pixel(
                pixel.get_char(),
                background_color=pixel.get_background_color(),
                foreground_color=self.__foreground_color
            )
        return pixel

    def __len__(self):
        return self.__width

    def __getitem__(self, item):
        if isinstance(item, slice):
            line_fragment = self.__line_fragment[item]

            return BlockPixelLineFragment(
                line_fragment,
                self.__calculate_slice_length(item),
                self.__foreground_color,
                self.__background_color
            )
        if isinstance(item, int):
            if item < self.__width:
                if item < len(self.__line_fragment):
                    return self.__format_pixel(self.__line_fragment[item])
                elif item < self.__width:
                    return Pixel(
                        char=' ',
                        foreground_color=self.__foreground_color,
                        background_color=self.__background_color
                    )

        raise IndexError

    def __calculate_slice_length(self, item):
        new_length = self.__width

        if item.stop is not None:
            new_length = min(item.stop, self.__width)

        if item.start is not None:
            new_length -= item.start

        if item.step is not None and new_length != 0:
            new_length = new_length // item.step + 1

        return new_length


class BlockPixelFragment:
    def __init__(self, lines_fragment, width=None, height=None):
        self.lines_fragment = lines_fragment
        self.width = width
        self.height = height

        if self.width is None:
            self.width = self.__get_max_line_width()

        if self.height is None:
            self.height = len(self.lines_fragment)

    def __iter__(self):
        for line in self.lines_fragment[:self.height]:
            yield BlockPixelLineFragment(line, self.width)

        if len(self.lines_fragment) < self.height:
            for _ in range(self.height - len(self.lines_fragment)):
                yield BlockPixelLineFragment([], self.width)

    def __len__(self):
        return self.height

    def __get_max_line_width(self):
        if len(self.lines_fragment) == 0:
            return 0
        bigger_line = max(self.lines_fragment, key=len)
        return len(bigger_line)


class ColorizeLinePixelsFragment:
    def __init__(self, line, foreground_color=None, background_color=None):
        self.__line = line
        self.__foreground_color = foreground_color
        self.__background_color = background_color

    def __iter__(self):
        for pixel in self.__line:
            yield self.__apply(pixel)

    def __apply(self, pixel):
        fg_color = pixel.get_foreground_color() or self.__foreground_color
        bg_color = pixel.get_background_color() or self.__background_color

        return Pixel(
            pixel.get_char(),
            foreground_color=fg_color,
            background_color=bg_color
        )

    def __len__(self):
        return len(self.__line)

    def __getitem__(self, item):
        if isinstance(item, slice):
            line = self.__line[item]
            return ColorizeLinePixelsFragment(
                line,
                self.__foreground_color,
                self.__background_color
            )
        elif isinstance(item, int):
            return self.__apply(self.__line[item])

        raise IndexError


class ColorizeMultiLinePixelsFragment:
    def __init__(self, lines, foreground_color=None, background_color=None):
        self.__lines = lines
        self.__foreground_color = foreground_color
        self.__background_color = background_color

    def __iter__(self):
        for line in self.__lines:
            yield self.__apply(line)

    def __apply(self, line):
        return ColorizeLinePixelsFragment(
            line,
            self.__foreground_color,
            self.__background_color
        )

    def __len__(self):
        return len(self.__lines)

    def __getitem__(self, item):
        if isinstance(item, slice):
            lines = self.__lines[item]
            return ColorizeMultiLinePixelsFragment(
                lines,
                self.__foreground_color,
                self.__background_color
            )
        if isinstance(item, int):
            return self.__apply(self.__lines[item])

        raise IndexError


class VerticalFragment:
    def __init__(self, fragments, width, height,
                 background_color, foreground_color):
        self.fragments = fragments
        self.width = width
        self.height = height
        self.background_color = background_color
        self.foreground_color = foreground_color

    def __iter__(self):
        total_of_lines = 0
        for fragment in self.fragments:
            for line_fragment in fragment:
                total_of_lines += 1
                yield BlockPixelLineFragment(
                    line_fragment,
                    self.width,
                    self.foreground_color,
                    self.background_color
                )

        if total_of_lines < self.height:
            for _ in range(self.height - total_of_lines):
                yield StringLineToPixelFragment(
                    ' ' * self.width,
                    self.foreground_color,
                    self.background_color
                )

    def __getitem__(self, item):
        return self.__iter__()
