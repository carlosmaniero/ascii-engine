import pytest
from ascii_engine.elements.fragments import LineFragment
from ascii_engine.elements.fragments import MultiLineFragment
from ascii_engine.elements.fragments import ContainerizeLineFragment
from ascii_engine.pixel import Pixel
from ascii_engine.colors import RGB


def fragment_to_list(fragment):
    return [list(line) for line in fragment]


def test_that_line_fragment_renders_each_line_of_a_given_text():
    text = "Hello, World!"

    iterations = 0
    for char, pixel in zip(text, LineFragment(text)):
        assert Pixel(char) == pixel
        iterations += 1

    assert iterations == len(text)


def test_that_line_fragment_has_the_length_equals_the_given_text():
    text = "Hello, World!"

    assert len(LineFragment(text)) == len(text)


def test_that_line_fragment_deals_with_slices():
    text = "Hello, World"
    assert list(LineFragment(text)[:2]) == [Pixel('H'), Pixel('e')]
    assert list(LineFragment(text)[10:]) == [Pixel('l'), Pixel('d')]
    assert list(LineFragment(text)[2:4]) == [Pixel('l'), Pixel('l')]
    assert list(LineFragment(text)[::7]) == [Pixel('H'), Pixel('W')]


def test_that_line_fragment_deals_with_indexs():
    text = "Hello, World"
    assert LineFragment(text)[0] == Pixel('H')
    assert LineFragment(text)[7] == Pixel('W')


def test_that_line_fragment_raises_index_error_given_a_invalid_index():
    with pytest.raises(IndexError):
        LineFragment("Hi")[100]

    with pytest.raises(IndexError):
        LineFragment("Hi")["it is not a valid index"]


def test_that_line_fragment_colorizes_the_text():
    assert list(LineFragment("Hi", RGB(200, 100, 0), RGB(0, 100, 200))) == [
        Pixel('H', RGB(200, 100, 0), RGB(0, 100, 200)),
        Pixel('i', RGB(200, 100, 0), RGB(0, 100, 200))
    ]
    assert LineFragment("Hi", RGB(200, 100, 0), RGB(0, 100, 200))[0] == Pixel(
        'H', RGB(200, 100, 0), RGB(0, 100, 200)
    )


def test_that_containerize_line_fragment_renders_each_line_of_a_given_line():
    text = "Hello, World!"
    expected_text = text + '   '

    fragment = ContainerizeLineFragment(LineFragment(text), len(expected_text))

    iterations = 0
    for char, pixel in zip(expected_text, fragment):
        assert Pixel(char) == pixel
        iterations += 1

    assert iterations == len(expected_text)


def test_that_given_an_larger_line_the_containerize_line_trucate_it():
    text = "Hello, World!"

    fragment = ContainerizeLineFragment(LineFragment(text), 4)

    assert list(fragment) == [
        Pixel('H'),
        Pixel('e'),
        Pixel('l'),
        Pixel('l')
    ]

    with pytest.raises(IndexError):
        fragment[4]


def test_that_containerize_line_fragment_has_the_length_equals_the_given_text():
    text = "Hello, World!"

    assert len(ContainerizeLineFragment(LineFragment(text), 1000)) == 1000


def test_that_containerize_line_fragment_deals_with_slices():
    text = "Hello, World"

    fragment = ContainerizeLineFragment(LineFragment(text), 100)
    empty_fragment = ContainerizeLineFragment(LineFragment(''), 0)

    assert list(fragment[:2]) == [Pixel('H'), Pixel('e')]
    assert list(fragment[10:]) == [Pixel('l'), Pixel('d')] + [Pixel(' ')] * 88
    assert list(fragment[:101]) == [Pixel(char) for char in text] + [Pixel(' ')] * 88
    assert list(fragment[11:14]) == [Pixel('d'), Pixel(' '), Pixel(' ')]
    assert list(fragment[4:14:4]) == [Pixel('o'), Pixel('o'), Pixel(' ')]
    assert list(empty_fragment[::4]) == []


def test_that_containerize_line_fragment_colorizes_the_text():
    fragment = ContainerizeLineFragment(
        LineFragment("Hi"),
        3,
        RGB(200, 100, 0),
        RGB(0, 100, 200)
    )

    assert list(fragment) == [
        Pixel('H', RGB(200, 100, 0), RGB(0, 100, 200)),
        Pixel('i', RGB(200, 100, 0), RGB(0, 100, 200)),
        Pixel(' ', RGB(200, 100, 0), RGB(0, 100, 200))
    ]
    assert fragment[0] == Pixel(
        'H', RGB(200, 100, 0), RGB(0, 100, 200)
    )


def test_that_containerize_line_fragment_use_the_text_background_when_given():
    fragment = ContainerizeLineFragment(
        LineFragment(
            line='Hi',
            background_color=RGB(1, 2, 3)
        ),
        width=3,
        foreground_color=RGB(0, 0, 0),
        background_color=RGB(1, 1, 1)
    )

    assert list(fragment) == [
        Pixel('H', foreground_color=RGB(0, 0, 0), background_color=RGB(1, 2, 3)),
        Pixel('i', foreground_color=RGB(0, 0, 0), background_color=RGB(1, 2, 3)),
        Pixel(' ', foreground_color=RGB(0, 0, 0), background_color=RGB(1, 1, 1)),
    ]

    assert fragment[0] == Pixel(
        char='H',
        foreground_color=RGB(0, 0, 0),
        background_color=RGB(1, 2, 3)
    )

    assert fragment[2] == Pixel(
        char=' ',
        foreground_color=RGB(0, 0, 0),
        background_color=RGB(1, 1, 1)
    )


def test_that_containerize_line_fragment_use_the_text_foreground_when_given():
    fragment = ContainerizeLineFragment(
        LineFragment(
            line='Hi',
            foreground_color=RGB(3, 2, 1)
        ),
        width=3,
        foreground_color=RGB(0, 0, 0),
        background_color=RGB(1, 1, 1)
    )

    assert list(fragment) == [
        Pixel('H', foreground_color=RGB(3, 2, 1), background_color=RGB(1, 1, 1)),
        Pixel('i', foreground_color=RGB(3, 2, 1), background_color=RGB(1, 1, 1)),
        Pixel(' ', foreground_color=RGB(0, 0, 0), background_color=RGB(1, 1, 1)),
    ]

    assert fragment[0] == Pixel(
        char='H',
        foreground_color=RGB(3, 2, 1),
        background_color=RGB(1, 1, 1)
    )

    assert fragment[2] == Pixel(
        char=' ',
        foreground_color=RGB(0, 0, 0),
        background_color=RGB(1, 1, 1)
    )


def test_that_containerize_line_fragment_deals_with_indexs():
    text = "Hello, World"
    fragment = ContainerizeLineFragment(LineFragment(text), 100)

    assert fragment[0] == Pixel('H')
    assert fragment[7] == Pixel('W')
    assert fragment[99] == Pixel(' ')

    with pytest.raises(IndexError):
        fragment[100]


def test_that_mult_line_fragment_renders_each_line_of_a_given_text():
    lines = ["Hello", "World!"]

    for text_line, line in zip(lines, MultiLineFragment(lines)):
        assert list(line) == [Pixel(char) for char in text_line]


def test_that_multi_line_fragment_has_the_length_equals_the_given_text():
    lines = ["Hello", "World!"]

    assert len(MultiLineFragment(lines)) == len(lines)


def test_that_nulti_line_fragment_deals_with_slices():
    lines = ['ab', 'cd', 'ef']

    line_pixels = [
        [Pixel('a'), Pixel('b')],
        [Pixel('c'), Pixel('d')],
        [Pixel('e'), Pixel('f')]
    ]

    fragment = MultiLineFragment(lines)

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

    fragment = MultiLineFragment(lines)

    for index in range(len(fragment)):
        assert list(fragment[index]) == line_pixels[index]


def test_that_mult_line_fragment_raises_index_error_given_a_invalid_index():
    with pytest.raises(IndexError):
        MultiLineFragment(["Hi"])[100]

    with pytest.raises(IndexError):
        MultiLineFragment(["Hi"])["it is not a valid index"]
