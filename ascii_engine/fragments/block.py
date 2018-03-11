from ascii_engine.fragments.base import BaseFragment
from ascii_engine.fragments.converter import StringLineToPixelFragment
from ascii_engine.pixel import Pixel


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

    def _get_index(self, index):
        if index < len(self._get_fragment()):
            return self._apply(self._get_fragment()[index])
        elif index < self.height:
            return self._apply([])
        raise IndexError

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
