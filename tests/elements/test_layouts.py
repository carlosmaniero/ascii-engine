from ascii_engine.elements.layouts import VerticalLayout
from ascii_engine.elements.text import Text
from ascii_engine.colors import RGB
from ascii_engine.pixel import Pixel
from tests.asserts import assertPixelsAreEquals


def test_texts_added_to_vertical_layout_are_rendered_after_each_other():
    layout = VerticalLayout(5, 2)
    layout.add(Text("Hello"))
    layout.add(Text("World"))

    assertPixelsAreEquals(layout.to_pixels(), Text("Hello\nWorld").to_pixels())


def test_that_when_the_background_is_defined_it_is_used_only_in_blank_chars():
    text_bg_color = RGB(200, 100, 150)
    text_fg_color = RGB(150, 75, 37)
    layout_color = RGB(100, 50, 25)

    text1 = Text("Hi")
    text1.set_background_color(text_bg_color)
    text1.set_foreground_color(text_fg_color)

    text2 = Text("Bye")
    text2.set_foreground_color(text_fg_color)

    text3 = Text('...')

    layout = VerticalLayout(3, 4)
    layout.add(text1)
    layout.add(text2)
    layout.add(text3)
    layout.set_background_color(layout_color)

    assertPixelsAreEquals(
        layout.to_pixels(),
        [
            [
                Pixel('H', foreground_color=text_fg_color, background_color=text_bg_color),
                Pixel('i', foreground_color=text_fg_color, background_color=text_bg_color),
                Pixel(' ', background_color=layout_color)
            ],
            [
                Pixel('B', foreground_color=text_fg_color, background_color=layout_color),
                Pixel('y', foreground_color=text_fg_color, background_color=layout_color),
                Pixel('e', foreground_color=text_fg_color, background_color=layout_color)
            ],
            [
                Pixel('.', background_color=layout_color),
                Pixel('.', background_color=layout_color),
                Pixel('.', background_color=layout_color)
            ],
            [
                Pixel(' ', background_color=layout_color),
                Pixel(' ', background_color=layout_color),
                Pixel(' ', background_color=layout_color)
            ]
        ]
    )
