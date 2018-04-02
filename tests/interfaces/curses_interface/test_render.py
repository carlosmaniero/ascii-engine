from unittest.mock import Mock
import pytest
import time

from ascii_engine.elements.styles import colorize
from tests.mocked_modules.curses import (mocked_curses, patch_curses,
                                         setup_curses)
from ascii_engine.interfaces.curses_interface.render import CursesRender
from ascii_engine.screen import Screen
from ascii_engine.elements.text import Text
from ascii_engine.colors import RGB


DEFAULT_PAIR = 1


async def wait_for_render(curses_interface, event_loop):
    await event_loop.run_in_executor(
        curses_interface.render_interface.pool,
        time.sleep,
        0
    )


@patch_curses
def test_that_interface_is_well_configured():
    curses_interface = CursesRender()
    assert mocked_curses.initscr.called
    assert mocked_curses.start_color.called
    assert mocked_curses.noecho.called
    assert mocked_curses.cbreak.called
    curses_interface.window.keypad.assert_called_with(True)


@pytest.mark.asyncio
async def test_that_all_pixels_are_send_to_screen(event_loop):
    setup_curses()
    curses_interface = CursesRender()
    text_element = Text('ab\ncd')
    screen = Screen(2, 2)
    screen.add_element(text_element)
    curses_interface.render(screen)

    await wait_for_render(curses_interface, event_loop)

    curses_interface.window.addstr.assert_any_call(0, 0, 'a', DEFAULT_PAIR)
    curses_interface.window.addstr.assert_any_call(0, 1, 'b', DEFAULT_PAIR)
    curses_interface.window.addstr.assert_any_call(1, 0, 'c', DEFAULT_PAIR)
    curses_interface.window.addstr.assert_any_call(1, 1, 'd', DEFAULT_PAIR)


@patch_curses
def test_that_the_terminal_is_well_reconfigured_after_stop_call():
    curses_interface = CursesRender()
    curses_interface.stop()

    curses_interface.window.keypad.assert_called_with(False)
    assert mocked_curses.nocbreak.called
    assert mocked_curses.echo.called
    assert mocked_curses.endwin.called


@pytest.mark.asyncio
async def test_that_given_a_foreground_and_background_a_curses_pair_is_created(
        event_loop):
    setup_curses()
    text_element = Text('ab\ncd')
    expected_fg = RGB(0, 0, 0)
    expected_bg = RGB(128, 0, 0)
    expected_color_pair = 1
    mocked_curses.color_pair = Mock(return_value='color_1')

    text_element.set_style([
        colorize(expected_fg, expected_bg)
    ])

    screen = Screen(2, 2)
    screen.add_element(text_element)

    curses_interface = CursesRender()
    curses_interface.render(screen)

    await wait_for_render(curses_interface, event_loop)

    mocked_curses.init_pair.assert_called_once_with(
        expected_color_pair,
        expected_fg.calculate_term_color(),
        expected_bg.calculate_term_color()
    )

    curses_interface.window.addstr.assert_any_call(0, 0, 'a', 'color_1')
    curses_interface.window.addstr.assert_any_call(0, 1, 'b', 'color_1')
    curses_interface.window.addstr.assert_any_call(1, 0, 'c', 'color_1')
    curses_interface.window.addstr.assert_any_call(1, 1, 'd', 'color_1')


def test_that_the_interface_returns_the_screen_with_terminal_size():
    curses_interface = CursesRender()
    curses_interface.window = Mock()
    curses_interface.window.getmaxyx = Mock(return_value=(10, 20))
    screen = curses_interface.create_empty_screen()
    assert screen.get_width() == 19
    assert screen.get_height() == 10
