from unittest.mock import Mock
import pytest
from tests.mocked_modules.curses import patch_curses
from ascii_engine.app import App, create_app
from ascii_engine.screen import Screen
from ascii_engine.interfaces import CursesInterface


class Subscription:
    def __init__(self, event_loop, calls=3):
        self.calls = calls
        self.future = event_loop.create_future()

    async def get_action(self):
        self.calls -= 1
        if self.calls == 0:
            self.future.set_result(True)
        return self.calls

    def has_next(self):
        return self.calls != 0


def create_mock_app(model, event_loop):
    draw = Mock(return_value=Mock())
    actor = Mock()
    interface = Mock()
    interface.get_subscriptions = Mock(return_value=[])
    app = App(interface, model, draw, actor)
    app.loop = event_loop
    return app


@pytest.mark.asyncio
async def test_that_given_a_draw_function_it_is_called_with_the_given_initial_model(event_loop):
    initial_model = 42
    app = create_mock_app(initial_model, event_loop)
    await event_loop.run_in_executor(None, app.start)
    app.draw.assert_called_once_with(app.interface.get_screen.return_value, initial_model)


@pytest.mark.asyncio
async def test_that_it_register_all_interfaces_subscription(event_loop):
    initial_model = 42
    app = create_mock_app(initial_model, event_loop)
    app.interface.get_subscriptions = Mock(return_value=[
        Subscription(event_loop),
        Subscription(event_loop),
        Subscription(event_loop)
    ])
    await event_loop.run_in_executor(None, app.start)
    await app.interface.get_subscriptions.return_value[2].future

    assert app.interface.get_subscriptions.called
    assert app.interface.get_subscriptions.return_value[0].calls == 0
    assert app.interface.get_subscriptions.return_value[1].calls == 0
    assert app.interface.get_subscriptions.return_value[2].calls == 0


def test_that_when_the_app_render_is_called_it_call_the_draw_and_send_the_result_to_interface(event_loop):
    initial_model = 42
    screen = Screen(1, 2)
    app = create_mock_app(initial_model, event_loop)
    app.model = 13
    app.interface.get_screen = Mock(return_value=screen)
    app.render_draw()
    app.draw.assert_called_with(screen, 13)
    app.interface.render.assert_called_once_with(app.draw.return_value)
    app.stop()


@pytest.mark.asyncio
async def test_that_the_when_app_starts_it_renders_the_draw(event_loop):
    initial_model = 42
    app = create_mock_app(initial_model, event_loop)
    app.render_draw = Mock()
    await event_loop.run_in_executor(None, app.start)
    assert app.render_draw.called
    app.stop()


@pytest.mark.asyncio
async def test_that_when_an_registered_action_returns_a_value_the_action_is_called_and_the_draw_is_rendered(event_loop):
    initial_model = 41
    app = create_mock_app(initial_model, event_loop)

    await event_loop.run_in_executor(None, app.start)
    app.render_draw = Mock()
    subscription = Subscription(event_loop, calls=1)
    app.register_subscription(subscription)
    await subscription.future

    assert subscription.calls == 0
    app.actor.assert_called_with(0, initial_model)
    assert app.model == app.actor.return_value
    assert app.render_draw.called
    app.stop()


@pytest.mark.asyncio
async def test_that_when_an_registered_action_is_called_until_has_no_next_action(event_loop):
    initial_model = 41
    app = create_mock_app(initial_model, event_loop)

    # await event_loop.run_in_executor(None, app.start)
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
    model = Mock()
    app = create_app(model, draw, actor)
    assert isinstance(app.interface, CursesInterface)
    assert app.actor == actor
    assert app.model == model
    assert app.draw == draw
