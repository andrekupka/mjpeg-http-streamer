import asyncio


class Subscription:

    def __init__(self, broker):
        self._broker = broker
        self._queue = asyncio.Queue()

    def unsubscribe(self):
        self._broker.unsubscribe(self)

    async def publish(self, frame):
        await self._queue.put(frame)

    async def get(self):
        return await self._queue.get()

    def __enter__(self):
        print("Subscribed")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Unsubscribed")
        self.unsubscribe()


class FrameBroker:

    def __init__(self, frame_queue):
        self._frame_queue = frame_queue
        self._current_frame = None
        self._subscriptions = set()

    async def run(self):
        while True:
            self._current_frame = await self._frame_queue.get()
            if self._current_frame is None:
                break
            for subscription in self._subscriptions:
                await subscription.publish(self._current_frame)

    def subscribe(self):
        subscription = Subscription(self)
        self._subscriptions.add(subscription)
        return subscription

    def unsubscribe(self, subscription):
        self._subscriptions.remove(subscription)

    @property
    def current_frame(self):
        return self._current_frame
