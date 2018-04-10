from collections import namedtuple

from ascii_engine.elements.text import Text


class InputField(Text):
    State = namedtuple('State', ['value', 'is_focused', 'position'])

    def __init__(self, state: State):
        super().__init__(state.value)
