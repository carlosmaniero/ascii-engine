"""
An event is the result of a Subscription it aways has a value.

The best way to validate the event kind is by using the isinstance function.
By example, if you want to check if the event is a keypress event you should
check by using `isinstance(event, KeypressEvent)`.
"""


class BaseEvent:
    """
    A base event it is a simple object to represent a event.
    """
    def __init__(self, value):
        self.value = value
