from ascii_engine.fragments.base import BaseFragment


class JoinMultiLineVerticallyFragment(BaseFragment):
    def __init__(self, *fragments):
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
