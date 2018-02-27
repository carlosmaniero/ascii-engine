from tests.mocked_modules.curses import mocked_curses
from ascii_engine.interfaces import curses_interface
from ascii_engine.screen import Screen
from ascii_engine.elements.text import Text


def test_that_render_configures_the_curses_application():
    curses_interface.render(Screen(10, 20))
    assert mocked_curses.initscr.called
    assert mocked_curses.noecho.called
    assert mocked_curses.cbreak.called
    curses_interface.window.keypad.assert_called_with(True)


def test_that_all_pixels_are_send_to_screen():
    text_element = Text('ab\ncd')
    screen = Screen(2, 2)
    screen.add_element(text_element)
    curses_interface.render(screen)

    curses_interface.window.addch.assert_any_call(0, 0, ord('a'))
    curses_interface.window.addch.assert_any_call(0, 1, ord('b'))
    curses_interface.window.addch.assert_any_call(1, 0, ord('c'))
    curses_interface.window.addch.assert_any_call(1, 1, ord('d'))


def test_that_the_terminal_is_well_reconfigured_after_stop_call():
    curses_interface.stop()

    curses_interface.window.keypad.assert_called_with(False)
    assert mocked_curses.nocbreak.called
    assert mocked_curses.echo.called
    assert mocked_curses.endwin.called
