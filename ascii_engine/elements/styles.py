from functools import reduce

from ascii_engine.fragments.align import AlignMatrixRightLineFragment, \
    AlignMatrixCenterLineFragment
from ascii_engine.fragments.colorize import ColorizeMatrixFragment
from ascii_engine.fragments.fixed import FixedMatrixFragment


def colorize(foreground_color=None, background_color=None):
    return lambda fragment: ColorizeMatrixFragment(
        fragment,
        foreground_color,
        background_color
    )


def size(width=None, height=None):
    return lambda fragment: FixedMatrixFragment(fragment, width, height)


def align_right():
    return lambda fragment: AlignMatrixRightLineFragment(fragment)


def align_center():
    return lambda fragment: AlignMatrixCenterLineFragment(fragment)


def display(horizontal_align='left', horizontal_size=None, vertical_size=None):
    applyers = []

    if horizontal_align == 'center':
        applyers.append(
            lambda fragment: AlignMatrixCenterLineFragment(
                fragment,
                horizontal_size
            )
        )
    if vertical_size or horizontal_size:
        applyers.append(size(horizontal_size, vertical_size))

    return lambda fragment: reduce(
        lambda current_fragment, applier: applier(current_fragment),
        applyers,
        fragment
    )
