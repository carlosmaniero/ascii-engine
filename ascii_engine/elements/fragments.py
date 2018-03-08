from ascii_engine.pixel import Pixel


class BaseFragment:
    def __init__(self, fragment):
        self.__fragment = fragment

    def __iter__(self):
        for fragment_part in self._get_fragment():
            yield self._apply(fragment_part)

    def _apply(self, element_part):
        raise NotImplementedError

    def _get_fragment(self):
        return self.__fragment

    def _get_slice(self, given_slice):
        return SliceIterableFragment(
            self,
            given_slice.start,
            given_slice.stop,
            given_slice.step
        )

    def _get_index(self, index):
        return self._apply(self._get_fragment()[index])

    def __getitem__(self, item):
        if isinstance(item, slice):
            return self._get_slice(item)
        elif isinstance(item, int):
            return self._get_index(item)

        raise IndexError

    def __len__(self):
        return len(self._get_fragment())


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
        if len(self._get_fragment()) < self.__width:
            total_of_blank_chars = self.__width - len(self._get_fragment())
            fill_with = ' ' * total_of_blank_chars
            for pixel in StringLineToPixelFragment(fill_with):
                yield pixel

    def _apply(self, pixel):
        return pixel

    def __len__(self):
        return self.__width

    def _get_index(self, index):
        if index < self.__width:
            if index < len(self._get_fragment()):
                return self._apply(self._get_fragment()[index])
            elif index < self.__width:
                return Pixel(' ')

        raise IndexError


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
        if len(self._get_fragment()) < self.height:
            for _ in range(self.height - len(self._get_fragment())):
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


class ColorizeMultiLinePixelsFragment(BaseFragment):
    def __init__(self, line, foreground_color=None, background_color=None):
        self.__foreground_color = foreground_color
        self.__background_color = background_color
        super().__init__(line)

    def _apply(self, line):
        return ColorizeLinePixelsFragment(
            line,
            self.__foreground_color,
            self.__background_color
        )


class SliceIterableFragment(BaseFragment):
    def __init__(self, fragment, start, stop, step):
        self.__start = start
        self.__stop = stop
        self.__step = step
        super().__init__(fragment)

    def _calculate_stop(self):
        stop = self.__stop or len(self._get_fragment())
        return min(len(self._get_fragment()), stop)

    def _calculate_start(self):
        return self.__start or 0

    def _calculate_step(self):
        return self.__step or 1

    def _get_range(self):
        return range(
            self._calculate_start(),
            self._calculate_stop(),
            self._calculate_step()
        )

    def _get_index(self, index):
        slice_index = self._get_range()[index]
        return self._get_fragment()[slice_index]

    def __iter__(self):
        for index in self._get_range():
            yield self._get_fragment()[index]

    def __len__(self):
        return len(self._get_range())


class JoinMultiLineVerticallyFragment(BaseFragment):
    def __init__(self, *fragments):
        super().__init__(fragments)

    def __iter__(self):
        for fragment in self._get_fragment():
            for line in fragment:
                yield line

    def _get_index(self, index):
        current_lenght = 0
        for fragment in self._get_fragment():
            if current_lenght + len(fragment) > index:
                return fragment[index - current_lenght]
            current_lenght += len(fragment)

        raise IndexError

    def __len__(self):
        return sum(map(len, self._get_fragment()))
