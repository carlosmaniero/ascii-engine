import pytest

from ascii_engine.fragments.base import SliceIterableFragment
from ascii_engine.pixel import Pixel


def test_that_slices_just_returns_the_index_of_the_given_fragment():
    given_fragment = [Pixel('a'), Pixel('b')]
    slice_fragment = SliceIterableFragment(given_fragment, 0, 2, 1)

    assert slice_fragment[0] == given_fragment[0]
    assert slice_fragment[1] == given_fragment[1]
    assert slice_fragment[-1] == given_fragment[-1]

    with pytest.raises(IndexError):
        assert slice_fragment[2]


def test_that_slices_has_the_same_behavior_of_an_array_slice():
    given_fragment = [Pixel('a'), Pixel('b')]

    assert list(SliceIterableFragment(given_fragment, 0, 2, 1)) == given_fragment
    assert list(SliceIterableFragment(given_fragment, 0, 2, 2)) == given_fragment[0:2:2]
    assert list(SliceIterableFragment(given_fragment, 1, 2, 1)) == given_fragment[1:2:1]