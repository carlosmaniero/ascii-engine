from ascii_engine.fragments.converter import StringToPixelMatrixFragment
from ascii_engine.elements.base import BaseElement


class Text(BaseElement):
    def __init__(self, text):
        self.lines = text.split('\n')
        super().__init__()

    def create_fragment(self):
        return StringToPixelMatrixFragment(
            self.lines
        )
