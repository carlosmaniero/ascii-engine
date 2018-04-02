from collections import namedtuple

import pytest

from ascii_engine.colors import RGB
from ascii_engine.fragments.align import AlignCenterLineFragment, \
    AlignRightLineFragment, AlignMatrixRightLineFragment, \
    AlignMatrixCenterLineFragment
from ascii_engine.fragments.colorize import ColorizeMatrixFragment, \
    ColorizeLineFragment
from ascii_engine.fragments.converter import StringToPixelLineFragment, \
    StringToPixelMatrixFragment
from ascii_engine.fragments.fixed import FixedLineFragment, FixedMatrixFragment
from ascii_engine.fragments.join import JoinVerticallyMatrixFragment
from ascii_engine.pixel import Pixel
from tests.fragments.utils import fragment_to_list

ParameterTestData = namedtuple('ParameterTestData', ['fragment', 'expected'])

given_text = 'Hello'

given_line_fragment = [
    Pixel(char) for char in given_text
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


def param(fragment, expected):
    return pytest.param(fragment, expected, id=type(fragment).__name__)


tests_data = [
    param(
        AlignCenterLineFragment(given_line_fragment, 11),
        [Pixel(' ')] * 3 + given_line_fragment + [Pixel(' ')] * 3,
    ),
    param(
        AlignRightLineFragment(given_line_fragment, 10),
        [Pixel(' ')] * 5 + given_line_fragment
    ),
    param(
        AlignMatrixRightLineFragment(given_matrix_fragment, 10),
        [
            [Pixel(' ')] * 5 + given_matrix_fragment[0],
            [Pixel(' ')] * 7 + given_matrix_fragment[1],
            [Pixel(' ')] * 7 + given_matrix_fragment[2],
        ]
    ),

    param(
        AlignMatrixCenterLineFragment(given_matrix_fragment, 10),
        [
            [Pixel(' ')] * 2 + given_matrix_fragment[0] + [Pixel(' ')] * 3,
            [Pixel(' ')] * 3 + given_matrix_fragment[1] + [Pixel(' ')] * 4,
            [Pixel(' ')] * 3 + given_matrix_fragment[2] + [Pixel(' ')] * 4,
        ]
    ),
    param(
        ColorizeLineFragment(
            given_line_fragment,
            foreground_color=RGB(3, 2, 1),
            background_color=RGB(1, 2, 3)),
        [
            Pixel('H', RGB(3, 2, 1), RGB(1, 2, 3)),
            Pixel('e', RGB(3, 2, 1), RGB(1, 2, 3)),
            Pixel('l', RGB(3, 2, 1), RGB(1, 2, 3)),
            Pixel('l', RGB(3, 2, 1), RGB(1, 2, 3)),
            Pixel('o', RGB(3, 2, 1), RGB(1, 2, 3)),
        ]
    ),
    param(
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
    ),
    param(
        StringToPixelLineFragment(given_text),
        given_line_fragment
    ),
    param(
        StringToPixelMatrixFragment([
            "Hello",
            "Bye",
            "..."
        ]),
        given_matrix_fragment
    ),
    param(
        FixedLineFragment(given_line_fragment, 10),
        given_line_fragment + [Pixel(' ')] * 5
    ),
    param(
        FixedMatrixFragment(
            lines_fragment=given_matrix_fragment,
            width=10,
            height=5
        ),
        [
            given_matrix_fragment[0] + [Pixel(' ')] * 5,
            given_matrix_fragment[1] + [Pixel(' ')] * 7,
            given_matrix_fragment[2] + [Pixel(' ')] * 7,
            [Pixel(' ')] * 10,
            [Pixel(' ')] * 10
        ]
    ),
    param(
        JoinVerticallyMatrixFragment([
            [given_matrix_fragment[0], given_matrix_fragment[1]],
            [given_matrix_fragment[2]]
        ]),
        given_matrix_fragment
    ),
]


@pytest.mark.parametrize('fragment, expected', tests_data)
def test_assert_elements_has_the_same_length(fragment, expected):
    assert len(fragment) == len(expected)


@pytest.mark.parametrize('fragment, expected', tests_data)
def test_raises_an_index_error_when_accessing_fragment_length_as_index(
        fragment, expected):
    with pytest.raises(IndexError):
        # noinspection PyStatementEffect
        fragment[len(fragment)]


@pytest.mark.parametrize('fragment, expected', tests_data)
def test_raises_an_index_error_when_accessing_a_negative_length_as_index(
        fragment, expected):
    with pytest.raises(IndexError):
        # noinspection PyStatementEffect
        fragment[-len(fragment)]


@pytest.mark.parametrize('fragment, expected', tests_data)
def test_raises_an_index_error_when_accessing_a_non_int_or_slice(
        fragment, expected):
    with pytest.raises(IndexError):
        # noinspection PyStatementEffect
        fragment['this-is-an-invalid-index']

    with pytest.raises(IndexError):
        # noinspection PyStatementEffect
        fragment[Exception]


@pytest.mark.parametrize('fragment, expected', tests_data)
def test_line_is_the_expected_when_iterated(fragment, expected):
    assert fragment_to_list(fragment) == expected


@pytest.mark.parametrize('fragment, expected', tests_data)
def test_line_is_the_expected_when_iterated(fragment, expected):
    assert fragment_to_list(fragment) == expected


@pytest.mark.parametrize('fragment, expected', tests_data)
def test_line_is_the_expected_when_accessing_by_index(fragment, expected):
    for index, pixel in enumerate(expected):
        assert fragment_to_list(fragment[index]) == pixel


@pytest.mark.parametrize('fragment, expected', tests_data)
def test_line_is_the_expected_when_accessing_by_reverse_index(fragment,
                                                              expected):
    for index in range(1 - len(fragment), 1, 1):
        assert fragment_to_list(
            fragment[index]) == expected[index]


@pytest.mark.parametrize('fragment, expected', tests_data)
def raises_an_index_error_when_accessing_fragment_length_as_index(fragment,
                                                                  expected):
    with pytest.raises(IndexError):
        # noinspection PyStatementEffect
        fragment[len(fragment)]


@pytest.mark.parametrize('fragment, expected', tests_data)
def test_fragment_is_sliceable(fragment, expected):
    half = len(fragment) // 2
    assert fragment_to_list(
        fragment[:half]) == expected[:half]

    assert fragment_to_list(
        fragment[half:]) == expected[half:]

    assert fragment_to_list(
        fragment[::2]) == expected[::2]

    assert fragment_to_list(
        fragment[half::2]) == expected[half::2]

    assert fragment_to_list(
        fragment[:half:2]) == expected[:half:2]

    assert fragment_to_list(
        fragment[half:half]) == []

    assert fragment_to_list(
        fragment[::-1]) == expected[::-1]

    assert fragment_to_list(
        fragment[:half:-1]) == expected[:half:-1]

    assert fragment_to_list(
        fragment[half::-1]) == expected[half::-1]

    assert fragment_to_list(
        fragment[:-1:-1]) == expected[:-1:-1]

    assert fragment_to_list(
        fragment[:-half:-1]) == expected[:-half:-1]

    assert fragment_to_list(
        fragment[-2::-1]) == expected[-2::-1]

    assert fragment_to_list(
        fragment[-2:half:-1]) == expected[-2:half:-1]


@pytest.mark.parametrize('fragment, expected', tests_data)
def test_fragment_slices_length(fragment, expected):
    half = len(fragment) // 2
    assert len(
        fragment[:half]) == len(expected[:half])
    assert len(
        fragment[half:]) == len(expected[half:])
    assert len(
        fragment[::2]) == len(expected[::2])
    assert len(
        fragment[half::2]) == len(expected[half::2])
    assert len(
        fragment[:half:2]) == len(expected[:half:2])
    assert len(
        fragment[half:half]) == 0
