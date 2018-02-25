from ascii_engine.pixel import Pixel
from ascii_engine.colors import RED


def test_pixels_are_equals_whem_they_have_the_same_char():
    assert Pixel('a') == Pixel('a')
    assert Pixel('b') != Pixel('a')


def test_pixels_are_equals_when_they_have_the_same_foreground():
    assert Pixel('a', foreground_color=RED) == Pixel('a', foreground_color=RED)
    assert Pixel('a', foreground_color=RED) != Pixel('a')


def test_pixels_are_equals_when_they_have_the_same_background():
    assert Pixel('a', foreground_color=RED) == Pixel('a', foreground_color=RED)
    assert Pixel('a', foreground_color=RED) != Pixel('a')
