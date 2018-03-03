from ascii_engine.elements.text import Text
from ascii_engine.screen import Screen
from ascii_engine.interfaces import CursesInterface
from ascii_engine.app import App
from ascii_engine.colors import RGB


def draw(model):
    screen = Screen(140, 50)
    if model.get('last_key') is not None:
        text_element = Text('You typed: ' + chr(model['last_key']))
        text_element.set_background_color(RGB(155, 200, 45))
    else:
        text_element = Text('Hello, type anything!')
    screen.add_element(text_element)
    return screen


def update(action, model):
    if action.name == 'keypress':
        model['last_key'] = action.value
    return model


app = App(CursesInterface(), {}, draw, update)

try:
    app.start()
except:
    app.stop()
