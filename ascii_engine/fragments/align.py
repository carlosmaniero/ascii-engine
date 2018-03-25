from ascii_engine.fragments.base import BaseFragment
from ascii_engine.pixel import Pixel


class AlignRightLineFragment(BaseFragment):
    """
    Align center a line.

    If the given width is lower than the fragment it keep align left.
    """
    def __init__(self, fragment, width):
        super().__init__(fragment)
        self.__width = width
        self.__start_pixel = max(self.__width - len(self._get_fragment()), 0)

    def __iter__(self):
        for index in range(self.__width):
            yield self._get_index(index)

    def _get_index(self, index):
        if index < self.__start_pixel:
            return Pixel(' ')
        else:
            return self._get_fragment()[index - self.__start_pixel]

    def __len__(self):
        return self.__width


class AlignCenterLineFragment(BaseFragment):
    """
    Align center a line.

    If the given width is lower than the fragment it keep align left.
    """
    def __init__(self, fragment, width):
        super().__init__(fragment)
        self.__width = width
        self.__start_pixel = (width - len(fragment)) // 2
        self.__end_pixel = self.__start_pixel + len(fragment) - 1

        if width < len(fragment):
            self.__start_pixel = 0
            self.__end_pixel = width

    def __iter__(self):
        for index in range(self.__width):
            yield self._get_index(index)

    def _get_index(self, index):
        if index < self.__start_pixel:
            return Pixel(' ')
        elif index > self.__end_pixel:
            return Pixel(' ')
        else:
            return self._get_fragment()[index - self.__start_pixel]

    def __len__(self):
        return self.__width
