import curses
from ascii_engine.action import Action
from ascii_engine.screen import Screen


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

    def listen_keyboard(self):
        return self.window.getch()

    def get_subscriptions(self, loop):
        return [CursesKeyboardSubscription(self, loop)]

    def get_screen(self):
        height, width = self.window.getmaxyx()
        return Screen(width, height)

    def stop(self):
        self.window.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()

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


class CursesKeyboardSubscription:
    def __init__(self, interface, loop):
        self.interface = interface
        self.loop = loop

    async def get_action(self):
        keycode = await self.loop.run_in_executor(
            None,
            self.interface.listen_keyboard
        )
        return Action('keypress', keycode)

    def has_next(self):
        return True
