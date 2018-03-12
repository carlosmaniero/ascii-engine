import curses
from concurrent.futures import ThreadPoolExecutor
from ascii_engine.action import Action
from ascii_engine.screen import Screen


class CursesRender:
    def __init__(self, window):
        self.pairs = []
        self.window = window
        self.screen = None
        self.executor = ThreadPoolExecutor(max_workers=1)

    def render(self, screen):
        self.screen = screen
        self.executor.submit(self._render_window)

    def _render_window(self):
        pixels = self.screen.render()
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


def _create_keyboard_interface():
    stdscr = curses.newwin(0, 0, 0, 0)
    stdscr.keypad(True)
    return stdscr


def _create_main_window():
    window = curses.initscr()
    window.keypad(True)
    return window


class CursesInterface:
    def __init__(self):
        self.window = _create_main_window()
        self.render_interface = CursesRender(self.window)
        _configure_curses()

    def render(self, screen):
        self.render_interface.render(screen)

    def get_screen(self):
        height, width = self.window.getmaxyx()
        return Screen(width - 1, height)

    def stop(self):
        self.window.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()


class CursesKeyboardSubscription:
    def __init__(self, loop):
        self.interface = _create_keyboard_interface()
        self.loop = loop

    def listen_keyboard(self):
        char = self.interface.get_wch()
        if isinstance(char, str):
            return ord(char)
        return char

    async def get_action(self):
        keycode = await self.loop.run_in_executor(
            None,
            self.listen_keyboard
        )
        return Action('keypress', keycode)

    def has_next(self):
        return True
