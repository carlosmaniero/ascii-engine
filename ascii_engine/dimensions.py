class Natural:
    def __init__(self, value):
        self.value = value

    def fits(self, size):
        return min(self.value, size)

    def __eq__(self, other):
        return self.value == other.value


class Percentage:
    def __init__(self, value):
        self.value = min(value, 100)

    def fits(self, size):
        return int(self.value * (size / 100))
