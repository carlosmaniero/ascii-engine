import curses
from concurrent.futures import ThreadPoolExecutor
from ascii_engine.screen import Screen


class CursesRender:
    """
    The render interface for curses application.
    """
    def __init__(self):
        self.window = _create_main_window()
        self.render_interface = CursesRenderExecutor(self.window)
        _configure_curses()

    def render(self, screen):
        """
        The render function receive a screen to be rendered and render it on
        screen.
        """
        self.render_interface.render(screen)

    def create_empty_screen(self):
        """
        Create a empty screen with the screen (terminal) Size.
        """
        height, width = self.window.getmaxyx()
        return Screen(width - 1, height)

    def stop(self):
        """
        This function resets the terminal to the "normal" state
        """
        self.window.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()


class CursesRenderExecutor:
    """
    A thread-safe way to render using the curses library.

    This class has a thread pool with one worker to prevent screen buffer.
    There is no grantee that all screens will be rendered. But the last
    send to the render function will.
    """

    def __init__(self, window):
        self.pairs = []
        self.window = window
        self.screen = None
        self.last_screen = None
        self.pool = ThreadPoolExecutor(max_workers=1)

    def render(self, screen):
        """
        Define a screen to be rendered
        """
        self.screen = screen
        self.pool.submit(self._check_for_next_render)

    def _render_window(self):
        """
        This internal method interacts with the curses library to render the
        screen.
        """
        pixels = self.screen.render()
        window = self.window
        window.clear()

        for line_index, line in enumerate(pixels):
            for pixel_index, pixel in enumerate(line):
                pair = self._get_pixel_pair(pixel)
                window.addstr(line_index, pixel_index, pixel.get_char(), pair)
        window.refresh()
        self.last_screen = self.screen

    def _check_for_next_render(self):
        """
        This method prevent unnecessary render by check if the last screen
        rendered
        is the current screen.

        It's necessary because each call to render generates a screen re-render
        """
        if self.screen != self.last_screen:
            self._render_window()

    def _get_pixel_pair(self, pixel):
        """
        Given a pixel it return a curses color_pair.

        It is necessary to stylizes and colorize the pixel.
        """
        term_fg = 231
        term_bg = 0

        if pixel.get_foreground_color():
            term_fg = pixel.get_foreground_color().calculate_term_color()

        if pixel.get_background_color():
            term_bg = pixel.get_background_color().calculate_term_color()

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


def _configure_curses():
    curses.start_color()
    curses.noecho()
    curses.cbreak()


def _create_main_window():
    window = curses.initscr()
    window.keypad(True)
    return window
