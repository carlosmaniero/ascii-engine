import signal
from ascii_engine.interfaces import CursesInterface
from ascii_engine.screen import Screen
from ascii_engine.elements.text import Text
from ascii_engine.elements.layouts import VerticalLayout
from ascii_engine.colors import RGB


if __name__ == '__main__':
    curses_interface = CursesInterface()
    screen = curses_interface.get_screen()
    layout = VerticalLayout(screen.get_width(), screen.get_height())
    text_element = Text('Hello, World!')
    text_element.set_foreground_color(RGB(255, 0, 0))

    layout.add(text_element)
    layout.set_background_color(RGB(0, 0, 255))

    screen.add_element(layout)
    curses_interface.render(screen)

    try:
        signal.pause()
    except KeyboardInterrupt:
        curses_interface.stop()
