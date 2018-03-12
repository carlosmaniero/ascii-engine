import pytest
from ascii_engine.fragments.join import JoinMultiLineVerticallyFragment
from ascii_engine.pixel import Pixel
from tests.fragments.utils import fragment_to_list


def test_join_multi_line_fragments_vertically_put_each_above_other():
    pixels1 = [
        [Pixel('a'), Pixel('b')],
        [Pixel('c'), Pixel('d')],
    ]

    pixels2 = [
        [Pixel('b'), Pixel('b')],
        [Pixel('d'), Pixel('d')],
    ]

    expected_fragment = pixels1 + pixels2
    fragment = JoinMultiLineVerticallyFragment(pixels1, pixels2)
    assert fragment_to_list(fragment) == expected_fragment


def test_join_multiline_fragment_has_the_length_equal_the_fragment_length_sum():
    pixels1 = [
        [Pixel('a'), Pixel('b')],
        [Pixel('c'), Pixel('d')],
    ]

    pixels2 = [
        [Pixel('b'), Pixel('b')],
        [Pixel('d'), Pixel('d')],
        [Pixel('c'), Pixel('c')],
    ]

    expected_length = 5
    fragment = JoinMultiLineVerticallyFragment(pixels1, pixels2)

    assert len(fragment) == expected_length


def test_join_multi_line_fragment_deals_with_indexing():
    pixels1 = [
        [Pixel('a'), Pixel('b')],
        [Pixel('c'), Pixel('d')],
    ]

    pixels2 = [
        [Pixel('b'), Pixel('b')],
        [Pixel('d'), Pixel('d')],
        [Pixel('c'), Pixel('c')],
    ]

    fragment = JoinMultiLineVerticallyFragment(pixels1, pixels2)
    assert list(fragment[0]) == pixels1[0]
    assert list(fragment[3]) == pixels2[1]

    with pytest.raises(IndexError):
        fragment[5]

    with pytest.raises(IndexError):
        JoinMultiLineVerticallyFragment()[1]


def test_join_multiline_fragment_deals_with_slices():
    pixels1 = [
        [Pixel('a'), Pixel('b')],
        [Pixel('c'), Pixel('d')],
    ]

    pixels2 = [
        [Pixel('b'), Pixel('b')],
        [Pixel('d'), Pixel('d')],
    ]

    expected_fragment = pixels1 + pixels2[:1]
    fragment = JoinMultiLineVerticallyFragment(pixels1, pixels2)

    assert fragment_to_list(fragment[:3]) == expected_fragment
    assert len(fragment[:3]) == 3
