from ascii_engine.elements.base import BaseElement
from ascii_engine.elements.fragments import BlockPixelFragment
from ascii_engine.elements.fragments import ColorizeMultiLinePixelsFragment
from ascii_engine.elements.fragments import JoinMultiLineVerticallyFragment
from ascii_engine.elements.fragments import ColorizeMultiLinePixelsFragment


class VerticalLayout(BaseElement):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.fragments = []

    def add(self, element):
        self.fragments.append(element.to_pixels())

    def to_pixels(self):
        return ColorizeMultiLinePixelsFragment(
            BlockPixelFragment(
                JoinMultiLineVerticallyFragment(
                    *self.fragments
                ),
                self.get_width(),
                self.get_height()
            ),
            background_color=self.background_color,
        )
