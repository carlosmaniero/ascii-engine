class BaseFragment:
    def __init__(self, fragment):
        self.__fragment = fragment

    def __iter__(self):
        for fragment_part in self._get_fragment():
            yield self._apply(fragment_part)

    def _apply(self, element_part):
        raise NotImplementedError

    def _get_fragment(self):
        return self.__fragment

    def _get_slice(self, given_slice):
        return SliceIterableFragment(
            self,
            given_slice.start,
            given_slice.stop,
            given_slice.step
        )

    def _get_index(self, index):
        return self._apply(self._get_fragment()[index])

    def __getitem__(self, item):
        if isinstance(item, slice):
            return self._get_slice(item)
        elif isinstance(item, int):
            return self._get_index(item)

        raise IndexError

    def __len__(self):
        return len(self._get_fragment())


class SliceIterableFragment(BaseFragment):
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
