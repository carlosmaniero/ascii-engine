from ascii_engine.fragments.colorize import ColorizeMatrixFragment


def colorize(foreground_color=None, background_color=None):
    return lambda fragment: ColorizeMatrixFragment(
        fragment,
        foreground_color,
        background_color
    )
