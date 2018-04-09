import pytest
from unittest.mock import patch, call

from ascii_engine.colors import RGB
from ascii_engine.elements.styles import colorize, size, align_right, \
    align_center
from ascii_engine.fragments.align import AlignMatrixRightLineFragment, \
    AlignMatrixCenterLineFragment
from ascii_engine.fragments.fixed import FixedMatrixFragment
from ascii_engine.pixel import Pixel
from ascii_engine.fragments.colorize import ColorizeMatrixFragment


def param(style, fragment, args):
    return pytest.param(
        style,
        fragment,
        args,
        id=style.__name__ + ' -> ' + fragment.__name__
    )


tests_data = [
    param(colorize, ColorizeMatrixFragment, (RGB(0, 0, 0), RGB(1, 2, 3))),
    param(size, FixedMatrixFragment, (10, 20)),
    param(align_right, AlignMatrixRightLineFragment, ()),
    param(align_center, AlignMatrixCenterLineFragment, ()),
]

given_fragment = [
    [Pixel('a'), Pixel('b'), Pixel('c')]
]


@pytest.mark.parametrize('style, fragment, args', tests_data)
def test_that_the_style_configures_a_fragment(
        style, fragment, args):

    with patch.object(fragment, '__init__', return_value=None) as mocked:

        style(*args)(given_fragment)

        assert mocked.called
        assert mocked.call_args == call(given_fragment, *args)


@pytest.mark.parametrize('style, fragment, args', tests_data)
def test_that_the_style_returns_a_fragment_instance(
        style, fragment, args):

    with patch.object(fragment, '__init__', return_value=None):
        result = style(*args)(given_fragment)
        assert isinstance(result, fragment)
