"""
This module provides an easy way to align fragments on screen.
"""

from ascii_engine.fragments.base import BaseFragment
from ascii_engine.fragments.fixed import FixedMatrixFragment
from ascii_engine.fragments.utils import get_max_line_width
from ascii_engine.pixel import Pixel


class AlignRightLineFragment(BaseFragment):
    """
    Align center a line.

    >>> given_fragment = [Pixel('a'), Pixel('b')]
    >>> expected_fragment = [Pixel(' '), Pixel(' '), Pixel('a'), Pixel('b')]
    >>> list(AlignRightLineFragment(given_fragment), 4) == expected_fragment
    ... True
    """
    def __init__(self, fragment, width):
        super().__init__(fragment, width)
        self.__start_pixel = max(width - len(self.get_fragment()), 0)

    def __iter__(self):
        for index in range(len(self)):
            yield self._get_index(index)

    def _get_index(self, index):
        if index < self.__start_pixel:
            return Pixel(' ')
        else:
            return self.get_fragment()[index - self.__start_pixel]


class AlignMatrixRightLineFragment(BaseFragment):
    """
    Given a Matrix Fragment it will put each line of the matrix to the right
    """
    def __init__(self, fragment, width=None):
        self.__width = width

        if not width:
            self.__width = get_max_line_width(fragment)
        super().__init__(fragment)

    def _apply(self, element_part):
        return AlignRightLineFragment(element_part, self.__width)


class AlignCenterLineFragment(BaseFragment):
    """
    Align center a line.

    >>> given_fragment = [Pixel('a'), Pixel('b')]
    >>> expected_fragment = [Pixel(' '), Pixel('a'), Pixel('b'), Pixel(' ')]
    >>> list(AlignCenterLineFragment(given_fragment), 4) == expected_fragment
    ... True

    If the given width is lower than the fragment it keep align left.

    >>> given_fragment = [Pixel('a'), Pixel('b')]
    >>> list(AlignCenterLineFragment(given_fragment), 1) == [Pixel('a')]
    ... True
    """
    def __init__(self, fragment, width):
        super().__init__(fragment, width)

        self.__start_pixel = (width - len(fragment)) // 2
        self.__end_pixel = self.__start_pixel + len(fragment) - 1

        if width <= len(fragment):
            self.__start_pixel = 0
            self.__end_pixel = len(fragment)

    def __iter__(self):
        for index in range(len(self)):
            yield self._get_index(index)

    def _get_index(self, index):
        if index < self.__start_pixel:
            return Pixel(' ')
        elif index > self.__end_pixel:
            return Pixel(' ')
        else:
            return self.get_fragment()[index - self.__start_pixel]


class AlignMatrixCenterLineFragment(BaseFragment):
    """
    Given a Matrix Fragment it will put each line of the matrix to the center
    """
    def __init__(self, fragment, width=None):
        self.__width = width
        if not width:
            self.__width = get_max_line_width(fragment)
        super().__init__(fragment)

    def _apply(self, element_part):
        return AlignCenterLineFragment(element_part, self.__width)

    def get_width(self):
        return self.__width


class AlignMatrixBottomFragment(FixedMatrixFragment):
    def __init__(self, lines_fragment, height):
        super().__init__(lines_fragment, height=height)
        self.__start_fragment = max(
            self.get_height() - len(self.get_fragment()),
            0
        )

    def _get_index(self, index):
        if index < self.__start_fragment:
            return self._apply([])
        return self._apply(self.get_fragment()[index - self.__start_fragment])


class AlignMatrixMiddleFragment(FixedMatrixFragment):
    def __init__(self, lines_fragment, height):
        super().__init__(lines_fragment, height=height)

        self.__start_pixel = (height - len(lines_fragment)) // 2
        self.__end_pixel = self.__start_pixel + len(lines_fragment) - 1

        if height <= len(lines_fragment):
            self.__start_pixel = 0
            self.__end_pixel = len(lines_fragment)

    def _get_index(self, index):
        if self.__start_pixel <= index <= self.__end_pixel:
            return self._apply(self.get_fragment()[
               index - self.__start_pixel
            ])
        return self._apply([])
