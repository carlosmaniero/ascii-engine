from ascii_engine.pixel import Pixel


def fragment_to_list(fragment):
    if isinstance(fragment, Pixel):
        return fragment
    return [fragment_to_list(element) for element in fragment]


class TestCaseFragmentBuilder:
    def __init__(self, fragment, expected, normalizer):
        self.fragment = fragment
        self.expected = expected
        self.normalizer = normalizer

    def assert_elements_has_the_same_length(self):
        assert len(self.fragment) == len(self.expected)

    def assert_elements_are_equals(self):
        assert self.normalizer(self.fragment) == self.expected

    def assert_elements_can_be_sliced(self):
        half = len(self.fragment) // 2
        assert self.normalizer(self.fragment[half:]) == self.expected[half:]
        assert self.normalizer(self.fragment[:half]) == self.expected[:half]
        assert self.normalizer(self.fragment[::2]) == self.expected[::2]
        assert self.normalizer(
            self.fragment[0:len(self.fragment) + 1000]
        ) == self.expected

    def run(self):
        self.assert_elements_has_the_same_length()
        self.assert_elements_are_equals()
        self.assert_elements_can_be_sliced()


def fragment_test_case(fragment, expected):
    TestCaseFragmentBuilder(fragment, expected, list).run()
