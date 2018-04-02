from ascii_engine.elements.base import BaseElement
from ascii_engine.fragments.join import JoinVerticallyMatrixFragment


class VerticalLayout(BaseElement):
    def __init__(self, ):
        super().__init__()
        self.fragments = []

    def add(self, element):
        self.fragments.append(element.to_pixels())

    def create_fragment(self):
        return JoinVerticallyMatrixFragment(
            self.fragments
        )
