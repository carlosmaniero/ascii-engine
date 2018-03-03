import asyncio


class App:
    def __init__(self, interface, initial_model, view, actor):
        self.interface = interface
        self.model = initial_model
        self.view = view
        self.loop = asyncio.new_event_loop()
        self.actor = actor

    def start(self):
        self.render_view()
        self.register_subscriptions_from_interface()
        self._block_loop()

    def render_view(self):
        screen = self.view(self.model)
        self.interface.render(screen)

    def register_subscription(self, subscription):
        asyncio.gather(self._call_subscription(subscription), loop=self.loop)

    def register_subscriptions_from_interface(self):
        for subscription in self.interface.get_subscriptions(self.loop):
            self.register_subscription(subscription)

    def stop(self):
        self.loop.stop()

    async def _call_subscription(self, subscription):
        while subscription.has_next():
            action = await subscription.get_action()
            self.model = self.actor(action, self.model)
            self.render_view()

    def _block_loop(self):
        if not self.loop.is_running():
            self.loop.run_forever()
