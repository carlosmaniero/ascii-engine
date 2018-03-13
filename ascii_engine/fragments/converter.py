"""
This module provide fragments that converts a set of types to pixel fragments.
"""
from ascii_engine.fragments.base import BaseFragment
from ascii_engine.pixel import Pixel


class StringToPixelLineFragment(BaseFragment):
    """
    Given a string it returns a list of pixels.

    >>> StringToPixelLineFragment("ab") == [Pixel('a'), Pixel('b')]
    ... True
    """
    def __init__(self, line):
        super().__init__(line)

    def _apply(self, char):
        return Pixel(char)


class StringToPixelMatrixFragment(BaseFragment):
    """
    Given a list of strings (remember a string is a list of char, because it
    that this class is called StringToPixelMatrixFragment) it returns a
    matrix of pixels.

    >>> StringToPixelMatrixFragment(["a", "b"]) == [[Pixel('a'), Pixel('b')]]
    """
    def __init__(self, lines):
        super().__init__(lines)

    def _apply(self, line):
        return StringToPixelLineFragment(
            line=line
        )
