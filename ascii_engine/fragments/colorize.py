"""
This module provide an easy way to colorize a pixel matrix.
"""

from ascii_engine.fragments.base import BaseFragment
from ascii_engine.pixel import Pixel


class ColorizeLineFragment(BaseFragment):
    """
    It colorize a line fragment with the defined foreground and background (
    both optional).

    It never change the pixel foreground or background just set when it is
    None.
    """
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


class ColorizeMatrixFragment(BaseFragment):
    """
    It colorize a matrix fragment with the defined foreground and background (
    both optional).

    It never change the pixel foreground or background just set when it is
    None.
    """
    def __init__(self, line, foreground_color=None, background_color=None):
        self.__foreground_color = foreground_color
        self.__background_color = background_color
        super().__init__(line)

    def _apply(self, line):
        return ColorizeLineFragment(
            line,
            self.__foreground_color,
            self.__background_color
        )

    def get_background_color(self):
        return self.__background_color

    def get_foreground_color(self):
        return self.__foreground_color
