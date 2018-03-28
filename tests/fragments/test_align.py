from ascii_engine.pixel import Pixel
from ascii_engine.fragments.align import AlignRightLineFragment, \
    AlignCenterLineFragment


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


def test_that_the_align_center_line_put_the_fragment_one_pixel_left_when_the_width_is_odd():
    given_line_fragment = [Pixel('a'), Pixel('b')]
    given_width = 5
    expected_fragment = [
        Pixel(' '), Pixel('a'), Pixel('b'), Pixel(' '), Pixel(' ')
    ]

    the_fragment = AlignCenterLineFragment(given_line_fragment, given_width)

    assert list(the_fragment) == expected_fragment


def test_that_the_align_center_truncates_from_the_init():
    given_line_fragment = [Pixel('a'), Pixel('b'), Pixel('c'), Pixel('d')]
    given_width = 2
    expected_fragment = [Pixel('a'), Pixel('b')]

    the_fragment = AlignCenterLineFragment(given_line_fragment, given_width)

    assert list(the_fragment) == expected_fragment
