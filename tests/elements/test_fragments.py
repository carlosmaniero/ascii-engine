import pytest
from ascii_engine.elements.fragments import StringLineToPixelFragment
from ascii_engine.elements.fragments import MultiLineStringToPixelFragment
from ascii_engine.elements.fragments import BlockPixelLineFragment
from ascii_engine.elements.fragments import BlockPixelFragment
from ascii_engine.elements.fragments import ColorizeLinePixelsFragment
from ascii_engine.elements.fragments import ColorizeMultiLinePixelsFragment
from ascii_engine.pixel import Pixel
from ascii_engine.colors import RGB


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



def test_that_colorized_line_has_the_length_equals_the_given_line():
    assert len(ColorizeMultiLinePixelsFragment([])) == 0
    assert len(ColorizeMultiLinePixelsFragment([[], []])) == 2


def fragment_to_list(fragment):
    return [list(line) for line in fragment]


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


def test_that_line_fragment_colorizes_the_text():
    assert list(StringLineToPixelFragment("Hi", RGB(200, 100, 0), RGB(0, 100, 200))) == [
        Pixel('H', RGB(200, 100, 0), RGB(0, 100, 200)),
        Pixel('i', RGB(200, 100, 0), RGB(0, 100, 200))
    ]
    assert StringLineToPixelFragment("Hi", RGB(200, 100, 0), RGB(0, 100, 200))[0] == Pixel(
        'H', RGB(200, 100, 0), RGB(0, 100, 200)
    )


def test_that_block_line_fragment_renders_each_line_of_a_given_line():
    text = "Hello, World!"
    expected_text = text + '   '

    fragment = BlockPixelLineFragment(StringLineToPixelFragment(text), len(expected_text))

    iterations = 0
    for char, pixel in zip(expected_text, fragment):
        assert Pixel(char) == pixel
        iterations += 1

    assert iterations == len(expected_text)


def test_that_given_an_larger_line_the_block_line_trucate_it():
    text = "Hello, World!"

    fragment = BlockPixelLineFragment(StringLineToPixelFragment(text), 4)

    assert list(fragment) == [
        Pixel('H'),
        Pixel('e'),
        Pixel('l'),
        Pixel('l')
    ]

    with pytest.raises(IndexError):
        fragment[4]


def test_that_block_line_fragment_has_the_length_equals_the_given_text():
    text = "Hello, World!"

    assert len(BlockPixelLineFragment(StringLineToPixelFragment(text), 1000)) == 1000


def test_that_block_line_fragment_deals_with_slices():
    text = "Hello, World"

    fragment = BlockPixelLineFragment(StringLineToPixelFragment(text), 100)
    empty_fragment = BlockPixelLineFragment(StringLineToPixelFragment(''), 0)

    assert list(fragment[:2]) == [Pixel('H'), Pixel('e')]
    assert list(fragment[10:]) == [Pixel('l'), Pixel('d')] + [Pixel(' ')] * 88
    assert list(fragment[:101]) == [Pixel(char) for char in text] + [Pixel(' ')] * 88
    assert list(fragment[11:14]) == [Pixel('d'), Pixel(' '), Pixel(' ')]
    assert list(fragment[4:14:4]) == [Pixel('o'), Pixel('o'), Pixel(' ')]
    assert list(empty_fragment[::4]) == []


def test_that_block_line_fragment_colorizes_the_text():
    fragment = BlockPixelLineFragment(
        StringLineToPixelFragment("Hi"),
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


def test_that_block_line_fragment_use_the_text_background_when_given():
    fragment = BlockPixelLineFragment(
        StringLineToPixelFragment(
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


def test_that_block_line_fragment_use_the_text_foreground_when_given():
    fragment = BlockPixelLineFragment(
        StringLineToPixelFragment(
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


def test_that_block_line_fragment_deals_with_indexs():
    text = "Hello, World"
    fragment = BlockPixelLineFragment(StringLineToPixelFragment(text), 100)

    assert fragment[0] == Pixel('H')
    assert fragment[7] == Pixel('W')
    assert fragment[99] == Pixel(' ')

    with pytest.raises(IndexError):
        fragment[100]


def test_that_block_fragment_renders_each_line_of_a_given_line():
    expected_lines = [
        [Pixel('a'), Pixel('b'), Pixel(' ')],
        [Pixel('c'), Pixel('d'), Pixel(' ')],
        [Pixel(' '), Pixel(' '), Pixel(' ')]
    ]

    lines = [
        expected_lines[0][:2],
        expected_lines[1][:2]
    ]

    fragment = BlockPixelFragment(
        lines_fragment=lines,
        width=3,
        height=3
    )

    iterations = 0
    for expected_line, line in zip(expected_lines, fragment):
        assert expected_line == list(line)
        iterations += 1

    assert iterations == len(expected_lines)



def test_that_block_fragment_can_blocks_only_the_width():
    expected_lines = [
        [Pixel('a'), Pixel('b'), Pixel(' ')],
        [Pixel('c'), Pixel('d'), Pixel(' ')],
    ]

    lines = [
        expected_lines[0][:2],
        expected_lines[1][:2]
    ]

    fragment = BlockPixelFragment(
        lines_fragment=lines,
        width=3
    )

    iterations = 0
    for expected_line, line in zip(expected_lines, fragment):
        assert expected_line == list(line)
        iterations += 1

    assert iterations == len(expected_lines)


def test_that_block_fragment_truncate_the_contant_if_it_exeeds_width_and_height():
    lines = [
        [Pixel('a'), Pixel('b'), Pixel(' ')],
        [Pixel('c'), Pixel('d'), Pixel('e')],
        [Pixel('f'), Pixel(' '), Pixel(' ')],
        [Pixel(' '), Pixel(' '), Pixel(' ')]
    ]

    expected_lines = [
        lines[0][:2],
        lines[1][:2],
    ]

    fragment = BlockPixelFragment(
        lines_fragment=lines,
        width=2,
        height=2
    )

    iterations = 0
    for index, line in enumerate(fragment):
        assert list(line) == expected_lines[index]
        iterations += 1

    assert iterations == len(expected_lines)


def test_that_block_fragment_can_blocks_only_the_height_by_using_the_max_line_width():
    expected_lines = [
        [Pixel('a'), Pixel('b'), Pixel(' ')],
        [Pixel('c'), Pixel('d'), Pixel('e')],
        [Pixel('f'), Pixel(' '), Pixel(' ')],
        [Pixel(' '), Pixel(' '), Pixel(' ')]
    ]

    lines = [
        expected_lines[0][:2],
        expected_lines[1][:3],
        expected_lines[2][:1]
    ]

    fragment = BlockPixelFragment(
        lines_fragment=lines,
        height=4
    )

    iterations = 0
    for expected_line, line in zip(expected_lines, fragment):
        assert expected_line == list(line)
        iterations += 1

    assert iterations == len(expected_lines)


def test_that_block_fragment_has_the_length_equal_the_given_height():
    assert len(BlockPixelFragment([], height=3)) == 3


def test_that_all_lines_of_block_fragment_is_equal_the_given_width():
    assert all(len(line) == 3 for line in BlockPixelFragment([], height=3, width=3))


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
