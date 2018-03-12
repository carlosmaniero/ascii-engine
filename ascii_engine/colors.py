from collections import namedtuple
from ascii_engine.term_colors import TERM_COLOR_MAP


cached_term_colors = {}


class RGB(namedtuple('RGBBase', ['r', 'g', 'b'])):
    def calculate_term_color(self):
        if self._has_cache():
            return self._get_cached()

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

        cached_term_colors[self] = best_choice
        return best_choice

    def _has_cache(self):
        return self in cached_term_colors

    def _get_cached(self):
        return cached_term_colors[self]
