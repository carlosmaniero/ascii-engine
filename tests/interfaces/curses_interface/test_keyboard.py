from unittest.mock import Mock

import pytest

from ascii_engine.interfaces.curses_interface.keyboard import CursesKeyboardSubscription
from tests.mocked_modules.curses import setup_curses


@pytest.mark.asyncio
async def test_that_curses_interface_read_the_input_from_curses(event_loop):
    setup_curses()
    keyboard = CursesKeyboardSubscription(event_loop)
    keyboard.interface.get_wch = Mock(return_value='a')

    keycode = keyboard.listen_keyboard()
    assert keycode == ord('a')
    assert keyboard.interface.get_wch.called is True


@pytest.mark.asyncio
async def test_that_curses_interface_read_the_input_from_curses_given_a_special_key(event_loop):
    keyboard = CursesKeyboardSubscription(event_loop)
    keyboard.interface.get_wch = Mock(return_value=297)

    keycode = keyboard.listen_keyboard()
    assert keycode == 297
    assert keyboard.interface.get_wch.called is True


@pytest.mark.asyncio
async def test_that_the_keyboard_subscription_get_the_keyboard_from_the_given_interface(event_loop):
    subscription = CursesKeyboardSubscription(event_loop)
    subscription.interface.get_wch = Mock(return_value=42)
    action = await subscription.get_action()
    assert subscription.interface.get_wch.called
    assert action.name == 'keypress'
    assert action.value == 42


def test_that_the_keyboard_always_returns_that_has_next_item(event_loop):
    subscription = CursesKeyboardSubscription(event_loop)
    assert subscription.has_next()