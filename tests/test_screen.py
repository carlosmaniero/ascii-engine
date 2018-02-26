from ascii_engine.screen import Screen
from ascii_engine.pixel import BLANK_PIXEL, Pixel
from ascii_engine.coords import Coords
from ascii_engine.elements.text import Text


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
               [BLANK_PIXEL, BLANK_PIXEL, BLANK_PIXEL],
               [BLANK_PIXEL, BLANK_PIXEL, BLANK_PIXEL]
           ] == rendered

def test_that_screen_render_a_given_element():
    screen = Screen(5, 1)
    text_element = Text('Hello')
    screen.add_element(text_element)
    assert screen.render() == text_element.get_pixels()


def test_that_screen_do_element_overlap():
    screen = Screen(5, 1)
    text_element1 = Text('Hello')
    text_element2 = Text('Bye')
    screen.add_element(text_element1)
    screen.add_element(text_element2)
    assert screen.render() == Text('Byelo').get_pixels()


def test_that_screen_render_elements_given_an_possition():
    screen = Screen(5, 2)
    text_element1 = Text('Hello')
    text_element2 = Text('Bye')
    screen.add_element(text_element1)
    screen.add_element(text_element2, coords=Coords(0, 1))
    assert screen.render() == Text('Hello\nBye').get_pixels()


def test_that_screen_pixels_out_of_screen():
    screen = Screen(5, 1)
    screen.add_element(Text('Hello'), Coords(1, 0))
    screen.render() == Text(' Hell').get_pixels()
