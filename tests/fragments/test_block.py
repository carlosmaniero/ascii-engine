import pytest
from ascii_engine.fragments.block import BlockPixelLineFragment
from ascii_engine.fragments.block import BlockPixelFragment
from ascii_engine.pixel import Pixel
from tests.fragments.utils import fragment_to_list


def test_that_block_line_fragment_renders_each_line_of_a_given_line():
    given_text = "Hello, World!"

    expected_text = given_text + '   '
    given_fragment = [Pixel(char) for char in given_text]

    fragment = BlockPixelLineFragment(given_fragment, len(expected_text))

    iterations = 0
    for char, pixel in zip(expected_text, fragment):
        assert Pixel(char) == pixel
        iterations += 1

    assert iterations == len(expected_text)


def test_that_given_an_larger_line_the_block_line_trucate_it():
    given_text = "Hello, World!"
    given_fragment = [Pixel(char) for char in given_text]

    fragment = BlockPixelLineFragment(given_fragment, 4)

    assert list(fragment) == [
        Pixel('H'),
        Pixel('e'),
        Pixel('l'),
        Pixel('l')
    ]

    with pytest.raises(IndexError):
        fragment[4]


def test_that_block_line_fragment_has_the_length_equals_the_given_text():
    given_fragment = [Pixel(' ')]

    assert len(BlockPixelLineFragment(given_fragment, 1000)) == 1000


def test_that_block_line_fragment_deals_with_slices():
    given_text = "Hello, World"
    given_fragment = [Pixel(char) for char in given_text]
    given_empty_fragment = []

    fragment = BlockPixelLineFragment(given_fragment, 100)
    empty_fragment = BlockPixelLineFragment(given_empty_fragment, 0)

    assert list(fragment[:2]) == [Pixel('H'), Pixel('e')]
    assert list(fragment[10:]) == [Pixel('l'), Pixel('d')] + [Pixel(' ')] * 88
    assert list(fragment[:101]) == [Pixel(char) for char in given_text] + [Pixel(' ')] * 88
    assert list(fragment[11:14]) == [Pixel('d'), Pixel(' '), Pixel(' ')]
    assert list(fragment[4:14:4]) == [Pixel('o'), Pixel('o'), Pixel(' ')]
    assert list(empty_fragment[::4]) == []


def test_that_block_line_fragment_deals_with_indexs():
    given_text = "Hello, World"
    given_fragment = [Pixel(char) for char in given_text]

    fragment = BlockPixelLineFragment(given_fragment, 100)

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


def test_that_block_fragment_works_with_slices_and_index():
    lines = [
        [Pixel('a'), Pixel('b'), Pixel('c')],
        [Pixel('d'), Pixel('e'), Pixel('f')],
    ]

    fragment = BlockPixelFragment(
        lines_fragment=lines,
        width=3,
        height=3
    )

    expected_empty_line = [Pixel(' ') for _ in range(3)]
    expected_block = lines.copy()
    expected_block.append(expected_empty_line)

    assert fragment_to_list(fragment[1:]) == expected_block[1:]
    assert fragment_to_list(fragment[:1]) == expected_block[:1]
    assert list(fragment[1]) == expected_block[1]
    assert list(fragment[2]) == expected_block[2]

    with pytest.raises(IndexError):
        fragment[3]


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


def test_that_when_a_block_is_called_by_index_it_always_returns_a_blocked_line():
    line = [
        [Pixel('a'), Pixel('b')],
        [Pixel('c'), Pixel('d'), Pixel('e')]
    ]

    assert list(BlockPixelFragment(line)[0]) == [Pixel('a'), Pixel('b'), Pixel(' ')]