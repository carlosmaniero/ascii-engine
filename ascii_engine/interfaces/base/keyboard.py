from ascii_engine.event import BaseEvent


class KeypressEvent(BaseEvent):
    def __init__(self, value, is_special=False):
        super().__init__(value)
        self._is_special = is_special

    def is_special(self):
        return self._is_special
