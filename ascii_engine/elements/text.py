from ascii_engine.fragments.converter import MultiLineStringToPixelFragment
from ascii_engine.fragments.colorize import ColorizeMultiLinePixelsFragment
from ascii_engine.elements.base import BaseElement


class Text(BaseElement):
    def __init__(self, text):
        self.lines = text.split('\n')
        width = self._get_biggest_line_size()
        height = len(self.lines)
        super().__init__(width, height)

    def to_pixels(self):
        return ColorizeMultiLinePixelsFragment(
            MultiLineStringToPixelFragment(
                self.lines
            ),
            self.foreground_color,
            self.background_color
        )

    def _get_biggest_line_size(self):
        return max([len(line) for line in self.lines])
