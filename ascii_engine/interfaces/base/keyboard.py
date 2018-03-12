from ascii_engine.action import Action


class KeypressAction(Action):
    def __init__(self, value, is_special=False):
        super().__init__('keypress', value)
        self._is_special = is_special

    def is_special(self):
        return self._is_special
