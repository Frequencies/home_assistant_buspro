# pybuspro

Embedded asynchronous HDL Buspro protocol library used by the Home Assistant
integration. See the [integration README](../README.md) for configuration,
supported models, entities, and migration instructions.

## Breaking API change

`Buspro` now requires an explicit `client_address`. The packet header also
accepts `advertised_ip`; direct library users should provide the IPv4 address
that the HDL gateway can route back to.

## Minimal example

```python
import asyncio

from pybuspro.buspro import Buspro


async def main():
    buspro = Buspro(
        (("192.0.2.10", 6000), ("", 6000)),
        asyncio.get_running_loop(),
        client_address=(200, 200),
        advertised_ip="192.0.2.20",
    )
    buspro.register_telegram_received_all_messages_cb(print)

    await buspro.start(state_updater=False)
    try:
        await asyncio.Event().wait()
    finally:
        await buspro.stop()


asyncio.run(main())
```

The example addresses use the documentation-only `192.0.2.0/24` network.
Choose an unused Buspro `subnet.device` client identity for each running
client. Multiple clients using the same identity can receive ambiguous
responses.

## Transport behavior

- The receive socket automatically reconnects after socket or transport errors.
- Bus silence is valid and does not trigger reconnection.
- Read-query deduplication prevents identical queries from being sent more
  than once within four seconds.
- Device coordinators should be shared per physical Buspro address to avoid
  duplicate subscriptions and status queries.
