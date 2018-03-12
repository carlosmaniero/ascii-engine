from ascii_engine.elements.text import Text
from ascii_engine.app import create_app
from ascii_engine.colors import RGB
from ascii_engine.elements.layouts import VerticalLayout
from ascii_engine.interfaces import CursesKeyboardSubscription


def draw(screen, model):
    layout = VerticalLayout(
        screen.get_width(),
        screen.get_height()
    )

    header = Text('Hello! Type anything:')
    layout.add(header)

    if model.get('last_key') is not None:
        text_element = Text('You typed: ' + chr(model['last_key']))
        text_element.set_background_color(RGB(155, 200, 45))
        layout.add(text_element)

    show_counter = Text('You typed ' + str(model['types']) + ' key(s).')
    layout.add(show_counter)

    layout.set_background_color(RGB(255, 0, 0))
    screen.add_element(layout)
    return screen


def update(action, model):
    if action.name == 'keypress':
        model['last_key'] = action.value
        model['types'] += 1
    return model


app = create_app({'types': 0}, draw, update)

try:
    app.register_subscription(CursesKeyboardSubscription(app.get_loop()))
    app.start()
except KeyboardInterrupt:
    app.stop()
