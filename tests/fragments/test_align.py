from ascii_engine.pixel import Pixel
from ascii_engine.fragments.align import AlignRightLineFragment, \
    AlignCenterLineFragment, AlignMatrixRightLineFragment
from tests.fragments.utils import fragment_to_list


def test_that_the_align_right_line_fragment_put_anything_on_the_right_given_a_bigger_width():
    given_line_fragment = [Pixel('h'), Pixel('i')]
    given_width = 4
    expected_fragment = [Pixel(' '), Pixel(' '), Pixel('h'), Pixel('i')]

    the_fragment = AlignRightLineFragment(given_line_fragment, given_width)

    assert list(the_fragment) == expected_fragment


def test_that_the_align_right_line_fragment_is_slices_the_pixel_part_when_the_width_is_bigger_than_the_fragment():
    given_line_fragment = [
        Pixel('a'),
        Pixel('b'),
        Pixel('c'),
        Pixel('d'),
        Pixel('e')
    ]
    given_width = 10
    the_fragment = AlignRightLineFragment(given_line_fragment, given_width)
    assert given_line_fragment == list(the_fragment[5:])


def test_that_the_align_right_line_fragment_truncates_the_given_fragment_on_the_left():
    given_line_fragment = [
        Pixel('a'),
        Pixel('b'),
        Pixel('c'),
        Pixel('d'),
        Pixel('e')
    ]
    given_width = 2
    expected_fragment = [Pixel('a'), Pixel('b')]

    the_fragment = AlignRightLineFragment(given_line_fragment, given_width)

    assert list(the_fragment) == expected_fragment


def test_that_the_align_right_line_fragment_is_slices_the_blank_part_when_the_width_is_bigger_than_the_fragment():
    given_line_fragment = [
        Pixel('a'),
        Pixel('b'),
        Pixel('c'),
        Pixel('d'),
        Pixel('e')
    ]
    given_width = 10
    the_fragment = AlignRightLineFragment(given_line_fragment, given_width)

    expected_fragment = [Pixel(' ')] * 5
    assert expected_fragment == list(the_fragment[:5])



def test_that_the_align_right_line_fragment_is_slices_by_step():
    given_line_fragment = [
        Pixel('a'),
        Pixel('b'),
        Pixel('c'),
        Pixel('d'),
        Pixel('e')
    ]
    given_width = 10
    the_fragment = AlignRightLineFragment(given_line_fragment, given_width)
    assert list(the_fragment[:5]) == [Pixel(' ')] * 5
    assert list(the_fragment[5:]) == given_line_fragment
    assert list(the_fragment[::3]) == [Pixel(' '), Pixel(' '), Pixel('b'), Pixel('e')]


def test_multi_line_line_fragment_can_be_aligned_to_right():
    given_matrix_fragment = [
        [Pixel('H'), Pixel('i')],
        [Pixel('b'), Pixel('y'), Pixel('e')],
    ]
    given_width = 4

    the_fragment = AlignMatrixRightLineFragment(
        given_matrix_fragment,
        given_width
    )
    assert fragment_to_list(the_fragment) == [
        [Pixel(' '), Pixel(' '), Pixel('H'), Pixel('i')],
        [Pixel(' '), Pixel('b'), Pixel('y'), Pixel('e')],
    ]



def test_that_the_align_center_line_fragment_put_anything_on_the_center_given_a_bigger_width():
    given_line_fragment = [Pixel('a'), Pixel('b')]
    given_width = 4
    expected_fragment = [Pixel(' '), Pixel('a'), Pixel('b'), Pixel(' ')]

    the_fragment = AlignCenterLineFragment(given_line_fragment, given_width)

    assert list(the_fragment) == expected_fragment


def test_that_the_align_center_line_put_the_fragment_one_pixel_left_when_the_width_is_odd():
    given_line_fragment = [Pixel('a'), Pixel('b')]
    given_width = 5
    expected_fragment = [Pixel(' '), Pixel('a'), Pixel('b'), Pixel(' '), Pixel(' ')]

    the_fragment = AlignCenterLineFragment(given_line_fragment, given_width)

    assert list(the_fragment) == expected_fragment


def test_that_the_align_center_truncates_from_the_init():
    given_line_fragment = [Pixel('a'), Pixel('b'), Pixel('c'), Pixel('d')]
    given_width = 2
    expected_fragment = [Pixel('a'), Pixel('b')]

    the_fragment = AlignCenterLineFragment(given_line_fragment, given_width)

    assert list(the_fragment) == expected_fragment


def test_that_the_align_center_line_fragment_can_be_sliced():
    given_line_fragment = [Pixel('a'), Pixel('b')]
    given_width = 4
    the_fragment = AlignCenterLineFragment(given_line_fragment, given_width)
    assert list(the_fragment[:2]) == [Pixel(' '), Pixel('a')]
    assert list(the_fragment[1:3]) == given_line_fragment
    assert list(the_fragment[::3]) == [Pixel(' '), Pixel(' ')]