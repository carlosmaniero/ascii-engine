import curses


class CursesInterface:
    def __init__(self):
        self.pairs = []
        self.window = curses.initscr()

    def render(self, screen):
        curses.start_color()
        curses.noecho()
        curses.cbreak()
        self.window.keypad(True)

        self._render_window(screen.render())

    def _render_window(self, pixels):
        window = self.window
        window.clear()

        for line_index, line in enumerate(pixels):
            for pixel_index, pixel in enumerate(line):
                pair = self._get_pixel_pair(pixel)
                window.addstr(line_index, pixel_index, pixel.get_char(), pair)
        window.refresh()

    def _get_pixel_pair(self, pixel):
        term_fg = 231
        term_bg = 0

        if pixel.get_foreground_color():
            term_fg = pixel.get_foreground_color().get_term_color()

        if pixel.get_background_color():
            term_bg = pixel.get_background_color().get_term_color()

        try:
            pair_index = self.pairs.index((term_fg, term_bg)) + 1
        except ValueError:
            pair_index = len(self.pairs) + 1
            curses.init_pair(
                pair_index,
                term_fg,
                term_bg
            )
            self.pairs.append((term_fg, term_bg))
        return curses.color_pair(pair_index)

    def listen_keyboard(self):
        return self.window.getch()

    def stop(self):
        self.window.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()
