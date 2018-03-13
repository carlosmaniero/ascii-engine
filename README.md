# ASCII ENGINE

[![Build Status](https://travis-ci.org/carlosmaniero/ascii-engine.svg?branch=master)](https://travis-ci.org/carlosmaniero/ascii-engine)
[![Coverage Status](https://coveralls.io/repos/github/carlosmaniero/ascii-engine/badge.svg?branch=master)](https://coveralls.io/github/carlosmaniero/ascii-engine?branch=master)

It is an engine to provide an easy way to make python `UI`s from the terminal using a event-based system.


A simple Hello World App:


# Examples

A simple hello world:

```python
from ascii_engine.app import create_app
from ascii_engine.elements.text import Text
from ascii_engine.colors import RGB


def draw(screen, state):
    text_element = Text('Hello, {}!'.format(state))
    text_element.set_foreground_color(RGB(255, 0, 0))
    screen.add_element(text_element)
    return screen


app = create_app('World', draw, actor=None)


if __name__ == '__main__':
    try:
        app.start()
    except KeyboardInterrupt:
        app.stop()

```

You should see it more in the examples path.