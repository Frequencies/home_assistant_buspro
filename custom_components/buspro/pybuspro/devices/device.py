import asyncio

from .control import _ReadStatusOfChannels


def startup_read_delay(device_address, base=0.0, window=15.0):
    """Return a base delay plus deterministic-per-process jitter.

    Every device requesting its initial state at the same fixed offset causes a
    thundering-herd burst of read telegrams at startup. Spreading each device
    across a window keeps the gateway from being hammered at one instant.
    """
    jitter = (abs(hash(str(device_address))) % int(window * 10)) / 10.0
    return base + jitter


class Device(object):
    def __init__(self, buspro, device_address, name=""):
        # device_address = (subnet_id, device_id, ...)

        self._device_address = device_address
        self._buspro = buspro
        self._name = name
        self.device_updated_cbs = []
        # Hold strong references to fire-and-forget tasks. asyncio keeps only a
        # weak reference to a bare ensure_future/create_task result, so without
        # this the loop may garbage-collect the task before it completes and a
        # state update or init read is silently dropped.
        self._pending_tasks = set()

    def _spawn(self, coro):
        task = asyncio.ensure_future(coro, loop=self._buspro.loop)
        self._pending_tasks.add(task)
        task.add_done_callback(self._pending_tasks.discard)
        return task

    @property
    def name(self):
        return self._name

    @property
    def device_address(self):
        return self._device_address

    def register_telegram_received_cb(self, telegram_received_cb, postfix=None):
        self._buspro.register_telegram_received_device_cb(telegram_received_cb, self._device_address, postfix)

    def unregister_telegram_received_cb(self, telegram_received_cb, postfix=None):
        self._buspro.unregister_telegram_received_device_cb(telegram_received_cb, self._device_address, postfix)

    def register_device_updated_cb(self, device_updated_cb):
        """Register device updated callback."""
        self.device_updated_cbs.append(device_updated_cb)

    def unregister_device_updated_cb(self, device_updated_cb):
        """Unregister device updated callback."""
        try:
            self.device_updated_cbs.remove(device_updated_cb)
        except ValueError:
            pass

    async def _device_updated(self):
        # One failing listener must not prevent the others from updating.
        for device_updated_cb in list(self.device_updated_cbs):
            try:
                await device_updated_cb(self)
            except Exception:
                self._buspro.logger.exception("Error in device_updated callback")

    async def _send_telegram(self, telegram):
        await self._buspro.network_interface.send_telegram(telegram)

    # async def _send_control(self, control):
    #     await self._buspro.network_interface.send_control(control)

    def _call_device_updated(self):
        self._spawn(self._device_updated())

    def _cancel_pending_tasks(self):
        for task in tuple(self._pending_tasks):
            if not task.done():
                task.cancel()

    def close(self):
        """Release loop tasks held by this device. Subclasses also detach bus
        callbacks."""
        self._cancel_pending_tasks()

    def _call_read_current_status_of_channels(self, run_from_init=False):

        async def read_current_state_of_channels():
            if run_from_init:
                await asyncio.sleep(startup_read_delay(self._device_address, base=3))

            read_status_of_channels = _ReadStatusOfChannels(self._buspro)
            read_status_of_channels.subnet_id, read_status_of_channels.device_id = self._device_address

            await read_status_of_channels.send()

        self._spawn(read_current_state_of_channels())
