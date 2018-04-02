from ascii_engine.elements.layouts import VerticalLayout
from ascii_engine.elements.styles import colorize
from ascii_engine.elements.text import Text
from ascii_engine.colors import RGB
from ascii_engine.pixel import Pixel
from tests.asserts import assertPixelsAreEquals


def test_texts_added_to_vertical_layout_are_rendered_after_each_other():
    layout = VerticalLayout(Text("Hello"), Text("World"))

    assertPixelsAreEquals(layout.to_pixels(), Text("Hello\nWorld").to_pixels())


def test_that_when_the_background_is_defined_it_is_used_only_in_blank_chars():
    text_bg_color = RGB(200, 100, 150)
    text_fg_color = RGB(150, 75, 37)
    layout_color = RGB(100, 50, 25)

    text1 = Text("Hi")
    text1.set_style([
        colorize(text_fg_color, text_bg_color)
    ])

    text2 = Text("Bye")
    text2.set_style([
        colorize(text_fg_color)
    ])

    text3 = Text('...')

    layout = VerticalLayout(text1, text2, text3)
    layout.set_style([
        colorize(background_color=layout_color)
    ])

    assertPixelsAreEquals(
        layout.to_pixels(),
        [
            [
                Pixel('H', text_fg_color, text_bg_color),
                Pixel('i', text_fg_color, text_bg_color),
            ],
            [
                Pixel('B', text_fg_color, layout_color),
                Pixel('y', text_fg_color, layout_color),
                Pixel('e', text_fg_color, layout_color)
            ],
            [
                Pixel('.', background_color=layout_color),
                Pixel('.', background_color=layout_color),
                Pixel('.', background_color=layout_color)
            ]
        ]
    )
