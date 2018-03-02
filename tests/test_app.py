import asyncio
import time
import pytest
from threading import Thread
from unittest.mock import Mock
from ascii_engine.app import App
from ascii_engine.screen import Screen
from tests.mocked_modules.asyncmock import AsyncMock



def create_app(model, event_loop):
    view = Mock(return_value=Mock())
    actor = Mock()
    interface = Mock()
    app = App(interface, model, view, actor)
    app.loop = event_loop
    return app


@pytest.mark.asyncio
async def test_that_given_a_view_function_it_is_called_with_the_given_initial_model(event_loop):
    initial_model = 42
    app = create_app(initial_model, event_loop)
    await event_loop.run_in_executor(None, app.start)
    app.view.assert_called_once_with(initial_model)


def test_that_when_the_app_render_is_called_it_call_the_view_and_send_the_result_to_interface(event_loop):
    initial_model = 42
    app = create_app(initial_model, event_loop)
    app.model = 13
    app.render_view()
    app.view.assert_called_with(13)
    app.interface.render.assert_called_once_with(app.view.return_value)
    app.stop()


@pytest.mark.asyncio
async def test_that_the_when_app_starts_it_renders_the_view(event_loop):
    initial_model = 42
    app = create_app(initial_model, event_loop)
    app.render_view = Mock()
    await event_loop.run_in_executor(None, app.start)
    assert app.render_view.called
    app.stop()


@pytest.mark.asyncio
async def test_that_when_an_registered_action_returns_a_value_the_action_is_called_and_the_view_is_rendered(event_loop):
    initial_model = 41
    app = create_app(initial_model, event_loop)

    await event_loop.run_in_executor(None, app.start)
    app.render_view = Mock()
    subscription = Mock()
    subscription.get_action = AsyncMock(return_value=51)
    app.register_subscription(subscription)

    await subscription.get_action.wait_for_call()
    app.actor.assert_called_with(51, initial_model)
    assert app.model == app.actor.return_value
    assert app.render_view.called
    app.stop()


@pytest.mark.asyncio
async def test_that_when_an_registered_action_is_called_until_has_no_next_action(event_loop):
    class Subscription:
        def __init__(self):
            self.calls = 3
            self.future = event_loop.create_future()

        async def get_action(self):
            self.calls -= 1
            if self.calls == 0:
                self.future.set_result(True)
            return self.calls

        def has_next(self):
            return self.calls != 0

    initial_model = 41
    app = create_app(initial_model, event_loop)

    await event_loop.run_in_executor(None, app.start)
    app.render_view = Mock()
    subscription = Subscription()
    app.register_subscription(subscription)

    await subscription.future
    assert app.actor.call_count == 3
    assert app.render_view.call_count == 3
    app.stop()


