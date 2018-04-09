import pytest

from ascii_engine.colors import RGB
from ascii_engine.elements.layouts import VerticalLayout
from ascii_engine.elements.styles import size, colorize, align_center, \
    align_right, display
from ascii_engine.elements.text import Text
from ascii_engine.fragments.align import AlignMatrixCenterLineFragment, \
    AlignMatrixRightLineFragment, AlignMatrixMiddleFragment, \
    AlignMatrixBottomFragment
from ascii_engine.fragments.colorize import ColorizeMatrixFragment
from ascii_engine.fragments.fixed import FixedMatrixFragment


def param(element):
    return pytest.param(element, id=type(element).__name__)


tests_data = [
    param(Text('Hello, World')),
    param(VerticalLayout(Text('Hello'), Text('World')))
]


@pytest.mark.parametrize('element', tests_data)
def test_element_can_be_styled_with_size(element):
    given_height = 200
    given_width = 100
    element.set_style([
        size(given_width, given_height)
    ])

    assert isinstance(element.to_pixels(), FixedMatrixFragment)
    assert element.to_pixels().get_width() == given_width
    assert element.to_pixels().get_height() == given_height


@pytest.mark.parametrize('element', tests_data)
def test_element_can_be_styled_with_align_center(element):
    element.set_style([
        align_center()
    ])

    assert isinstance(element.to_pixels(), AlignMatrixCenterLineFragment)


@pytest.mark.parametrize('element', tests_data)
def test_element_can_be_styled_with_align_right(element):
    element.set_style([
        align_right()
    ])

    assert isinstance(element.to_pixels(), AlignMatrixRightLineFragment)


@pytest.mark.parametrize('element', tests_data)
def test_element_can_be_styled_with_colors(element):
    given_fg = RGB(2, 3, 4)
    given_bg = RGB(1, 2, 3)

    element.set_style([
        colorize(given_fg, given_bg)
    ])

    assert isinstance(element.to_pixels(), ColorizeMatrixFragment)
    assert element.to_pixels().get_background_color() == given_bg
    assert element.to_pixels().get_foreground_color() == given_fg


@pytest.mark.parametrize('element', tests_data)
def test_element_style_is_applied_in_the_given_order(element):
    element.set_style([
        size(100, 300),
        align_right(),
        colorize(RGB(0, 0, 0), RGB(0, 0, 0))
    ])

    assert isinstance(
        element.to_pixels(),
        ColorizeMatrixFragment
    )
    assert isinstance(
        element.to_pixels().get_fragment(),
        AlignMatrixRightLineFragment
    )
    assert isinstance(
        element.to_pixels().get_fragment().get_fragment(),
        FixedMatrixFragment
    )


@pytest.mark.parametrize('element', tests_data)
def test_element_is_centered_given_the_display_style(element):
    element.set_style([
        display(horizontal_align='center', horizontal_size=100),
    ])

    assert isinstance(
        element.to_pixels(),
        AlignMatrixCenterLineFragment
    )
    assert element.to_pixels().get_width() == 100


@pytest.mark.parametrize('element', tests_data)
def test_element_is_centered_and_blocked_using_display(element):
    element.set_style([
        display(
            horizontal_align='center',
            horizontal_size=100,
            vertical_size=200
        ),
    ])

    assert isinstance(
        element.to_pixels(),
        FixedMatrixFragment
    )
    assert len(element.to_pixels()) == 200

    assert isinstance(
        element.to_pixels().get_fragment(),
        AlignMatrixCenterLineFragment
    )
    assert element.to_pixels().get_fragment().get_width() == 100


@pytest.mark.parametrize('element', tests_data)
def test_element_is_aligned_right_given_the_display_style(element):
    element.set_style([
        display(horizontal_align='right'),
    ])

    assert isinstance(
        element.to_pixels(),
        AlignMatrixRightLineFragment
    )


@pytest.mark.parametrize('element', tests_data)
def test_element_is_aligned_right_given_the_display_style(element):
    element.set_style([
        display(horizontal_align='right'),
    ])

    assert isinstance(
        element.to_pixels(),
        AlignMatrixRightLineFragment
    )


@pytest.mark.parametrize('element', tests_data)
def test_element_is_aligned_right_with_a_given_width(element):
    element.set_style([
        display(horizontal_align='right', horizontal_size=100),
    ])

    assert isinstance(
        element.to_pixels(),
        AlignMatrixRightLineFragment
    )

    assert element.to_pixels().get_width() == 100


@pytest.mark.parametrize('element', tests_data)
def test_element_has_fixed_width_using_display(element):
    element.set_style([
        display(
            horizontal_size=100
        ),
    ])

    assert isinstance(
        element.to_pixels(),
        FixedMatrixFragment
    )
    assert element.to_pixels().get_width() == 100


@pytest.mark.parametrize('element', tests_data)
def test_element_is_put_on_middle_and_blocked_using_display(element):
    element.set_style([
        display(vertical_align='middle', vertical_size=100),
    ])

    assert isinstance(
        element.to_pixels(),
        AlignMatrixMiddleFragment
    )
    assert element.to_pixels().get_height() == 100


@pytest.mark.parametrize('element', tests_data)
def test_element_align_is_ignored_when_there_is_no_vertical_size(element):
    element.set_style([
        display(vertical_align='middle'),
    ])

    assert not isinstance(
        element.to_pixels(),
        AlignMatrixMiddleFragment
    )


@pytest.mark.parametrize('element', tests_data)
def test_element_is_put_on_bottom_and_blocked_using_display(element):
    element.set_style([
        display(vertical_align='bottom', vertical_size=100),
    ])

    assert isinstance(
        element.to_pixels(),
        AlignMatrixBottomFragment
    )
    assert element.to_pixels().get_height() == 100


@pytest.mark.parametrize('element', tests_data)
def test_element_align_is_ignored_when_there_is_no_vertical_size(element):
    element.set_style([
        display(vertical_align='bottom'),
    ])

    assert not isinstance(
        element.to_pixels(),
        AlignMatrixBottomFragment
    )
