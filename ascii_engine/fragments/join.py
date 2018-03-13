"""
This module provide ways to join fragments.
"""

from ascii_engine.fragments.base import BaseFragment


class JoinVerticallyMatrixFragment(BaseFragment):
    """
    It joins many fragments in one vertically

    >>> matrix_list_fragment = [
    >>>     [
    >>>         [Pixel('a')],
    >>>         [Pixel('b')]
    >>>     ],
    >>>     [
    >>>         [Pixel('c')],
    >>>         [Pixel('b')]
    >>>     ]
    >>> ]
    >>>
    >>> JoinVerticallyMatrixFragment(matrix_list_fragment) == [
    >>>     [Pixel('a')],
    >>>     [Pixel('b')],
    >>>     [Pixel('c')],
    >>>     [Pixel('d')]
    >>> ]
    """
    def __init__(self, fragments):
        super().__init__(fragments)

    def __iter__(self):
        for fragment in self._get_fragment():
            for line in fragment:
                yield line

    def _get_index(self, index):
        current_lenght = 0
        for fragment in self._get_fragment():
            if current_lenght + len(fragment) > index:
                return fragment[index - current_lenght]
            current_lenght += len(fragment)

        raise IndexError

    def __len__(self):
        return sum(map(len, self._get_fragment()))
