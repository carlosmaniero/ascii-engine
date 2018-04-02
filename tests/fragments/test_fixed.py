import pytest
from ascii_engine.fragments.fixed import FixedLineFragment
from ascii_engine.fragments.fixed import FixedMatrixFragment
from ascii_engine.pixel import Pixel
from tests.fragments.utils import fragment_to_list


def test_that_given_a_larger_line_the_fixed_line_truncates_it():
    given_text = "Hello, World!"
    given_fragment = [Pixel(char) for char in given_text]

    fragment = FixedLineFragment(given_fragment, 4)

    assert list(fragment) == [
        Pixel('H'),
        Pixel('e'),
        Pixel('l'),
        Pixel('l')
    ]

    with pytest.raises(IndexError):
        # noinspection PyStatementEffect
        fragment[4]


def test_that_fixed_fragment_can_fixes_only_the_width():
    expected_lines = [
        [Pixel('a'), Pixel('b'), Pixel(' ')],
        [Pixel('c'), Pixel('d'), Pixel(' ')],
    ]

    lines = [
        expected_lines[0][:2],
        expected_lines[1][:2]
    ]

    fragment = FixedMatrixFragment(
        lines_fragment=lines,
        width=3
    )

    iterations = 0
    for expected_line, line in zip(expected_lines, fragment):
        assert expected_line == list(line)
        iterations += 1

    assert iterations == len(expected_lines)


def test_that_fixed_fragment_truncates_given_a_larger_content():
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

    fragment = FixedMatrixFragment(
        lines_fragment=lines,
        width=2,
        height=2
    )

    iterations = 0
    for index, line in enumerate(fragment):
        assert list(line) == expected_lines[index]
        iterations += 1

    assert iterations == len(expected_lines)


def test_that_fixed_fragment_assumes_the_width_of_largest_line_by_default():
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

    fragment = FixedMatrixFragment(
        lines_fragment=lines,
        height=4
    )

    iterations = 0
    for expected_line, line in zip(expected_lines, fragment):
        assert expected_line == list(line)
        iterations += 1

    assert iterations == len(expected_lines)


def test_that_fixed_fragment_has_the_length_equal_the_given_height():
    assert len(FixedMatrixFragment([], height=3)) == 3


def test_that_all_lines_of_fixed_fragment_is_equal_the_given_width():
    assert all(
        len(line) == 3 for line in FixedMatrixFragment([], height=3, width=3))
