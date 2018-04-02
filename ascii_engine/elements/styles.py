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
