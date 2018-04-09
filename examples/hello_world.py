from ascii_engine.app import create_app
from ascii_engine.elements.styles import colorize, display
from ascii_engine.elements.text import Text
from ascii_engine.colors import RGB


def draw(screen, state):
    text_element = Text('Hello, {}!'.format(state))
    text_element.set_style([
        colorize(RGB(255, 0, 0)),
        display(horizontal_size=screen.get_width(), horizontal_align='center')
    ])
    screen.add_element(text_element)
    return screen


app = create_app('World', draw, actor=None)


if __name__ == '__main__':
    try:
        app.start()
    except KeyboardInterrupt:
        app.stop()
