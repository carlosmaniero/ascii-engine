import pytest
from ascii_engine.fragments.colorize import ColorizeLinePixelsFragment
from ascii_engine.fragments.colorize import ColorizeMultiLinePixelsFragment
from ascii_engine.colors import RGB
from ascii_engine.pixel import Pixel
from tests.elements.fragments.utils import fragment_to_list


def test_that_colorized_line_pixels_set_the_foreground_of_a_given_line():
    text = "Hello, World"

    given_color = RGB(1, 2, 3)
    given_line_pixels = [Pixel(char) for char in text]

    fragment = ColorizeLinePixelsFragment(given_line_pixels, foreground_color=given_color)

    expected_line_pixels = [Pixel(char, foreground_color=given_color) for char in text]
    assert list(fragment) == expected_line_pixels


def test_that_colorized_line_pixels_set_the_background_of_a_given_line():
    text = "Hello, World"

    given_color = RGB(1, 2, 3)
    given_line_pixels = [Pixel(char) for char in text]

    fragment = ColorizeLinePixelsFragment(given_line_pixels, background_color=given_color)

    expected_line_pixels = [Pixel(char, background_color=given_color) for char in text]
    assert list(fragment) == expected_line_pixels


def test_that_colorized_line_pixels_set_the_foreground_and_background_of_a_given_line():
    text = "Hello, World"

    given_foreground_color = RGB(3, 2, 1)
    given_background_color = RGB(1, 2, 3)
    given_line_pixels = [Pixel(char) for char in text]

    fragment = ColorizeLinePixelsFragment(
        given_line_pixels,
        foreground_color=given_foreground_color,
        background_color=given_background_color
    )

    expected_line_pixels = [
        Pixel(
            char=char,
            foreground_color=given_foreground_color,
            background_color=given_background_color
        ) for char in text
    ]
    assert list(fragment) == expected_line_pixels


def test_that_colorized_line_pixels_accepts_slices():
    text = "Hello, World"

    given_foreground_color = RGB(3, 2, 1)
    given_background_color = RGB(1, 2, 3)
    given_line_pixels = [Pixel(char) for char in text]

    fragment = ColorizeLinePixelsFragment(
        given_line_pixels,
        foreground_color=given_foreground_color,
        background_color=given_background_color
    )

    expected_line_pixels = [
        Pixel(
            char=char,
            foreground_color=given_foreground_color,
            background_color=given_background_color
        ) for char in text
    ]
    assert list(fragment[1:]) == expected_line_pixels[1:]
    assert list(fragment[:2]) == expected_line_pixels[:2]
    assert list(fragment[::2]) == expected_line_pixels[::2]


def test_that_colorized_line_pixels_accepts_indexing():
    text = "Hello, World"

    given_foreground_color = RGB(3, 2, 1)
    given_background_color = RGB(1, 2, 3)
    given_line_pixels = [Pixel(char) for char in text]

    fragment = ColorizeLinePixelsFragment(
        given_line_pixels,
        foreground_color=given_foreground_color,
        background_color=given_background_color
    )

    expected_line_pixels = [
        Pixel(
            char=char,
            foreground_color=given_foreground_color,
            background_color=given_background_color
        ) for char in text
    ]
    assert fragment[1] == expected_line_pixels[1]
    assert fragment[-1] == expected_line_pixels[-1]

    with pytest.raises(IndexError):
        fragment[len(text)]

    with pytest.raises(IndexError):
        fragment["anything-that-is-invalid"]


def test_that_colorized_line_just_colorize_non_colorized_pixels():
    given_foreground_color = RGB(3, 2, 1)
    given_background_color = RGB(1, 2, 3)

    given_line_pixels = [
        Pixel('B'),
        Pixel('y', foreground_color=RGB(0, 0, 0), background_color=RGB(1, 1, 1)),
        Pixel('e')
    ]

    fragment = ColorizeLinePixelsFragment(
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
            foreground_color=RGB(0, 0, 0),
            background_color=RGB(1, 1, 1)
        ),
        Pixel(
            char='e',
            foreground_color=given_foreground_color,
            background_color=given_background_color
        )
    ]
    assert list(fragment) == expected_line_pixels


def test_that_colorized_line_has_the_length_equals_the_given_line():
    assert len(ColorizeLinePixelsFragment([])) == 0
    assert len(ColorizeLinePixelsFragment([Pixel('a'), Pixel('b')])) == 2


def test_that_colorized_multi_line_pixels_set_the_foreground_and_background_of_a_given_line():
    text1 = "Hello"
    text2 = "World"

    given_foreground_color = RGB(3, 2, 1)
    given_background_color = RGB(1, 2, 3)
    given_line_pixels = [
        [Pixel(char) for char in text1],
        [Pixel(char) for char in text2],
    ]

    fragment = ColorizeMultiLinePixelsFragment(
        given_line_pixels,
        foreground_color=given_foreground_color,
        background_color=given_background_color
    )

    expected_line_pixels = [
        [
            Pixel(
                char=char,
                foreground_color=given_foreground_color,
                background_color=given_background_color
            ) for char in text1
        ],
        [
            Pixel(
                char=char,
                foreground_color=given_foreground_color,
                background_color=given_background_color
            ) for char in text2
        ],
    ]
    assert fragment_to_list(fragment) == expected_line_pixels


def test_that_colorized_multi_line_pixels_supportes_slices():
    text1 = "Hello"
    text2 = "World"

    given_foreground_color = RGB(3, 2, 1)
    given_background_color = RGB(1, 2, 3)
    given_line_pixels = [
        [Pixel(char) for char in text1],
        [Pixel(char) for char in text2],
    ]

    fragment = ColorizeMultiLinePixelsFragment(
        given_line_pixels,
        foreground_color=given_foreground_color,
        background_color=given_background_color
    )

    expected_line_pixels = [
        [
            Pixel(
                char=char,
                foreground_color=given_foreground_color,
                background_color=given_background_color
            ) for char in text1
        ],
        [
            Pixel(
                char=char,
                foreground_color=given_foreground_color,
                background_color=given_background_color
            ) for char in text2
        ],
    ]
    assert fragment_to_list(fragment[1:]) == expected_line_pixels[1:]
    assert fragment_to_list(fragment[:2]) == expected_line_pixels[:2]
    assert fragment_to_list(fragment[::2]) == expected_line_pixels[::2]


def test_that_colorized_multi_line_pixels_supportes_indexing():
    text1 = "Hello"
    text2 = "World"

    given_foreground_color = RGB(3, 2, 1)
    given_background_color = RGB(1, 2, 3)
    given_line_pixels = [
        [Pixel(char) for char in text1],
        [Pixel(char) for char in text2],
    ]

    fragment = ColorizeMultiLinePixelsFragment(
        given_line_pixels,
        foreground_color=given_foreground_color,
        background_color=given_background_color
    )

    expected_line_pixels = [
        [
            Pixel(
                char=char,
                foreground_color=given_foreground_color,
                background_color=given_background_color
            ) for char in text1
        ],
        [
            Pixel(
                char=char,
                foreground_color=given_foreground_color,
                background_color=given_background_color
            ) for char in text2
        ],
    ]
    assert list(fragment[1]) == expected_line_pixels[1]
    assert list(fragment[-1]) == expected_line_pixels[-1]

    with pytest.raises(IndexError):
        fragment[len(expected_line_pixels)]

    with pytest.raises(IndexError):
        fragment['Anything-else']


def test_that_colorized_multi_line_has_the_length_equals_the_given_line():
    assert len(ColorizeMultiLinePixelsFragment([])) == 0
    assert len(ColorizeMultiLinePixelsFragment([[], []])) == 2
