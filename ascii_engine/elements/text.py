from ascii_engine.elements.fragments import ElementFragment
from ascii_engine.elements.base import BaseElement
from ascii_engine.dimensions import Natural


class Text(BaseElement):
    def __init__(self, text):
        self.lines = text.split('\n')
        width = self._get_biggest_line_size()
        height = len(self.lines)
        super().__init__(Natural(width), Natural(height))

    def get_pixels(self):
        return ElementFragment(
            self.lines,
            self.get_width().value,
            self.get_height().value,
            self.background_color,
            self.foreground_color
        )

    def _get_biggest_line_size(self):
        return max([len(line) for line in self.lines])
