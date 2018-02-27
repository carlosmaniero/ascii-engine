from collections import namedtuple
from ascii_engine.term_colors import TERM_COLOR_MAP


class RGB(namedtuple('RGBBase', ['r', 'g', 'b'])):
    def get_term_color(self):
        diff = 255 ** 3
        best_choice = 0

        for term_color, rgb in TERM_COLOR_MAP:
            if rgb == self:
                return term_color

            r, g, b = rgb

            current_diff = abs(self.r - r) + abs(self.g - g) + abs(self.b - b)
            if current_diff < diff:
                best_choice = term_color
                diff = current_diff

        return best_choice
