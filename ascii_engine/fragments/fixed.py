"""
This module provide fragments to help you to define a fixed size for fragments
"""
from ascii_engine.fragments.base import BaseFragment
from ascii_engine.fragments.converter import StringToPixelLineFragment
from ascii_engine.pixel import Pixel


class FixedLineFragment(BaseFragment):
    """
    This fragment receive a line and block the line with the given width.

    Examples:

    >>> given_fragment = [Pixel('a'), Pixel('b')]
    >>> expected_fragment = given_fragment + [Pixel(' ')]
    >>> list(FixedLineFragment(given_fragment), 3) == expected_fragment
    ... True

    When the fragment is larger then the width its truncated.

    >>> given_fragment = [Pixel('a'), Pixel('b')]
    >>> expected_fragment = [Pixel('a')]
    >>> list(FixedLineFragment(given_fragment), 1) == expected_fragment
    ... True
    """

    def __init__(self, fragment, width):
        self.__width = width
        super().__init__(fragment[:self.__width])

    def __iter__(self):
        yield from super().__iter__()
        yield from self.__complete_with_blank_pixels()

    def __complete_with_blank_pixels(self):
        if len(self._get_fragment()) < self.__width:
            total_of_blank_chars = self.__width - len(self._get_fragment())
            fill_with = ' ' * total_of_blank_chars
            for pixel in StringToPixelLineFragment(fill_with):
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


class FixedMatrixFragment(BaseFragment):
    """
    This fragment receive a multi line and block the line with the given
    width and height.

    When the width is not defined it assumes the width of the largest line.

    When the height is not defined it assumes the fragment length.

    If the width or height is less than the fragment size, it truncates the
    fragment.
    """
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
                yield FixedLineFragment([], self.width)

    def _apply(self, line):
        return FixedLineFragment(line, self.width)

    def __len__(self):
        return self.height

    def __get_max_line_width(self, fragment):
        if not fragment:
            return 0
        bigger_line = max(fragment, key=len)
        return len(bigger_line)
