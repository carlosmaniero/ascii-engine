import signal
from ascii_engine.interfaces import CursesInterface
from ascii_engine.screen import Screen
from ascii_engine.elements.text import Text
from ascii_engine.colors import RGB


if __name__ == '__main__':
    text_element = Text('Hello, World!')
    text_element.set_foreground_color(RGB(255, 0, 0))
    text_element.set_background_color(RGB(0, 0, 255))

    screen = Screen(20, 1)
    screen.add_element(text_element)
    curses_interface = CursesInterface()
    curses_interface.render(screen)

    try:
        signal.pause()
    except KeyboardInterrupt:
        curses_interface.stop()
