import pytest
from ascii_engine.fragments.converter import StringLineToPixelFragment
from ascii_engine.fragments.converter import MultiLineStringToPixelFragment
from ascii_engine.pixel import Pixel
from tests.fragments.utils import fragment_to_list


def test_that_line_fragment_renders_each_line_of_a_given_text():
    text = "Hello, World!"

    iterations = 0
    for char, pixel in zip(text, StringLineToPixelFragment(text)):
        assert Pixel(char) == pixel
        iterations += 1

    assert iterations == len(text)


def test_that_line_fragment_has_the_length_equals_the_given_text():
    text = "Hello, World!"

    assert len(StringLineToPixelFragment(text)) == len(text)


def test_that_line_fragment_deals_with_slices():
    text = "Hello, World"
    assert list(StringLineToPixelFragment(text)[:2]) == [Pixel('H'), Pixel('e')]
    assert list(StringLineToPixelFragment(text)[10:]) == [Pixel('l'), Pixel('d')]
    assert list(StringLineToPixelFragment(text)[2:4]) == [Pixel('l'), Pixel('l')]
    assert list(StringLineToPixelFragment(text)[::7]) == [Pixel('H'), Pixel('W')]


def test_that_line_fragment_deals_with_indexs():
    text = "Hello, World"
    assert StringLineToPixelFragment(text)[0] == Pixel('H')
    assert StringLineToPixelFragment(text)[7] == Pixel('W')


def test_that_line_fragment_raises_index_error_given_a_invalid_index():
    with pytest.raises(IndexError):
        StringLineToPixelFragment("Hi")[100]

    with pytest.raises(IndexError):
        StringLineToPixelFragment("Hi")["it is not a valid index"]

def test_that_mult_line_fragment_renders_each_line_of_a_given_text():
    lines = ["Hello", "World!"]

    for text_line, line in zip(lines, MultiLineStringToPixelFragment(lines)):
        assert list(line) == [Pixel(char) for char in text_line]


def test_that_multi_line_fragment_has_the_length_equals_the_given_text():
    lines = ["Hello", "World!"]

    assert len(MultiLineStringToPixelFragment(lines)) == len(lines)


def test_that_nulti_line_fragment_deals_with_slices():
    lines = ['ab', 'cd', 'ef']

    line_pixels = [
        [Pixel('a'), Pixel('b')],
        [Pixel('c'), Pixel('d')],
        [Pixel('e'), Pixel('f')]
    ]

    fragment = MultiLineStringToPixelFragment(lines)

    assert fragment_to_list(fragment[:2]) == line_pixels[:2]
    assert fragment_to_list(fragment[2:]) == line_pixels[2:]
    assert fragment_to_list(fragment[1:2]) == line_pixels[1:2]
    assert fragment_to_list(fragment[::2]) == line_pixels[::2]


def test_that_nulti_line_fragment_deals_with_indexes():
    lines = ['ab', 'cd', 'ef']

    line_pixels = [
        [Pixel('a'), Pixel('b')],
        [Pixel('c'), Pixel('d')],
        [Pixel('e'), Pixel('f')]
    ]

    fragment = MultiLineStringToPixelFragment(lines)

    for index in range(len(fragment)):
        assert list(fragment[index]) == line_pixels[index]


def test_that_mult_line_fragment_raises_index_error_given_a_invalid_index():
    with pytest.raises(IndexError):
        MultiLineStringToPixelFragment(["Hi"])[100]

    with pytest.raises(IndexError):
        MultiLineStringToPixelFragment(["Hi"])["it is not a valid index"]
