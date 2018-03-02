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
        self.loop.run_forever()

    def render_view(self):
        screen = self.view(self.model)
        self.interface.render(screen)

    def register_subscription(self, subscription):
        task = self.loop.create_task(self._call_subscription(subscription))
        self.loop.call_soon(task)

    def stop(self):
        self.loop.stop()

    async def _call_subscription(self, subscription):
        while subscription.has_next():
            action = await subscription.get_action()
            self.model = self.actor(action, self.model)
            self.render_view()
