import pytest

from ascii_engine.elements.styles import colorize
from ascii_engine.elements.text import Text
from ascii_engine import colors
from ascii_engine.pixel import Pixel
from tests.asserts import assertPixelsAreEquals


RED = colors.RGB(255, 0, 0)


def test_text_has_pixel_representations():
    text = 'Hi\nBye'
    text_element = Text(text)
    assertPixelsAreEquals(text_element.to_pixels(), [
        [Pixel('H'), Pixel('i')],
        [Pixel('B'), Pixel('y'), Pixel('e')]
    ])


def test_text_validate_if_pixels_are_different():
    text = 'Hi\nBye'
    text_element = Text(text)
    with pytest.raises(AssertionError):
        assertPixelsAreEquals(text_element.to_pixels(), [
            [Pixel('H'), Pixel('i'), Pixel(' ')],
            [Pixel('B'), Pixel('i'), Pixel('e')]
        ])


def test_text_uses_the_given_foreground_color():
    text = 'Hi\nBye'
    text_element = Text(text)
    text_element.set_style([
        colorize(RED)
    ])

    for pixels in text_element.to_pixels():
        assert all([RED == pixel.get_foreground_color()
                    for pixel in pixels])


def test_text_uses_the_given_background_color():
    text = 'Hi\nBye'
    text_element = Text(text)

    text_element.set_style([
        colorize(background_color=RED)
    ])

    for pixels in text_element.to_pixels():
        assert all([RED == pixel.get_background_color()
                    for pixel in pixels])
