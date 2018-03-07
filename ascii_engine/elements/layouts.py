from ascii_engine.elements.base import BaseElement
from ascii_engine.elements.fragments import VerticalFragment
from ascii_engine.elements.fragments import ColorizeMultiLinePixelsFragment


class VerticalLayout(BaseElement):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.elements = []

    def add(self, element):
        self.elements.append(element)

    def to_pixels(self):
        return ColorizeMultiLinePixelsFragment(
            VerticalFragment(
                map(lambda element: element.to_pixels(), self.elements),
                self.get_width(),
                self.get_height(),
            ),
            background_color=self.background_color,
        )
