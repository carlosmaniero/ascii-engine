from ascii_engine.elements.text import Text
from ascii_engine.dimensions import Natural
from ascii_engine import colors
from ascii_engine.pixel import Pixel


RED = colors.RGB(255, 0, 0)


def test_text_has_the_width_equals_the_text_size():
    text = 'My great text'
    text_element = Text(text)
    assert text_element.get_width() == Natural(13)


def test_text_has_the_height_equals_the_number_of_lines():
    text = 'My\ngreat\ntext'
    text_element = Text(text)
    assert text_element.get_height() == Natural(3)


def test_text_has_the_width_equals_the_length_of_the_biggest_line():
    text = 'My\ngreat\ntext\n!'
    text_element = Text(text)
    assert text_element.get_width() == Natural(5)
    assert text_element.get_height() == Natural(4)


def test_text_has_pixel_representations():
    text = 'Hi\nBye'
    text_element = Text(text)
    assert text_element.get_pixels() == [
        [Pixel('H'), Pixel('i'), Pixel(' ')],
        [Pixel('B'), Pixel('y'), Pixel('e')]
    ]

def test_text_validate_if_pixels_are_different():
    text = 'Hi\nBye'
    text_element = Text(text)
    assert text_element.get_pixels() != [
        [Pixel('H'), Pixel('i'), Pixel(' ')],
        [Pixel('B'), Pixel('i'), Pixel('e')]
    ]

def test_text_uses_the_given_foreground_color():
    text = 'Hi\nBye'
    text_element = Text(text)
    text_element.set_foreground_color(RED)

    for pixels in text_element.get_pixels():
        assert all([RED == pixel.get_foreground_color()
                    for pixel in pixels])

def test_text_uses_the_given_background_color():
    text = 'Hi\nBye'
    text_element = Text(text)
    text_element.set_background_color(RED)

    for pixels in text_element.get_pixels():
        assert all([RED == pixel.get_background_color()
                    for pixel in pixels])
