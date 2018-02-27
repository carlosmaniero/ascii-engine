from unittest.mock import Mock
from functools import wraps
import sys
import types

curses_module_name = 'curses'
mocked_curses = types.ModuleType(curses_module_name)
mocked_curses.initscr = Mock(name=curses_module_name + '.initscr')

sys.modules[curses_module_name] = mocked_curses


def patch_curses(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        mocked_curses.initscr = Mock(name=curses_module_name + '.initscr')
        mocked_curses.start_color = Mock(name=curses_module_name + '.start_color')
        mocked_curses.echo = Mock(name=curses_module_name + '.echo')
        mocked_curses.noecho = Mock(name=curses_module_name + '.noecho')
        mocked_curses.cbreak = Mock(name=curses_module_name + '.cbreak')
        mocked_curses.nocbreak = Mock(name=curses_module_name + '.nocbreak')
        mocked_curses.endwin = Mock(name=curses_module_name + '.endwin')
        mocked_curses.init_pair = Mock(name=curses_module_name + '.init_pair')
        mocked_curses.color_pair = Mock(name=curses_module_name + '.color_pair', return_value=1)
        fn(*args, **kwargs)

    return wrapper
