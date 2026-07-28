import asyncio
import logging
import socket
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN,
    CONF_HOST,
    CONF_PORT,
    CONF_SEND_PORT,
    CONF_RECEIVE_PORT,
)

_LOGGER = logging.getLogger(__name__)


def _form_schema(default_host=None, default_port=6000, default_send_port=6000, default_receive_port=6000):
    return vol.Schema({
        vol.Required(CONF_HOST, default=default_host or ""): cv.string,
        vol.Required(CONF_PORT, default=default_port): cv.port,
        vol.Optional(CONF_SEND_PORT, default=default_send_port): cv.port,
        vol.Optional(CONF_RECEIVE_PORT, default=default_receive_port): cv.port,
    })


async def _async_validate_connectivity(hass, data):
    """Validate Buspro host/port connectivity with protocol handshake."""
    host = data[CONF_HOST]
    send_port = data.get(CONF_SEND_PORT, data[CONF_PORT])
    receive_port = data.get(CONF_RECEIVE_PORT, data[CONF_PORT])

    try:
        await hass.async_add_executor_job(socket.gethostbyname, host)
    except socket.gaierror as err:
        raise InvalidHost from err

    # Protocol-level probe: start a short-lived Buspro session, send a safe
    # read request, and require at least one valid Buspro telegram.
    # This confirms we are speaking to a real Buspro gateway/bus, not just
    # an open UDP endpoint.
    from .pybuspro.buspro import Buspro
    from .pybuspro.core.telegram import Telegram
    from .pybuspro.helpers.enums import OperateCode

    buspro = Buspro(((host, send_port), ("", receive_port)), hass.loop)
    handshake = hass.loop.create_future()

    def _on_telegram(telegram):
        if handshake.done() or telegram is None or telegram.operate_code is None:
            return
        handshake.set_result(telegram)

    buspro.register_telegram_received_all_messages_cb(_on_telegram)

    try:
        await buspro.start(state_updater=False)

        probe = Telegram()
        probe.target_address = (1, 1)
        probe.operate_code = OperateCode.ReadStatusOfChannels
        probe.payload = []
        await buspro.network_interface.send_telegram(probe)

        await asyncio.wait_for(handshake, timeout=5)
    except (OSError, asyncio.TimeoutError) as err:
        raise CannotConnect from err
    finally:
        try:
            await buspro.stop()
        except Exception:
            _LOGGER.debug("Failed to stop validation Buspro transport", exc_info=True)


class CannotConnect(Exception):
    """Error to indicate we cannot connect."""


class InvalidHost(Exception):
    """Error to indicate host is invalid."""

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return BusproOptionsFlow(config_entry)

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        try:
            if user_input is not None:
                host = user_input[CONF_HOST].strip()
                if not host:
                    errors["base"] = "invalid_host"
                port = user_input[CONF_PORT]
                send_port = user_input.get(CONF_SEND_PORT, port)
                receive_port = user_input.get(CONF_RECEIVE_PORT, port)

                data = {
                    CONF_HOST: host,
                    CONF_PORT: port,
                    CONF_SEND_PORT: send_port,
                    CONF_RECEIVE_PORT: receive_port,
                }

                if not errors:
                    try:
                        await _async_validate_connectivity(self.hass, data)
                    except CannotConnect:
                        errors["base"] = "cannot_connect"
                    except InvalidHost:
                        errors["base"] = "invalid_host"
                    except Exception:  # pragma: no cover - unexpected
                        _LOGGER.exception("Unexpected exception")
                        errors["base"] = "unknown"

                if not errors:
                    await self.async_set_unique_id(f"{host.lower()}:{port}")
                    self._abort_if_unique_id_configured()

                    return self.async_create_entry(title=f"Buspro ({host})", data=data)

            default_port = 6000
            return self.async_show_form(
                step_id="user",
                data_schema=_form_schema(
                    default_host="",
                    default_port=default_port,
                    default_send_port=default_port,
                    default_receive_port=default_port,
                ),
                errors=errors,
            )
        except Exception:  # pragma: no cover - last-resort guard for HA UI stability
            _LOGGER.exception("Failed to render Buspro user config step")
            return self.async_show_form(
                step_id="user",
                data_schema=_form_schema(),
                errors={"base": "unknown"},
            )

    async def async_step_reconfigure(self, user_input=None):
        """Handle reconfiguration of an existing entry."""
        entry_id = self.context.get("entry_id")
        entry = self.hass.config_entries.async_get_entry(entry_id) if entry_id else None
        if entry is None:
            return self.async_abort(reason="reconfigure_not_supported")

        current = {**entry.data, **entry.options}
        default_host = current.get(CONF_HOST, "")
        default_port = current.get(CONF_PORT, 6000)
        default_send_port = current.get(CONF_SEND_PORT, default_port)
        default_receive_port = current.get(CONF_RECEIVE_PORT, default_port)

        try:
            if user_input is not None:
                host = user_input[CONF_HOST].strip()
                port = user_input[CONF_PORT]
                send_port = user_input.get(CONF_SEND_PORT, port)
                receive_port = user_input.get(CONF_RECEIVE_PORT, port)

                data = {
                    CONF_HOST: host,
                    CONF_PORT: port,
                    CONF_SEND_PORT: send_port,
                    CONF_RECEIVE_PORT: receive_port,
                }

                if not host:
                    return self.async_show_form(
                        step_id="reconfigure",
                        data_schema=_form_schema(host, port, send_port, receive_port),
                        errors={"base": "invalid_host"},
                    )

                try:
                    await _async_validate_connectivity(self.hass, data)
                except CannotConnect:
                    return self.async_show_form(
                        step_id="reconfigure",
                        data_schema=_form_schema(host, port, send_port, receive_port),
                        errors={"base": "cannot_connect"},
                    )
                except InvalidHost:
                    return self.async_show_form(
                        step_id="reconfigure",
                        data_schema=_form_schema(host, port, send_port, receive_port),
                        errors={"base": "invalid_host"},
                    )
                except Exception:  # pragma: no cover - unexpected
                    _LOGGER.exception("Unexpected exception")
                    return self.async_show_form(
                        step_id="reconfigure",
                        data_schema=_form_schema(host, port, send_port, receive_port),
                        errors={"base": "unknown"},
                    )

                self.hass.config_entries.async_update_entry(entry, data=data, options={})
                await self.hass.config_entries.async_reload(entry.entry_id)
                return self.async_abort(reason="reconfigure_successful")

            return self.async_show_form(
                step_id="reconfigure",
                data_schema=_form_schema(default_host, default_port, default_send_port, default_receive_port),
            )
        except Exception:  # pragma: no cover - last-resort guard for HA UI stability
            _LOGGER.exception("Failed to render Buspro reconfigure step")
            return self.async_show_form(
                step_id="reconfigure",
                data_schema=_form_schema(default_host, default_port, default_send_port, default_receive_port),
                errors={"base": "unknown"},
            )


class BusproOptionsFlow(config_entries.OptionsFlow):
    """Handle Buspro options."""

    def __init__(self, config_entry):
        super().__init__(config_entry)

    async def async_step_init(self, user_input=None):
        errors = {}
        current = {**self.config_entry.data, **self.config_entry.options}
        default_host = current.get(CONF_HOST, "")
        default_port = current.get(CONF_PORT, 6000)
        default_send_port = current.get(CONF_SEND_PORT, default_port)
        default_receive_port = current.get(CONF_RECEIVE_PORT, default_port)

        try:
            if user_input is not None:
                host = user_input[CONF_HOST].strip()
                port = user_input[CONF_PORT]
                send_port = user_input.get(CONF_SEND_PORT, port)
                receive_port = user_input.get(CONF_RECEIVE_PORT, port)

                data = {
                    CONF_HOST: host,
                    CONF_PORT: port,
                    CONF_SEND_PORT: send_port,
                    CONF_RECEIVE_PORT: receive_port,
                }

                if not host:
                    errors["base"] = "invalid_host"
                else:
                    try:
                        await _async_validate_connectivity(self.hass, data)
                    except CannotConnect:
                        errors["base"] = "cannot_connect"
                    except InvalidHost:
                        errors["base"] = "invalid_host"
                    except Exception:  # pragma: no cover - unexpected
                        _LOGGER.exception("Unexpected exception")
                        errors["base"] = "unknown"

                if not errors:
                    return self.async_create_entry(title="", data=data)

            return self.async_show_form(
                step_id="init",
                data_schema=_form_schema(default_host, default_port, default_send_port, default_receive_port),
                errors=errors,
            )
        except Exception:  # pragma: no cover - last-resort guard for HA UI stability
            _LOGGER.exception("Failed to render Buspro options step")
            return self.async_show_form(
                step_id="init",
                data_schema=_form_schema(default_host, default_port, default_send_port, default_receive_port),
                errors={"base": "unknown"},
            )
