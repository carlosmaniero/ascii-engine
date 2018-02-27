from unittest.mock import Mock
from tests.mocked_modules.curses import mocked_curses, patch_curses
from ascii_engine.interfaces import CursesInterface
from ascii_engine.screen import Screen
from ascii_engine.elements.text import Text
from ascii_engine.colors import RGB


DEFAULT_PAIR = 1


@patch_curses
def test_that_render_configures_the_curses_application():
    curses_interface = CursesInterface()
    curses_interface.render(Screen(10, 20))
    assert mocked_curses.initscr.called
    assert mocked_curses.start_color.called
    assert mocked_curses.noecho.called
    assert mocked_curses.cbreak.called
    curses_interface.window.keypad.assert_called_with(True)


@patch_curses
def test_that_all_pixels_are_send_to_screen():
    curses_interface = CursesInterface()
    text_element = Text('ab\ncd')
    screen = Screen(2, 2)
    screen.add_element(text_element)
    curses_interface.render(screen)

    curses_interface.window.addstr.assert_any_call(0, 0, 'a', DEFAULT_PAIR)
    curses_interface.window.addstr.assert_any_call(0, 1, 'b', DEFAULT_PAIR)
    curses_interface.window.addstr.assert_any_call(1, 0, 'c', DEFAULT_PAIR)
    curses_interface.window.addstr.assert_any_call(1, 1, 'd', DEFAULT_PAIR)


@patch_curses
def test_that_the_terminal_is_well_reconfigured_after_stop_call():
    curses_interface = CursesInterface()
    curses_interface.stop()

    curses_interface.window.keypad.assert_called_with(False)
    assert mocked_curses.nocbreak.called
    assert mocked_curses.echo.called
    assert mocked_curses.endwin.called


@patch_curses
def test_that_given_a_foreground_and_background_a_curses_pair_is_created():
    text_element = Text('ab\ncd')
    expected_fg = RGB(0, 0, 0)
    expected_bg = RGB(128, 0, 0)
    expected_color_pair = 1
    mocked_curses.color_pair = Mock(return_value='color_1')

    text_element.set_foreground_color(expected_fg)
    text_element.set_background_color(expected_bg)
    screen = Screen(2, 2)
    screen.add_element(text_element)

    curses_interface = CursesInterface()
    curses_interface.render(screen)

    mocked_curses.init_pair.assert_called_once_with(
        expected_color_pair,
        expected_fg.get_term_color(),
        expected_bg.get_term_color()
    )

    curses_interface.window.addstr.assert_any_call(0, 0, 'a', 'color_1')
    curses_interface.window.addstr.assert_any_call(0, 1, 'b', 'color_1')
    curses_interface.window.addstr.assert_any_call(1, 0, 'c', 'color_1')
    curses_interface.window.addstr.assert_any_call(1, 1, 'd', 'color_1')


@patch_curses
def test_that_curses_interface_read_the_input_from_curses():
    curses_interface = CursesInterface()
    curses_interface.window.getch = Mock(return_value=ord('a'))

    keycode = curses_interface.listen_keyboard()
    assert keycode == ord('a')
    assert curses_interface.window.getch.called is True
