"""
This module provide fragments to help you to define a fixed size for fragments
"""
from ascii_engine.fragments.base import BaseFragment
from ascii_engine.fragments.converter import StringToPixelLineFragment
from ascii_engine.fragments.utils import get_max_line_width
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
        super().__init__(fragment[:width], width)

    def _get_index(self, index):
        if index < len(self):
            if index < len(self._get_fragment()):
                return self._apply(self._get_fragment()[index])
            elif index < len(self):
                return Pixel(' ')


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
        self.__width = width

        if self.__width is None:
            self.__width = get_max_line_width(lines_fragment)

        if height is None:
            height = len(lines_fragment)

        super().__init__(lines_fragment[:height], height)

    def _get_index(self, index):
        if index < len(self._get_fragment()):
            return self._apply(self._get_fragment()[index])
        elif index < len(self):
            return self._apply([])

    def _apply(self, line):
        return FixedLineFragment(line, self.__width)
