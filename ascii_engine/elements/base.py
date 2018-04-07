import abc


class BaseElement(metaclass=abc.ABCMeta):
    def __init__(self):
        self.styles = []

    def set_style(self, styles):
        self.styles = styles

    @abc.abstractmethod
    def create_fragment(self):
        """
        This method should return the fragment of the element;

        The fragment returned from this method will be applied to the given
        styles in the `to_pixels` function.
        """

    def to_pixels(self):
        fragment = self.create_fragment()
        for style in self.styles:
            fragment = style(fragment)

        return fragment
