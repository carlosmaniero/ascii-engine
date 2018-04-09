from functools import reduce

from ascii_engine.fragments.align import AlignMatrixRightLineFragment, \
    AlignMatrixCenterLineFragment, AlignMatrixMiddleFragment, \
    AlignMatrixBottomFragment
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


def display(horizontal_align='left', horizontal_size=None,
            vertical_align='top', vertical_size=None):
    applyers = []

    if horizontal_align == 'center':
        applyers.append(
            lambda fragment: AlignMatrixCenterLineFragment(
                fragment,
                horizontal_size
            )
        )
    elif horizontal_align == 'right':
        applyers.append(
            lambda fragment: AlignMatrixRightLineFragment(
                fragment,
                horizontal_size
            )
        )

    if vertical_align == 'middle' and vertical_size is not None:
        applyers.append(
            lambda fragment: AlignMatrixMiddleFragment(
                fragment,
                vertical_size
            )
        )
    elif vertical_align == 'bottom' and vertical_size is not None:
        applyers.append(
            lambda fragment: AlignMatrixBottomFragment(
                fragment,
                vertical_size
            )
        )

    default_horizontal_align = horizontal_align not in ('center', 'right')
    fixed_width = horizontal_size is not None and default_horizontal_align

    default_vertical_align = vertical_align not in ('middle', 'bottom')
    fixed_height = vertical_size is not None and default_vertical_align

    if fixed_width or fixed_height:
        applyers.append(size(horizontal_size, vertical_size))

    return lambda fragment: reduce(
        lambda current_fragment, applier: applier(current_fragment),
        applyers,
        fragment
    )
