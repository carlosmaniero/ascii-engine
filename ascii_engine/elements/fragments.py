from ascii_engine.pixel import Pixel


class BaseFragment:
    def __init__(self, fragment):
        self._fragment = fragment

    def __iter__(self):
        for fragment_part in self._fragment:
            yield self._apply(fragment_part)

    def _apply(self, element_part):
        raise NotImplementedError

    def _get_new_instance_kwargs(self):
        return {}

    def _create_new_instance(self, new_fragment):
        fragment_class = type(self)
        return fragment_class(new_fragment, **self._get_new_instance_kwargs())

    def _get_slice(self, given_slice):
        new_fragment = self._fragment[given_slice]
        return self._create_new_instance(new_fragment)

    def _get_index(self, index):
        return self._apply(self._fragment[index])

    def __getitem__(self, item):
        if isinstance(item, slice):
            return self._get_slice(item)
        elif isinstance(item, int):
            return self._get_index(item)

        raise IndexError

    def __len__(self):
        return len(self._fragment)


class StringLineToPixelFragment(BaseFragment):
    def __init__(self, line):
        super().__init__(line)

    def _apply(self, char):
        return Pixel(char)


class MultiLineStringToPixelFragment(BaseFragment):
    def __init__(self, lines):
        super().__init__(lines)

    def _apply(self, line):
        return StringLineToPixelFragment(
            line=line
        )


class BlockPixelLineFragment(BaseFragment):
    def __init__(self, line_fragment, width):
        self.__width = width
        super().__init__(line_fragment[:self.__width])

    def __iter__(self):
        yield from super().__iter__()
        yield from self.__complete_with_blank_pixels()

    def __complete_with_blank_pixels(self):
        if len(self._fragment) < self.__width:
            total_of_blank_chars = self.__width - len(self._fragment)
            fill_with = ' ' * total_of_blank_chars
            for pixel in StringLineToPixelFragment(fill_with):
                yield pixel

    def _get_new_instance_kwargs(self):
        return {
            'width': self.__width,
        }

    def _apply(self, pixel):
        return pixel

    def __len__(self):
        return self.__width

    def _get_index(self, index):
        if index < self.__width:
            if index < len(self._fragment):
                return self._apply(self._fragment[index])
            elif index < self.__width:
                return Pixel(' ')

        raise IndexError

    def _get_slice(self, given_slice):
        line_fragment = self._fragment[given_slice]

        return BlockPixelLineFragment(
            line_fragment,
            self.__calculate_slice_length(given_slice)
        )

    def __calculate_slice_length(self, item):
        new_length = self.__width

        if item.stop is not None:
            new_length = min(item.stop, self.__width)

        if item.start is not None:
            new_length -= item.start

        if item.step is not None and new_length != 0:
            new_length = new_length // item.step + 1

        return new_length


class BlockPixelFragment(BaseFragment):
    def __init__(self, lines_fragment, width=None, height=None):
        self.width = width
        self.height = height

        if self.width is None:
            self.width = self.__get_max_line_width(lines_fragment)

        if self.height is None:
            self.height = len(lines_fragment)

        super().__init__(lines_fragment[:self.height])

    def __iter__(self):
        yield from super().__iter__()
        yield from self.__complete_lines()

    def __complete_lines(self):
        if len(self._fragment) < self.height:
            for _ in range(self.height - len(self._fragment)):
                yield BlockPixelLineFragment([], self.width)

    def _apply(self, line):
        return BlockPixelLineFragment(line, self.width)

    def __len__(self):
        return self.height

    def __get_max_line_width(self, fragment):
        if not fragment:
            return 0
        bigger_line = max(fragment, key=len)
        return len(bigger_line)


class ColorizeLinePixelsFragment(BaseFragment):
    def __init__(self, line, foreground_color=None, background_color=None):
        self.__foreground_color = foreground_color
        self.__background_color = background_color
        super().__init__(line)

    def _apply(self, pixel):
        fg_color = pixel.get_foreground_color() or self.__foreground_color
        bg_color = pixel.get_background_color() or self.__background_color

        return Pixel(
            pixel.get_char(),
            foreground_color=fg_color,
            background_color=bg_color
        )

    def _get_new_instance_kwargs(self):
        return dict(
            foreground_color=self.__foreground_color,
            background_color=self.__background_color
        )


class ColorizeMultiLinePixelsFragment(BaseFragment):
    def __init__(self, line, foreground_color=None, background_color=None):
        self.__foreground_color = foreground_color
        self.__background_color = background_color
        super().__init__(line)

    def _get_new_instance_kwargs(self):
        return dict(
            foreground_color=self.__foreground_color,
            background_color=self.__background_color
        )

    def _apply(self, line):
        return ColorizeLinePixelsFragment(
            line,
            self.__foreground_color,
            self.__background_color
        )


class VerticalFragment:
    def __init__(self, fragments, width, height):
        self.fragments = fragments
        self.width = width
        self.height = height

    def __iter__(self):
        total_of_lines = 0
        for fragment in self.fragments:
            for line_fragment in fragment:
                total_of_lines += 1
                yield BlockPixelLineFragment(
                    line_fragment,
                    self.width,
                )

        if total_of_lines < self.height:
            for _ in range(self.height - total_of_lines):
                yield StringLineToPixelFragment(
                    ' ' * self.width
                )

    def __getitem__(self, item):
        return self.__iter__()
