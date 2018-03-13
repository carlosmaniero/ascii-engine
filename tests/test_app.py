from unittest.mock import Mock
import pytest
from tests.mocked_modules.curses import patch_curses
from ascii_engine.app import App, create_app
from ascii_engine.screen import Screen
from ascii_engine.interfaces.curses_interface.render import CursesRender


class Subscription:
    def __init__(self, event_loop, calls=3):
        self.calls = calls
        self.future = event_loop.create_future()

    async def listen(self):
        self.calls -= 1
        if self.calls == 0:
            self.future.set_result(True)
        return self.calls

    def has_next(self):
        return self.calls != 0


def create_mock_app(state, event_loop):
    draw = Mock(return_value=Mock())
    actor = Mock()
    interface = Mock()
    interface.get_subscriptions = Mock(return_value=[])
    app = App(interface, state, draw, actor)
    app.loop = event_loop
    return app


@pytest.mark.asyncio
async def test_that_given_a_draw_function_it_is_called_with_the_given_initial_state(event_loop):
    initial_state = 42
    app = create_mock_app(initial_state, event_loop)
    await event_loop.run_in_executor(None, app.start)
    app.draw.assert_called_once_with(app.interface.create_empty_screen.return_value, initial_state)


def test_that_when_the_app_render_is_called_it_call_the_draw_and_send_the_result_to_interface(event_loop):
    initial_state = 42
    screen = Screen(1, 2)
    app = create_mock_app(initial_state, event_loop)
    app.state = 13
    app.interface.create_empty_screen = Mock(return_value=screen)
    app.render_draw()
    app.draw.assert_called_with(screen, 13)
    app.interface.render.assert_called_once_with(app.draw.return_value)
    app.stop()


@pytest.mark.asyncio
async def test_that_the_when_app_starts_it_renders_the_draw(event_loop):
    initial_state = 42
    app = create_mock_app(initial_state, event_loop)
    app.render_draw = Mock()
    await event_loop.run_in_executor(None, app.start)
    assert app.render_draw.called
    app.stop()


@pytest.mark.asyncio
async def test_that_when_an_registered_action_returns_a_value_the_action_is_called_and_the_draw_is_rendered(event_loop):
    initial_state = 41
    app = create_mock_app(initial_state, event_loop)

    await event_loop.run_in_executor(None, app.start)
    app.render_draw = Mock()
    subscription = Subscription(event_loop, calls=1)
    app.register_subscription(subscription)
    await subscription.future

    assert subscription.calls == 0
    app.actor.assert_called_with(0, initial_state)
    assert app.state == app.actor.return_value
    assert app.render_draw.called
    app.stop()


@pytest.mark.asyncio
async def test_that_when_an_registered_action_is_called_until_has_no_next_action(event_loop):
    initial_state = 41
    app = create_mock_app(initial_state, event_loop)

    await event_loop.run_in_executor(None, app.start)
    app.start()
    app.render_draw = Mock()
    subscription = Subscription(event_loop)
    app.register_subscription(subscription)

    await subscription.future
    assert app.actor.call_count == 3
    assert app.render_draw.call_count == 3
    app.stop()


def test_that_loop_just_run_forever_when_it_is_not_started():
    mock_forever = Mock()
    mock_forever.is_running = Mock(return_value=False)
    app = create_mock_app(0, mock_forever)
    app.start()
    assert mock_forever.is_running.called
    assert mock_forever.run_forever.called


@patch_curses
def test_that_loop_start_app_helper_creates_an_app_with_curses_interface():
    draw = Mock()
    actor = Mock()
    state = Mock()
    app = create_app(state, draw, actor)
    assert isinstance(app.interface, CursesRender)
    assert app.actor == actor
    assert app.state == state
    assert app.draw == draw


@patch_curses
def test_that_app_returns_the_loop(event_loop):
    app = create_mock_app(1, event_loop)
    loop = Mock()
    app.loop = loop
    assert app.get_loop() == loop


