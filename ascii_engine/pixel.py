"""
This module contains the a pixel representation

In this case a pixel is a character in the screen
"""


class Pixel:
    """
    A pixel is the small part in the screen. It is represented by a
    character with a foreground and background color.
    """
    def __init__(self, char, foreground_color=None, background_color=None):
        self.__char = char
        self.__foreground_color = foreground_color
        self.__background_color = background_color

    def get_foreground_color(self):
        """
        Get the pixel foreground color in a RGB format
        """
        return self.__foreground_color

    def get_background_color(self):
        """
        Get the pixel background color in a RGB format
        """
        return self.__background_color

    def get_char(self):
        """
        Get the pixel character.

        It returns a string of one character
        """
        return self.__char

    def __eq__(self, other):
        if not isinstance(other, Pixel):
            return False

        same_char = self.get_char() == other.get_char()
        same_fg = self.get_foreground_color() == other.get_foreground_color()
        same_bg = self.get_background_color() == other.get_background_color()
        return same_char and same_fg and same_bg

    def __repr__(self):
        return 'Pixel({})'.format(repr(self.__char))


BLANK_PIXEL = Pixel(' ')
