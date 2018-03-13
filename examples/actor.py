from ascii_engine.elements.text import Text
from ascii_engine.app import create_app
from ascii_engine.colors import RGB
from ascii_engine.elements.layouts import VerticalLayout
from ascii_engine.interfaces.curses_interface.keyboard import (
    CursesKeyboardSubscription
)
from ascii_engine.interfaces.base.keyboard import KeypressEvent


header = Text('Hello! Type anything:')


def base_layout(width, height, elements):
    layout = VerticalLayout(width, height)
    layout.set_background_color(RGB(255, 0, 0))

    layout.add(header)

    for element in elements:
        layout.add(element)

    return layout


def types_counter(types):
    return Text('You typed ' + str(types) + ' key(s).')


def type_message(model):
    text_element = Text('You typed: ' + chr(model['last_key']))

    if model['special_key']:
        text_element = Text('You pressed a special key')

    text_element.set_background_color(RGB(155, 200, 45))
    return text_element


def draw(screen, model):
    elements = []

    if model.get('last_key'):
        elements.append(type_message(model))

    if model['types'] != 0:
        elements.append(types_counter(model['types']))

    layout = base_layout(
        screen.get_width(),
        screen.get_height(),
        elements
    )

    screen.add_element(layout)
    return screen


def actor(action, model):
    if isinstance(action, KeypressEvent):
        model['special_key'] = action.is_special()
        model['last_key'] = action.value
        model['types'] += 1
    return model


app = create_app({'types': 0}, draw, actor)

try:
    app.register_subscription(CursesKeyboardSubscription(app.get_loop()))
    app.start()
except KeyboardInterrupt:
    app.stop()
