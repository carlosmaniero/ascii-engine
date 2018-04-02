from ascii_engine.pixel import Pixel
from ascii_engine.fragments.align import AlignRightLineFragment, \
    AlignCenterLineFragment


def test_that_the_align_right_slices_the_blank_part():
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


def test_that_the_align_right_truncates_the_given_fragment_on_the_left():
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


def test_that_the_align_center_put_keep_pixels_left_given_odd_width():
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
