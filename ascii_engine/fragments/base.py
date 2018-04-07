"""
A fragment is a fundamental piece of the ascii_engine.

It implements an iterable and a hashable interfaces providing a easy way to
work with pixels.

Fragments are lazy and is only perform their actions when iterated or hashed.
"""


class BaseFragment:
    """
    This is the base fragment class. When you create a Fragment you need
    basically inherit this class and create you own _apply method.

    The apply method is the method that receive a part of a given fragment
    and converts its characteristics.

    the given fragment in the construct should be anything iterable and
    hashable, it not necessarily should be a fragment object. You can see a
    example where the given fragment isn't a fragment object in the
    converter module.

    You can define the fragment size by passing the size argument in the
    constructor if it is not given, the BaseFragment will use the fragment
    length.

    Remember that, if the given size is larger than the fragment size, you
    should implement the _get_index by yourself because it by default always
    get the element by index from the fragment.
    """

    def __init__(self, fragment, size=None):
        self.__fragment = fragment

        if size:
            self.__size = size
        else:
            self.__size = len(fragment)

    def __iter__(self):
        """
        Iterate over the given fragment by calling the self._apply
        """
        for index in range(len(self)):
            yield self._get_index(index)

    def _apply(self, element_part):
        """
        Apply receive the small part of the given fragment (an element) and
        change its characteristics.
        """
        return element_part

    def get_fragment(self):
        """
        Return the given fragment
        """
        return self.__fragment

    def _get_slice(self, given_slice):
        """
        When a slice is given for the __getitem__ it calls the _get_slice that
        by default return un SliceIterableFragment that lazily slices the
        fragment.
        """
        return SliceIterableFragment(
            self,
            given_slice.start,
            given_slice.stop,
            given_slice.step
        )

    def _normalize_index(self, index):
        if abs(index) >= len(self):
            raise IndexError
        if index < 0:
            return len(self) + index
        return index

    def _get_index(self, index):
        """
        When an integer is given for the __getitem__ it calls this method
        that get the fragment element with the given index and return the
        element by applying the change described in _apply method.
        """
        return self._apply(self.get_fragment()[index])

    def __getitem__(self, item):
        """
        By default it check the item type and calls the _get_slice or
        _get_index depending if the item isn't a slice or integer it raises
        IndexError.

        I don't need to deal with negative indexes it always normalizes and
        convert to a positive one.
        """
        if isinstance(item, slice):
            return self._get_slice(item)
        elif isinstance(item, int):
            return self._get_index(
                self._normalize_index(item)
            )

        raise IndexError

    def __len__(self):
        """
        Delegates to the fragment length.
        """
        return self.__size


class SliceIterableFragment(BaseFragment):
    """
    This provide a lazy way to slice a fragment.

    Like the slice function it receives a start, a stop and a step.

    By default, all fragments returns a SliceIterableFragment instance when
    the fragment is sliced.
    """

    def __init__(self, fragment, start, stop, step):
        self.__start = start
        self.__stop = stop
        self.__step = step
        super().__init__(fragment)

    def _is_reverse(self):
        """
        Check if it's a reverse slice
        """
        return self.__step is not None and self.__step < 1

    def _calculate_start(self):
        if self._is_reverse():
            if self.__start is None:
                if self.__stop is not None and self._calculate_stop() < 0:
                    return -1
                return len(self.get_fragment()) - 1

            if self.__start < 0:
                return len(self.get_fragment()) + self.__start

        return self.__start or 0

    def _calculate_stop(self):
        """
        When the step receives a negative number and there is no stop value
        set, it assumes that the stop is -1. Where is possible to
        """
        if self.__stop is None and self._is_reverse():
            return -1

        stop = self.__stop or len(self.get_fragment())
        return min(len(self.get_fragment()), stop)

    def _calculate_step(self):
        return self.__step or 1

    def _get_range(self):
        return range(
            self._calculate_start(),
            self._calculate_stop(),
            self._calculate_step()
        )

    def _get_index(self, index):
        slice_index = self._get_range()[index]
        return self.get_fragment()[slice_index]

    def __len__(self):
        return len(self._get_range())
