"""
This module provide ways to join fragments.
"""

from ascii_engine.fragments.base import BaseFragment
from ascii_engine.fragments.utils import calculate_fragments_length_sum


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
        length = calculate_fragments_length_sum(fragments)
        super().__init__(fragments, length)

    def __iter__(self):
        for fragment in self.get_fragment():
            for line in fragment:
                yield line

    def _get_index(self, index):
        current_length = 0
        for fragment in self.get_fragment():
            if current_length + len(fragment) > index:
                return fragment[index - current_length]
            current_length += len(fragment)
