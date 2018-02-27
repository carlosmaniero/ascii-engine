from unittest.mock import Mock
import sys
import types

curses_module_name = 'curses'
mocked_curses = types.ModuleType(curses_module_name)
sys.modules[curses_module_name] = mocked_curses


mocked_curses.initscr = Mock(name=curses_module_name + '.initscr')
mocked_curses.echo = Mock(name=curses_module_name + '.echo')
mocked_curses.noecho = Mock(name=curses_module_name + '.noecho')
mocked_curses.cbreak = Mock(name=curses_module_name + '.cbreak')
mocked_curses.nocbreak = Mock(name=curses_module_name + '.nocbreak')
mocked_curses.endwin = Mock(name=curses_module_name + '.endwin')
