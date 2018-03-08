from ascii_engine.fragments.base import BaseFragment
from ascii_engine.pixel import Pixel


class StringLineToPixelFragment(BaseFragment):
    def __init__(self, line):
        super().__init__(line)

    def _apply(self, char):
        return Pixel(char)


class MultiLineStringToPixelFragment(BaseFragment):
    def __init__(self, lines):
        super().__init__(lines)

    def _apply(self, line):
        return StringLineToPixelFragment(
            line=line
        )
