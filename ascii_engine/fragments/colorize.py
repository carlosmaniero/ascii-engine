from ascii_engine.fragments.base import BaseFragment
from ascii_engine.pixel import Pixel


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
