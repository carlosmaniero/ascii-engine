from ascii_engine.pixel import Pixel
from ascii_engine.colors import RGB


RED = RGB(255, 0, 0)


def test_pixels_are_equals_whem_they_have_the_same_char():
    assert Pixel('a') == Pixel('a')
    assert Pixel('b') != Pixel('a')


def test_pixels_are_equals_when_they_have_the_same_foreground():
    assert Pixel('a', foreground_color=RED) == Pixel('a', foreground_color=RED)
    assert Pixel('a', foreground_color=RED) != Pixel('a')


def test_pixels_are_equals_when_they_have_the_same_background():
    assert Pixel('a', background_color=RED) == Pixel('a', background_color=RED)
    assert Pixel('a', background_color=RED) != Pixel('a')


def test_pixel_is_different_of_anything_that_is_not_a_pixel():
    assert Pixel('a') != 'a'
    assert Pixel('1') != 1


def test_that_pixel_repl_returns_the_class_name_and_the_given_char():
    assert repr(Pixel('a')) == "Pixel('a')"
