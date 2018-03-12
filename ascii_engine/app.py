import asyncio
from ascii_engine.interfaces import CursesInterface


class App:
    def __init__(self, interface, initial_model, draw, actor):
        self.interface = interface
        self.model = initial_model
        self.draw = draw
        self.loop = asyncio.new_event_loop()
        self.actor = actor

    def start(self):
        self.render_draw()
        self._block_loop()

    def render_draw(self):
        screen = self.interface.get_screen()
        screen_to_render = self.draw(screen, self.model)
        self.interface.render(screen_to_render)

    def register_subscription(self, subscription):
        subscription_coro = self._call_subscription(subscription)
        asyncio.ensure_future(subscription_coro, loop=self.loop)

    def stop(self):
        self.loop.stop()

    def get_loop(self):
        return self.loop

    async def _call_subscription(self, subscription):
        while subscription.has_next():
            action = await subscription.get_action()
            self.model = self.actor(action, self.model)
            self.render_draw()

    def _block_loop(self):
        if not self.loop.is_running():
            self.loop.run_forever()


def create_app(initial_model, draw, actor):
    return App(CursesInterface(), initial_model, draw, actor)
