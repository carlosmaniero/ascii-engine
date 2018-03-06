from ascii_engine.pixel import Pixel


class LineFragment:
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
            return LineFragment(
                line,
                self.__foreground_color,
                self.__background_color
            )
        elif isinstance(item, int):
            return self.__create_pixel(self.__line[item])

        raise IndexError

    def __len__(self):
        return len(self.__line)


class ContainerizeLineFragment:
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
            for pixel in LineFragment(
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

            return ContainerizeLineFragment(
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
                    return Pixel(' ', self.__foreground_color, self.__background_color)

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


class MultiLineFragment:
    def __init__(self, lines, foreground_color=None, background_color=None):
        self.__lines = lines
        self.__background_color = background_color
        self.__foreground_color = foreground_color

    def __iter__(self):
        for line in self.__lines:
            yield self.__create_line_fragment(line)

    def __create_line_fragment(self, line):
        return LineFragment(
            line=line,
            background_color=self.__background_color,
            foreground_color=self.__foreground_color
        )

    def __getitem__(self, item):
        if isinstance(item, slice):
            lines = self.__lines[item]
            return MultiLineFragment(
                lines,
                self.__foreground_color,
                self.__background_color
            )
        elif isinstance(item, int):
            return self.__create_line_fragment(self.__lines[item])

        raise IndexError

    def __len__(self):
        return len(self.__lines)


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
                yield ContainerizeLineFragment(
                    line_fragment,
                    self.width,
                    self.foreground_color,
                    self.background_color
                )

        if total_of_lines < self.height:
            for _ in range(self.height - total_of_lines):
                yield LineFragment(
                    ' ' * self.width,
                    self.foreground_color,
                    self.background_color
                )

    def __getitem__(self, item):
        return self.to_pixels()
