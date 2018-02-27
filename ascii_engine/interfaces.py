import curses


class CursesRender:
    def __init__(self):
        pass

    def render(self, screen):
        self.window = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.window.keypad(True)

        self._render_window(screen.render())

    def _render_window(self, pixels):
        window = self.window
        window.clear()

        for line_index, line in enumerate(pixels):
            for pixel_index, pixel in enumerate(line):
                window.addch(line_index, pixel_index, ord(pixel.get_char()))
        window.refresh()

    def stop(self):
        self.window.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()


curses_interface = CursesRender()
