import pytest
from ascii_engine.fragments.colorize import ColorizeLineFragment
from ascii_engine.fragments.colorize import ColorizeMatrixFragment
from ascii_engine.colors import RGB
from ascii_engine.pixel import Pixel
from tests.fragments.utils import fragment_to_list


def test_that_colorized_line_pixels_set_the_foreground_of_a_given_line():
    text = "Hello, World"

    given_color = RGB(1, 2, 3)
    given_line_pixels = [Pixel(char) for char in text]

    fragment = ColorizeLineFragment(
        given_line_pixels,
        foreground_color=given_color
    )

    expected_line_pixels = [
        Pixel(char, foreground_color=given_color) for char in text
    ]
    assert fragment_to_list(fragment) == expected_line_pixels


def test_that_colorized_line_pixels_set_the_background_of_a_given_line():
    text = "Hello, World"

    given_color = RGB(1, 2, 3)
    given_line_pixels = [Pixel(char) for char in text]

    fragment = ColorizeLineFragment(
        given_line_pixels,
        background_color=given_color
    )

    expected_line_pixels = [
        Pixel(
            char=char,
            background_color=given_color
        ) for char in text
    ]

    assert fragment_to_list(fragment) == expected_line_pixels


def test_that_colorized_line_pixels_does_not_replace_pixels_background_color():
    given_background_color = RGB(1, 2, 3)
    given_colorized_line = [
        Pixel(
            char=str(i),
            background_color=given_background_color
        ) for i in range(3)
    ]

    given_non_color_line = [Pixel(str(i)) for i in range(3)]
    given_line = given_colorized_line + given_non_color_line

    expected_background_color = RGB(3, 2, 1)
    expected_line = given_colorized_line + [
        Pixel(
            pixel.get_char(), background_color=expected_background_color
        ) for pixel in given_colorized_line
    ]

    fragment = ColorizeLineFragment(
        given_line,
        background_color=expected_background_color
    )
    assert fragment_to_list(fragment) == expected_line


def test_that_colorized_line_just_colorize_non_colorized_pixels():
    given_foreground_color = RGB(3, 2, 1)
    given_background_color = RGB(1, 2, 3)

    given_start_fg = RGB(0, 0, 0)
    given_start_bg = RGB(1, 1, 1)

    given_line_pixels = [
        Pixel('B'),
        Pixel('y', given_start_fg, given_start_bg),
        Pixel('e')
    ]

    fragment = ColorizeLineFragment(
        given_line_pixels,
        foreground_color=given_foreground_color,
        background_color=given_background_color
    )

    expected_line_pixels = [
        Pixel(
            char='B',
            foreground_color=given_foreground_color,
            background_color=given_background_color
        ),
        Pixel(
            char='y',
            foreground_color=given_start_fg,
            background_color=given_start_bg
        ),
        Pixel(
            char='e',
            foreground_color=given_foreground_color,
            background_color=given_background_color
        )
    ]
    assert list(fragment) == expected_line_pixels
