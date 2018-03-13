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
    """
    def __init__(self, fragment):
        self.__fragment = fragment

    def __iter__(self):
        """
        Iterate over the given fragment by calling the self._apply
        """
        for fragment_part in self._get_fragment():
            yield self._apply(fragment_part)

    def _apply(self, element_part):
        """
        Apply receive the small part of the given fragment (an element) and
        change its characteristics.
        """
        raise NotImplementedError

    def _get_fragment(self):
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

    def _get_index(self, index):
        """
        When an integer is given for the __getitem__ it calls this method
        that get the fragment element with the given index and return the
        element by applying the change described in _apply method.
        """
        return self._apply(self._get_fragment()[index])

    def __getitem__(self, item):
        """
        By default it check the item type and calls the _get_slice or
        _get_index depending if the item isn't a slice or integer it raises
        IndexError.
        """
        if isinstance(item, slice):
            return self._get_slice(item)
        elif isinstance(item, int):
            return self._get_index(item)

        raise IndexError

    def __len__(self):
        """
        Delegates to the fragment length.
        """
        return len(self._get_fragment())


class SliceIterableFragment(BaseFragment):
    """
    This provide a lazy way to slice a fragment.

    Like the slice function it receives a start, a stop and a step.
    """
    def __init__(self, fragment, start, stop, step):
        self.__start = start
        self.__stop = stop
        self.__step = step
        super().__init__(fragment)

    def _calculate_stop(self):
        stop = self.__stop or len(self._get_fragment())
        return min(len(self._get_fragment()), stop)

    def _calculate_start(self):
        return self.__start or 0

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
        return self._get_fragment()[slice_index]

    def __iter__(self):
        for index in self._get_range():
            yield self._get_fragment()[index]

    def __len__(self):
        return len(self._get_range())
