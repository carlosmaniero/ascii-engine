from ascii_engine.interfaces import curses_interface
from ascii_engine.screen import Screen
from ascii_engine.elements.text import Text
import signal



if __name__ == '__main__':
    text_element = Text('Hello, World!')
    screen = Screen(20, 1)
    screen.add_element(text_element)
    curses_interface.render(screen)

    try:
        signal.pause()
    except KeyboardInterrupt:
        curses_interface.stop()
