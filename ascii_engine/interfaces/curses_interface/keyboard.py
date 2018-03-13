import curses
from ascii_engine.interfaces.base.keyboard import KeypressEvent


def _create_keyboard_interface():
    stdscr = curses.newwin(0, 0, 0, 0)
    stdscr.keypad(True)
    return stdscr


class CursesKeyboardSubscription:
    def __init__(self, loop):
        self.interface = _create_keyboard_interface()
        self.loop = loop

    def listen_keyboard(self):
        char = self.interface.get_wch()
        if isinstance(char, str):
            return KeypressEvent(ord(char))
        return KeypressEvent(char, True)

    async def listen(self):
        return await self.loop.run_in_executor(
            None,
            self.listen_keyboard
        )

    def has_next(self):
        return True
