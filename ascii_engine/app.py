"""
This module provides the full architecture to create an event based program
using the ascii_engine.

An App is composed by three parts a state, a draw and an actor.

The state is the state of your application. It could be what you want to.

The actor is a function thar receives your state and an Event. It will
return a new state.

By example. Let's suppose that your model is a simple integer and when
a KeypressEvent is performed you will increase the state.

>>> from ascii_engine.interfaces.base.keyboard import KeypressEvent
>>>
>>> def actor(state, action):
>>>     if isinstance(action, KeypressEvent):
>>>         return state + 1
>>>     return state

A draw is a function that receives a blank scene and the application state
and return the scene that could be rendered.

>>> from ascii_engine.elements.text import Text
>>>
>>> def draw(scene, state):
>>>     if state == 0:
>>>         scene.add_element(Text('Press any key'))
>>>     elif state == 1:
>>>         scene.add_element(Text("You pressed one key"format(state)))
>>>     else:
>>>         scene.add_element(Text("You pressed: {} keys".format(state)))
>>>     return scene

Now that we have our actor and state, we can start our application by using
the create_app helper.

>>> from ascii_engine.interfaces.curses_interface.keyboard import (
>>>     CursesKeyboardSubscription
>>> )
>>>
>>> app = create_app(initial_model=0, draw=draw, actor=actor)

You Can so register the subscriptions. In our example we are using the
keyboard subscription.

Subscriptions generates an event that will be used by actor.

>>> keyboard_subscription = CursesKeyboardSubscription(app.get_loop()
>>> app.register_subscription(keyboard_subscription)

After it we can finally start our application.

It will call our draw function with the initial model and render it on the
screen.
>>> app.start()

When the app is started it blocks forever.
"""
import asyncio
from ascii_engine.interfaces.curses_interface.render import CursesRender


class App:
    """
    The App creates the render ecosystem based on events.

    Each event generated by the subscriptions generates an actor call and
    the model returned by actor is used to render the screen using the draw.

    It's possible to define the render interface. When the create_app is
    called by default it uses the CursesInterface.
    """
    def __init__(self, interface, initial_state, draw, actor):
        self.interface = interface
        self.state = initial_state
        self.draw = draw
        self.loop = asyncio.new_event_loop()
        self.actor = actor

    def start(self):
        """
        Start the main loop blocking the application until the stop method
        be called.
        """
        self.render_draw()
        self._block_loop_safely()

    def render_draw(self):
        """
        Render the given draw with the current state using the given
        interface.
        """
        screen = self.interface.create_empty_screen()
        screen_to_render = self.draw(screen, self.state)
        self.interface.render(screen_to_render)

    def register_subscription(self, subscription):
        """
        Register a subscription in the application the application will be
        listened until the subscription.has_next() returns False.
        """
        subscription_coroutine = self._call_subscription(subscription)
        asyncio.ensure_future(subscription_coroutine, loop=self.loop)

    def stop(self):
        """
        Stop the application by stopping the loop.
        """
        self.loop.stop()

    def get_loop(self):
        """
        Get the application asyncio event loop.
        """
        return self.loop

    async def _call_subscription(self, subscription):
        while subscription.has_next():
            event = await subscription.listen()
            self.state = self.actor(event, self.state)
            self.render_draw()

    def _block_loop_safely(self):
        if not self.loop.is_running():
            self.loop.run_forever()


def create_app(initial_model, draw, actor):
    return App(CursesRender(), initial_model, draw, actor)
