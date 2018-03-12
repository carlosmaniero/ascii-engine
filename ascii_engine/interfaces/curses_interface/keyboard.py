import curses
from ascii_engine.action import Action


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
