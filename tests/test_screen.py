from ascii_engine.screen import Screen
from ascii_engine.colors import BLANK_COLOR


def test_that_screen_returns_the_given_size():
    screen = Screen(80, 23)
    width = screen.get_width()
    height = screen.get_height()

    assert width == 80
    assert height == 23


def test_that_screen_render_returns_an_empty_matrix_of_colors():
    screen = Screen(3, 2)
    rendered = screen.render()
    assert [
               [BLANK_COLOR, BLANK_COLOR, BLANK_COLOR],
               [BLANK_COLOR, BLANK_COLOR, BLANK_COLOR]
           ] == rendered
