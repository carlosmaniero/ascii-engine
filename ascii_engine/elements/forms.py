import functools
from collections import namedtuple

from ascii_engine.elements.text import Text
from ascii_engine.fragments.base import BaseFragment
from ascii_engine.pixel import Pixel


class CursorLineFragment(BaseFragment):
    def __init__(self, fragment, position, foreground_color, background_color):
        super().__init__(fragment)
        self.__position = position
        self.__foreground_color = foreground_color
        self.__background_color = background_color

    def _get_index(self, index):
        if self.__position == index:
            char = super()._get_index(index).get_char()
            return Pixel(
                char,
                self.__foreground_color,
                self.__background_color
            )
        return super()._get_index(index)


class CursorFragment(BaseFragment):
    def __init__(self, fragment, position, foreground_color, background_color):
        super().__init__(fragment)
        self.__position = position
        self.__foreground_color = foreground_color
        self.__background_color = background_color

    def _apply(self, element_part):
        return CursorLineFragment(element_part, self.__position,
                                  self.__foreground_color,
                                  self.__background_color)


class InputField(Text):
    State = namedtuple('State', ['value', 'is_focused', 'position'])

    def __init__(self, state, cursor_foreground=None, cursor_background=None):
        super().__init__(state.value)
        self.state = state
        self.__focus_style = []
        self.__placeholder_style = []
        self.__cursor_background = cursor_background
        self.__cursor_foreground = cursor_foreground

    def set_focus_style(self, styles):
        self.__focus_style = styles

    def set_placeholder_style(self, styles):
        self.__placeholder_style = styles

    def create_fragment(self):
        if self.state.is_focused:
            return CursorFragment(
                super().create_fragment(),
                self.state.position,
                self.__cursor_foreground,
                self.__cursor_background
            )
        return super().create_fragment()

    def to_pixels(self):
        if self.state.is_focused and self.__focus_style:
            return functools.reduce(
                lambda current, style: style(current),
                self.__focus_style,
                self.create_fragment()
            )
        if self.state.value == '' and self.__placeholder_style:
            return functools.reduce(
                lambda current, style: style(current),
                self.__placeholder_style,
                self.create_fragment()
            )
        return super().to_pixels()
