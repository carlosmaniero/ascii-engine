from collections import namedtuple

import pytest

from ascii_engine.colors import RGB
from ascii_engine.fragments.align import AlignCenterLineFragment, \
    AlignRightLineFragment, AlignMatrixRightLineFragment
from ascii_engine.fragments.colorize import ColorizeMatrixFragment
from ascii_engine.pixel import Pixel
from tests.fragments.utils import fragment_to_list

ParameterTestData = namedtuple('ParameterTestData', ['fragment', 'expected'])

given_line_fragment = [
    Pixel('H'),
    Pixel('e'),
    Pixel('l'),
    Pixel('l'),
    Pixel('o'),
]

given_matrix_fragment = [
    given_line_fragment,
    [
        Pixel('B'),
        Pixel('y'),
        Pixel('e'),
    ],
    [
        Pixel('.'),
        Pixel('.'),
        Pixel('.'),
    ]
]


tests_data = [
    ParameterTestData(
        AlignCenterLineFragment(given_line_fragment, 11),
        [Pixel(' ')] * 3 + given_line_fragment + [Pixel(' ')] * 3
    ),
    ParameterTestData(
        AlignRightLineFragment(given_line_fragment, 10),
        [Pixel(' ')] * 5 + given_line_fragment
    ),
    ParameterTestData(
        AlignMatrixRightLineFragment(given_matrix_fragment, 10),
        [
            [Pixel(' ')] * 5 + given_matrix_fragment[0],
            [Pixel(' ')] * 7 + given_matrix_fragment[1],
            [Pixel(' ')] * 7 + given_matrix_fragment[2],
        ]
    ),
    ParameterTestData(
        ColorizeMatrixFragment(
            given_matrix_fragment,
            foreground_color=RGB(3, 2, 1),
            background_color=RGB(1, 2, 3)
        ),
        [
            [
                Pixel('H', RGB(3, 2, 1), RGB(1, 2, 3)),
                Pixel('e', RGB(3, 2, 1), RGB(1, 2, 3)),
                Pixel('l', RGB(3, 2, 1), RGB(1, 2, 3)),
                Pixel('l', RGB(3, 2, 1), RGB(1, 2, 3)),
                Pixel('o', RGB(3, 2, 1), RGB(1, 2, 3)),
            ],
            [
                Pixel('B', RGB(3, 2, 1), RGB(1, 2, 3)),
                Pixel('y', RGB(3, 2, 1), RGB(1, 2, 3)),
                Pixel('e', RGB(3, 2, 1), RGB(1, 2, 3)),
            ],
            [
                Pixel('.', RGB(3, 2, 1), RGB(1, 2, 3)),
                Pixel('.', RGB(3, 2, 1), RGB(1, 2, 3)),
                Pixel('.', RGB(3, 2, 1), RGB(1, 2, 3)),
            ]
        ]
    )
]

@pytest.mark.parametrize('test_data', tests_data)
def test_assert_elements_has_the_same_length(test_data):
    assert len(test_data.fragment) == len(test_data.expected)


@pytest.mark.parametrize('test_data', tests_data)
def test_raises_an_index_error_when_accessing_fragment_length_as_index(
        test_data):
    with pytest.raises(IndexError):
        # noinspection PyStatementEffect
        test_data.fragment[len(test_data.fragment)]


@pytest.mark.parametrize('test_data', tests_data)
def test_raises_an_index_error_when_accessing_a_negative_length_as_index(
        test_data):
    with pytest.raises(IndexError):
        # noinspection PyStatementEffect
        test_data.fragment[-len(test_data.fragment)]


@pytest.mark.parametrize('test_data', tests_data)
def test_line_is_the_expected_when_iterated(test_data):
    assert fragment_to_list(test_data.fragment) == test_data.expected


@pytest.mark.parametrize('test_data', tests_data)
def test_line_is_the_expected_when_iterated(test_data):
    assert fragment_to_list(test_data.fragment) == test_data.expected


@pytest.mark.parametrize('test_data', tests_data)
def test_line_is_the_expected_when_accessing_by_index(test_data):
    for index, pixel in enumerate(test_data.expected):
        assert fragment_to_list(test_data.fragment[index]) == pixel


@pytest.mark.parametrize('test_data', tests_data)
def test_line_is_the_expected_when_accessing_by_reverse_index(test_data):
    for index in range(1 - len(test_data.fragment), 1, 1):
        assert fragment_to_list(
            test_data.fragment[index]) == test_data.expected[index]


@pytest.mark.parametrize('test_data', tests_data)
def raises_an_index_error_when_accessing_fragment_length_as_index(test_data):
    with pytest.raises(IndexError):
        # noinspection PyStatementEffect
        test_data.fragment[len(test_data.fragment)]


@pytest.mark.parametrize('test_data', tests_data)
def test_fragment_is_sliceable(test_data):
    half = len(test_data.fragment) // 2
    assert fragment_to_list(
        test_data.fragment[:half]) == test_data.expected[:half]

    assert fragment_to_list(
        test_data.fragment[half:]) == test_data.expected[half:]

    assert fragment_to_list(
        test_data.fragment[::2]) == test_data.expected[::2]

    assert fragment_to_list(
        test_data.fragment[half::2]) == test_data.expected[half::2]

    assert fragment_to_list(
        test_data.fragment[:half:2]) == test_data.expected[:half:2]

    assert fragment_to_list(
        test_data.fragment[half:half]) == []

    assert fragment_to_list(
        test_data.fragment[::-1]) == test_data.expected[::-1]

    assert fragment_to_list(
        test_data.fragment[:half:-1]) == test_data.expected[:half:-1]

    assert fragment_to_list(
        test_data.fragment[half::-1]) == test_data.expected[half::-1]

    assert fragment_to_list(
        test_data.fragment[:-1:-1]) == test_data.expected[:-1:-1]

    assert fragment_to_list(
        test_data.fragment[-2::-1]) == test_data.expected[-2::-1]

    assert fragment_to_list(
        test_data.fragment[-2:half:-1]) == test_data.expected[-2:half:-1]


@pytest.mark.parametrize('test_data', tests_data)
def test_fragment_slices_length(test_data):
    half = len(test_data.fragment) // 2
    assert len(
        test_data.fragment[:half]) == len(test_data.expected[:half])
    assert len(
        test_data.fragment[half:]) == len(test_data.expected[half:])
    assert len(
        test_data.fragment[::2]) == len(test_data.expected[::2])
    assert len(
        test_data.fragment[half::2]) == len(test_data.expected[half::2])
    assert len(
        test_data.fragment[:half:2]) == len(test_data.expected[:half:2])
    assert len(
        test_data.fragment[half:half]) == 0
