import functools
from collections import namedtuple

from ascii_engine.elements.text import Text


class InputField(Text):
    State = namedtuple('State', ['value', 'is_focused', 'position'])

    def __init__(self, state: State):
        super().__init__(state.value)
        self.state = state
        self.__focus_style = []
        self.__placeholder_style = []

    def set_focus_style(self, styles):
        self.__focus_style = styles

    def set_placeholder_style(self, styles):
        self.__placeholder_style = styles

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
