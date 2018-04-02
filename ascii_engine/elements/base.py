class BaseElement:
    def __init__(self):
        self.styles = []

    def set_style(self, styles):
        self.styles = styles

    def create_fragment(self):
        raise NotImplementedError

    def to_pixels(self):
        fragment = self.create_fragment()
        for style in self.styles:
            fragment = style(fragment)

        return fragment
