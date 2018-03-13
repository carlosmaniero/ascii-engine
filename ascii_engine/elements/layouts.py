from ascii_engine.elements.base import BaseElement
from ascii_engine.fragments.fixed import FixedMatrixFragment
from ascii_engine.fragments.colorize import ColorizeMatrixFragment
from ascii_engine.fragments.join import JoinVerticallyMatrixFragment
from ascii_engine.fragments.colorize import ColorizeMatrixFragment


class VerticalLayout(BaseElement):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.fragments = []

    def add(self, element):
        self.fragments.append(element.to_pixels())

    def to_pixels(self):
        return ColorizeMatrixFragment(
            FixedMatrixFragment(
                JoinVerticallyMatrixFragment(
                    self.fragments
                ),
                self.get_width(),
                self.get_height()
            ),
            background_color=self.background_color,
        )
