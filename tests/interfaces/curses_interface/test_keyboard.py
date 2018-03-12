from unittest.mock import Mock

import pytest

from ascii_engine.interfaces.curses_interface.keyboard import CursesKeyboardSubscription
from tests.mocked_modules.curses import setup_curses


@pytest.mark.asyncio
async def test_that_curses_interface_read_the_input_from_curses(event_loop):
    setup_curses()
    keyboard = CursesKeyboardSubscription(event_loop)
    keyboard.interface.get_wch = Mock(return_value='a')

    action = keyboard.listen_keyboard()
    assert action.value == ord('a')
    assert keyboard.interface.get_wch.called is True


@pytest.mark.asyncio
async def test_that_curses_interface_read_the_input_from_curses_given_a_special_key(event_loop):
    keyboard = CursesKeyboardSubscription(event_loop)
    keyboard.interface.get_wch = Mock(return_value=297)

    action = keyboard.listen_keyboard()
    assert action.value == 297
    assert keyboard.interface.get_wch.called


@pytest.mark.asyncio
async def test_that_the_keyboard_subscription_return_an_action_given_a_char(event_loop):
    subscription = CursesKeyboardSubscription(event_loop)
    subscription.interface.get_wch = Mock(return_value='a')
    action = await subscription.get_action()
    assert subscription.interface.get_wch.called
    assert action.name == 'keypress'
    assert action.value == ord('a')
    assert not action.is_special()


@pytest.mark.asyncio
async def test_that_the_keyboard_subscription_return_an_action_given_a_special_key(event_loop):
    subscription = CursesKeyboardSubscription(event_loop)
    subscription.interface.get_wch = Mock(return_value=260)
    action = await subscription.get_action()
    assert subscription.interface.get_wch.called
    assert action.name == 'keypress'
    assert action.value == 260
    assert action.is_special()


def test_that_the_keyboard_always_returns_that_has_next_item(event_loop):
    subscription = CursesKeyboardSubscription(event_loop)
    assert subscription.has_next()
