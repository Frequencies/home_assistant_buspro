import asyncio
import logging
import socket
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_ADDRESS, CONF_MODEL, CONF_NAME
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers import device_registry as dr, entity_registry as er
from homeassistant.helpers import selector, translation as ha_translation

from .const import (
    CONF_CHANNEL_COUNT,
    CONF_CLIENT_ADDRESS,
    CONF_CHANNEL_NUMBER,
    CONF_CHANNELS,
    CONF_DEVICE_TYPE,
    DATA_BUSPRO_CONFIG,
    DEVICE_TYPE_COVER,
    DEVICE_TYPE_DIMMER,
    DEVICE_TYPE_RELAY,
    DEVICE_TYPE_UNIVERSAL_SWITCH,
    DOMAIN,
    CONF_HOST,
    CONF_MANAGED_DEVICES,
    CONF_PORT,
    CONF_SEND_PORT,
    CONF_RECEIVE_PORT,
    DEFAULT_CLIENT_ADDRESS,
)
from .catalog import DEVICE_CATALOG
from .managed import (
    DEVICE_TYPE_LABELS,
    build_channels,
    managed_devices,
    models_for_type,
    validate_physical_address,
    fixed_channel_count,
    removed_managed_unique_ids,
)
from .helpers.entity import channel_number_from_unique_id
from .helpers.network import local_ip_for_gateway

_LOGGER = logging.getLogger(__name__)
CONF_REMOVE_DEVICE = "remove_device"
_MANUAL_ENTRY = "__manual__"


async def _flow_translations(hass, category: str) -> dict[str, str]:
    """Fetch flow translations for the active HA language."""
    return await ha_translation.async_get_translations(
        hass, hass.config.language, category, {DOMAIN}
    )


def _t(translations: dict[str, str], key: str, default: str) -> str:
    """Return translated string or English default."""
    return translations.get(f"component.{DOMAIN}.{key}", default)



# --- bus-scan helpers --------------------------------------------------------

def _infer_device_type(dev) -> str | None:
    """Map scan traffic patterns to a managed device type, or None if unknown."""
    op = dev.op_codes
    if "ReadStatusofCurtainSwitchResponse" in op or "CurtainSwitchControlResponse" in op:
        return DEVICE_TYPE_COVER
    if "ReadStatusOfUniversalSwitchResponse" in op:
        return DEVICE_TYPE_UNIVERSAL_SWITCH
    if "ReadStatusOfChannelsResponse" in op or "SingleChannelControlResponse" in op:
        return DEVICE_TYPE_DIMMER if dev.dimmer_evidence else DEVICE_TYPE_RELAY
    return None


def _pick_model(device_type: str, channel_count: int | None) -> str | None:
    """Pick the best-fit catalog model for a discovered device."""
    _GENERIC_MODELS = {
        DEVICE_TYPE_COVER: "HDL Buspro Curtain Controller",
        DEVICE_TYPE_UNIVERSAL_SWITCH: "HDL Buspro Universal Switch",
    }
    if device_type in _GENERIC_MODELS:
        return _GENERIC_MODELS[device_type]

    # For relay/dimmer: pick smallest fixed model with channels >= discovered count.
    candidates = [
        (model, spec)
        for model, spec in DEVICE_CATALOG.items()
        if spec.get(CONF_DEVICE_TYPE) == device_type
        and not spec.get("configurable_channels", False)
        and not spec.get("generic", False)
        and "channels" in spec
    ]
    if not candidates:
        return None
    if channel_count:
        fitting = [
            (m, s) for m, s in candidates
            if int(s["channels"]) >= channel_count
        ]
        if fitting:
            return min(fitting, key=lambda ms: int(ms[1]["channels"]))[0]
    return min(candidates, key=lambda ms: int(ms[1]["channels"]))[0]


def _scan_device_label(dev, type_label: str, model: str, ch_fmt: str) -> str:
    """One-line label for the scan checklist."""
    ch = f", {ch_fmt.format(count=dev.channel_count)}" if dev.channel_count else ""
    return f"{dev.address} — {type_label}{ch} ({model})"


def _build_managed_device(dev, device_type: str, model: str, type_label: str) -> dict:
    """Build a managed-device record from a discovered device."""
    spec = DEVICE_CATALOG[model]
    name = f"{type_label} {dev.address}"

    if "capabilities" in spec:
        channel_keys = list(spec["capabilities"])
        channel_count = len(channel_keys)
    elif spec.get("configurable_channels", False):
        channel_count = dev.channel_count or 1
        channel_keys = list(range(1, channel_count + 1))
    else:
        channel_count = int(spec["channels"])
        channel_keys = list(range(1, channel_count + 1))

    names = {key: f"{name} {key}" for key in channel_keys}
    channels = build_channels(dev.address, device_type, name, channel_keys, names, {})

    return {
        CONF_ADDRESS: dev.address,
        CONF_NAME: name,
        CONF_MODEL: model,
        CONF_DEVICE_TYPE: device_type,
        CONF_CHANNEL_COUNT: channel_count,
        CONF_CHANNELS: channels,
    }


def _form_schema(
    default_host=None,
    default_port=6000,
    default_send_port=6000,
    default_receive_port=6000,
    default_client_address=DEFAULT_CLIENT_ADDRESS,
):
    return vol.Schema({
        vol.Required(CONF_HOST, default=default_host or ""): cv.string,
        vol.Required(CONF_PORT, default=default_port): cv.port,
        vol.Optional(CONF_SEND_PORT, default=default_send_port): cv.port,
        vol.Optional(CONF_RECEIVE_PORT, default=default_receive_port): cv.port,
        vol.Required(
            CONF_CLIENT_ADDRESS, default=default_client_address
        ): cv.string,
    })


async def _async_validate_connectivity(hass, data, probe_socket=True):
    """Validate Buspro network settings without assuming a device address.

    When an entry is already loaded it holds the receive socket; binding a
    second one on the same port would falsely fail. Callers in that situation
    pass ``probe_socket=False`` to validate host/client only.
    """
    host = data[CONF_HOST]
    send_port = data.get(CONF_SEND_PORT, data[CONF_PORT])
    receive_port = data.get(CONF_RECEIVE_PORT, data[CONF_PORT])
    client_address = validate_physical_address(data[CONF_CLIENT_ADDRESS])
    if client_address is None:
        raise InvalidClientAddress

    try:
        await hass.async_add_executor_job(socket.gethostbyname, host)
    except socket.gaierror as err:
        raise InvalidHost from err

    if not probe_socket:
        return

    # UDP has no connection handshake. Validate that the local receive socket
    # can be created without assuming a physical device exists at any address.
    from .pybuspro.buspro import Buspro

    buspro = None
    try:
        route_ip = await hass.async_add_executor_job(
            local_ip_for_gateway, host, send_port
        )
        buspro = Buspro(
            ((host, send_port), ("", receive_port)),
            asyncio.get_running_loop(),
            client_address=tuple(
                int(part) for part in client_address.split(".")
            ),
            advertised_ip=route_ip,
        )
        await buspro.start(state_updater=False)
        if buspro.network_interface.udp_client.transport is None:
            raise CannotConnect
    except OSError as err:
        raise CannotConnect from err
    finally:
        try:
            if buspro is not None:
                await buspro.stop()
        except Exception:
            _LOGGER.debug("Failed to stop validation Buspro transport", exc_info=True)


class CannotConnect(Exception):
    """Error to indicate we cannot connect."""


class InvalidHost(Exception):
    """Error to indicate host is invalid."""


class InvalidClientAddress(Exception):
    """Error to indicate the Buspro client identity is invalid."""


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return BusproOptionsFlow(config_entry)

    async def async_step_user(self, user_input=None):
        """Discover gateways on the LAN and let the user pick one or enter manually."""
        if not hasattr(self, "_discovered_gateways"):
            from .gateway_discovery import async_discover_gateways
            try:
                self._discovered_gateways = await async_discover_gateways(self.hass)
            except Exception:  # noqa: BLE001
                _LOGGER.debug("Gateway discovery failed", exc_info=True)
                self._discovered_gateways = []

        if not self._discovered_gateways:
            return await self.async_step_manual()

        if user_input is not None:
            selected = user_input.get("gateway", _MANUAL_ENTRY)
            if selected != _MANUAL_ENTRY:
                self._prefill_host = selected
            return await self.async_step_manual()

        t = await _flow_translations(self.hass, "selector")
        manual_label = _t(t, "selector.gateway_selection.options.__manual__", "Enter IP manually")
        options = [
            selector.SelectOptionDict(value=gw.ip, label=gw.label)
            for gw in self._discovered_gateways
        ]
        options.append(
            selector.SelectOptionDict(value=_MANUAL_ENTRY, label=manual_label)
        )
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        "gateway", default=self._discovered_gateways[0].ip
                    ): selector.SelectSelector(
                        selector.SelectSelectorConfig(
                            options=options,
                            mode=selector.SelectSelectorMode.LIST,
                        )
                    )
                }
            ),
            description_placeholders={
                "count": str(len(self._discovered_gateways))
            },
        )

    async def async_step_manual(self, user_input=None):
        """Handle manual gateway address entry."""
        errors = {}
        prefill_host = getattr(self, "_prefill_host", "")
        try:
            if user_input is not None:
                host = user_input[CONF_HOST].strip()
                if not host:
                    errors["base"] = "invalid_host"
                port = user_input[CONF_PORT]
                send_port = user_input.get(CONF_SEND_PORT, port)
                receive_port = user_input.get(CONF_RECEIVE_PORT, port)
                client_address = validate_physical_address(
                    user_input[CONF_CLIENT_ADDRESS]
                )
                if client_address is None:
                    errors[CONF_CLIENT_ADDRESS] = "invalid_client_address"

                data = {
                    CONF_HOST: host,
                    CONF_PORT: port,
                    CONF_SEND_PORT: send_port,
                    CONF_RECEIVE_PORT: receive_port,
                    CONF_CLIENT_ADDRESS: client_address
                    or user_input[CONF_CLIENT_ADDRESS],
                }

                if not errors:
                    try:
                        await _async_validate_connectivity(self.hass, data)
                    except CannotConnect:
                        errors["base"] = "cannot_connect"
                    except InvalidHost:
                        errors["base"] = "invalid_host"
                    except InvalidClientAddress:
                        errors[CONF_CLIENT_ADDRESS] = "invalid_client_address"
                    except Exception:  # pragma: no cover - unexpected
                        _LOGGER.exception("Unexpected exception")
                        errors["base"] = "unknown"

                if not errors:
                    await self.async_set_unique_id(f"{host.lower()}:{port}")
                    self._abort_if_unique_id_configured()
                    return self.async_create_entry(title=f"Buspro ({host})", data=data)

            default_port = user_input.get(CONF_PORT, 6000) if user_input else 6000
            return self.async_show_form(
                step_id="manual",
                data_schema=_form_schema(
                    default_host=user_input.get(CONF_HOST, prefill_host) if user_input else prefill_host,
                    default_port=default_port,
                    default_send_port=user_input.get(CONF_SEND_PORT, default_port) if user_input else default_port,
                    default_receive_port=user_input.get(CONF_RECEIVE_PORT, default_port) if user_input else default_port,
                    default_client_address=user_input.get(CONF_CLIENT_ADDRESS, DEFAULT_CLIENT_ADDRESS) if user_input else DEFAULT_CLIENT_ADDRESS,
                ),
                errors=errors,
            )
        except Exception:  # pragma: no cover - last-resort guard for HA UI stability
            _LOGGER.exception("Failed to render Buspro manual config step")
            return self.async_show_form(
                step_id="manual",
                data_schema=_form_schema(default_host=prefill_host),
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
        default_client_address = current.get(
            CONF_CLIENT_ADDRESS, DEFAULT_CLIENT_ADDRESS
        )

        try:
            if user_input is not None:
                host = user_input[CONF_HOST].strip()
                port = user_input[CONF_PORT]
                send_port = user_input.get(CONF_SEND_PORT, port)
                receive_port = user_input.get(CONF_RECEIVE_PORT, port)
                client_address = validate_physical_address(
                    user_input[CONF_CLIENT_ADDRESS]
                )

                data = {
                    CONF_HOST: host,
                    CONF_PORT: port,
                    CONF_SEND_PORT: send_port,
                    CONF_RECEIVE_PORT: receive_port,
                    CONF_CLIENT_ADDRESS: client_address
                    or user_input[CONF_CLIENT_ADDRESS],
                }

                if not host:
                    return self.async_show_form(
                        step_id="reconfigure",
                        data_schema=_form_schema(
                            host, port, send_port, receive_port,
                            user_input[CONF_CLIENT_ADDRESS],
                        ),
                        errors={"base": "invalid_host"},
                    )
                if client_address is None:
                    return self.async_show_form(
                        step_id="reconfigure",
                        data_schema=_form_schema(
                            host, port, send_port, receive_port,
                            user_input[CONF_CLIENT_ADDRESS],
                        ),
                        errors={CONF_CLIENT_ADDRESS: "invalid_client_address"},
                    )

                try:
                    # Skip UDP socket probe when entry is loaded — binding the
                    # same receive port twice would fail, but host/client validation
                    # is always safe and useful to run.
                    await _async_validate_connectivity(
                        self.hass,
                        data,
                        probe_socket=entry.state
                        != config_entries.ConfigEntryState.LOADED,
                    )
                except CannotConnect:
                    return self.async_show_form(
                        step_id="reconfigure",
                        data_schema=_form_schema(
                            host, port, send_port, receive_port, client_address
                        ),
                        errors={"base": "cannot_connect"},
                    )
                except InvalidHost:
                    return self.async_show_form(
                        step_id="reconfigure",
                        data_schema=_form_schema(
                            host, port, send_port, receive_port, client_address
                        ),
                        errors={"base": "invalid_host"},
                    )
                except InvalidClientAddress:
                    return self.async_show_form(
                        step_id="reconfigure",
                        data_schema=_form_schema(
                            host, port, send_port, receive_port, client_address
                        ),
                        errors={CONF_CLIENT_ADDRESS: "invalid_client_address"},
                    )
                except Exception:  # pragma: no cover - unexpected
                    _LOGGER.exception("Unexpected exception")
                    return self.async_show_form(
                        step_id="reconfigure",
                        data_schema=_form_schema(
                            host, port, send_port, receive_port, client_address
                        ),
                        errors={"base": "unknown"},
                    )

                preserved_options = {
                    key: value
                    for key, value in entry.options.items()
                    if key == CONF_MANAGED_DEVICES
                }
                new_unique_id = f"{host.lower()}:{port}"
                if entry.unique_id != new_unique_id:
                    await self.async_set_unique_id(new_unique_id)
                    self._abort_if_unique_id_configured()
                self.hass.config_entries.async_update_entry(
                    entry,
                    title=f"Buspro ({host})",
                    unique_id=new_unique_id,
                    data=data,
                    options=preserved_options,
                )
                await self.hass.config_entries.async_reload(entry.entry_id)
                return self.async_abort(reason="reconfigure_successful")

            return self.async_show_form(
                step_id="reconfigure",
                data_schema=_form_schema(
                    default_host,
                    default_port,
                    default_send_port,
                    default_receive_port,
                    default_client_address,
                ),
            )
        except Exception:  # pragma: no cover - last-resort guard for HA UI stability
            _LOGGER.exception("Failed to render Buspro reconfigure step")
            return self.async_show_form(
                step_id="reconfigure",
                data_schema=_form_schema(
                    default_host,
                    default_port,
                    default_send_port,
                    default_receive_port,
                    default_client_address,
                ),
                errors={"base": "unknown"},
            )


class BusproOptionsFlow(config_entries.OptionsFlow):
    """Handle Buspro options."""

    def __init__(self, config_entry):
        # Keep local reference for compatibility across HA versions where
        # OptionsFlow may or may not expose/accept config_entry handling
        # in the base class.
        self._config_entry = config_entry
        self._device_type = None
        self._device_draft = None
        self._editing_address = None
        self._legacy_device = None
        self._legacy_entities = []
        self._legacy_channel_entities = {}

    async def async_step_init(self, user_input=None):
        """Show the Buspro management menu."""
        menu_options = ["gateway", "add_device", "scan_bus"]
        if managed_devices(self._config_entry) or self._registry_devices():
            menu_options.append("edit_device")
        return self.async_show_menu(step_id="init", menu_options=menu_options)

    async def async_step_scan_bus(self, user_input=None):
        """Scan the HDL bus and offer discovered devices for import."""
        if user_input is None:
            # Discard stale candidates when the user navigates back to this step.
            self.__dict__.pop("_scan_candidates", None)
        if not hasattr(self, "_scan_candidates"):
            modules = self.hass.data.get(DATA_BUSPRO_CONFIG, {}).get("entry_modules", {})
            module = modules.get(self._config_entry.entry_id)
            if module is None or module.hdl is None:
                return self.async_abort(reason="not_loaded")

            from .bus_scanner import BusScanner
            try:
                discovered = await BusScanner(module.hdl).scan(duration=12.0)
            except Exception:
                _LOGGER.exception("Bus scan failed")
                return self.async_abort(reason="scan_failed")

            # Collect all addresses already known (managed + YAML registry + raw YAML config)
            existing: set[str] = {
                d[CONF_ADDRESS] for d in managed_devices(self._config_entry)
            }
            for dev in self._registry_devices():
                addr = self._device_address(dev)
                if addr:
                    existing.add(addr)
            # Belt-and-suspenders: also exclude YAML-configured addresses even if
            # their entities haven't been loaded into the device registry yet.
            for yaml_dev in self.hass.data.get(DATA_BUSPRO_CONFIG, {}).get("configured_devices", []):
                addr = yaml_dev.get(CONF_ADDRESS)
                if addr:
                    existing.add(addr)

            candidates = []
            for dev in discovered:
                if dev.address in existing or dev.looks_like_keypad:
                    continue
                device_type = _infer_device_type(dev)
                if device_type is None:
                    continue
                model = _pick_model(device_type, dev.channel_count)
                if model is None:
                    continue
                candidates.append((dev, device_type, model))

            self._scan_candidates = candidates

        candidates = self._scan_candidates
        if not candidates:
            return self.async_abort(reason="scan_no_new_devices")

        ch_fmt = "{count} ch"

        if user_input is not None:
            selected_keys = set(user_input.get("devices") or [])
            if selected_keys:
                new_devices = [
                    _build_managed_device(dev, device_type, model, DEVICE_TYPE_LABELS.get(device_type, device_type))
                    for dev, device_type, model in candidates
                    if dev.key in selected_keys
                ]
                return self._save_devices(managed_devices(self._config_entry) + new_devices)
            return self.async_abort(reason="scan_no_new_devices")

        options = [
            selector.SelectOptionDict(
                value=dev.key,
                label=_scan_device_label(dev, DEVICE_TYPE_LABELS.get(device_type, device_type), model, ch_fmt),
            )
            for dev, device_type, model in candidates
        ]
        return self.async_show_form(
            step_id="scan_bus",
            data_schema=vol.Schema({
                vol.Optional("devices", default=list): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=options,
                        multiple=True,
                        mode=selector.SelectSelectorMode.LIST,
                    )
                )
            }),
            description_placeholders={"count": str(len(candidates))},
        )

    async def async_step_gateway(self, user_input=None):
        """Update gateway network settings."""
        errors = {}
        current = {**self._config_entry.data, **self._config_entry.options}
        default_host = current.get(CONF_HOST, "")
        default_port = current.get(CONF_PORT, 6000)
        default_send_port = current.get(CONF_SEND_PORT, default_port)
        default_receive_port = current.get(CONF_RECEIVE_PORT, default_port)
        default_client_address = current.get(
            CONF_CLIENT_ADDRESS, DEFAULT_CLIENT_ADDRESS
        )

        try:
            if user_input is not None:
                host = user_input[CONF_HOST].strip()
                port = user_input[CONF_PORT]
                send_port = user_input.get(CONF_SEND_PORT, port)
                receive_port = user_input.get(CONF_RECEIVE_PORT, port)
                client_address = validate_physical_address(
                    user_input[CONF_CLIENT_ADDRESS]
                )

                data = {
                    CONF_HOST: host,
                    CONF_PORT: port,
                    CONF_SEND_PORT: send_port,
                    CONF_RECEIVE_PORT: receive_port,
                    CONF_CLIENT_ADDRESS: client_address
                    or user_input[CONF_CLIENT_ADDRESS],
                }

                if not host:
                    errors["base"] = "invalid_host"
                if client_address is None:
                    errors[CONF_CLIENT_ADDRESS] = "invalid_client_address"
                if not errors:
                    try:
                        await _async_validate_connectivity(
                            self.hass,
                            data,
                            probe_socket=self._config_entry.state
                            != config_entries.ConfigEntryState.LOADED,
                        )
                    except CannotConnect:
                        errors["base"] = "cannot_connect"
                    except InvalidHost:
                        errors["base"] = "invalid_host"
                    except InvalidClientAddress:
                        errors[CONF_CLIENT_ADDRESS] = "invalid_client_address"
                    except Exception:  # pragma: no cover - unexpected
                        _LOGGER.exception("Unexpected exception")
                        errors["base"] = "unknown"

                if not errors:
                    entry = self._config_entry
                    new_data = {**entry.data, **data}
                    network_keys = {
                        CONF_HOST, CONF_PORT, CONF_SEND_PORT,
                        CONF_RECEIVE_PORT, CONF_CLIENT_ADDRESS,
                    }
                    clean_options = {
                        k: v for k, v in entry.options.items()
                        if k not in network_keys
                    }
                    self.hass.config_entries.async_update_entry(
                        entry, data=new_data, title=f"Buspro ({host})",
                        options=clean_options,
                    )
                    return self.async_create_entry(title="", data=clean_options)

            return self.async_show_form(
                step_id="gateway",
                data_schema=_form_schema(
                    default_host,
                    default_port,
                    default_send_port,
                    default_receive_port,
                    default_client_address,
                ),
                errors=errors,
            )
        except Exception:  # pragma: no cover - last-resort guard for HA UI stability
            _LOGGER.exception("Failed to render Buspro options step")
            return self.async_show_form(
                step_id="gateway",
                data_schema=_form_schema(
                    default_host,
                    default_port,
                    default_send_port,
                    default_receive_port,
                    default_client_address,
                ),
                errors={"base": "unknown"},
            )

    async def async_step_add_device(self, user_input=None):
        """Select the type of device to add."""
        if user_input is not None:
            self._device_type = user_input[CONF_DEVICE_TYPE]
            self._device_draft = None
            self._editing_address = None
            return await self.async_step_device_details()

        return self.async_show_form(
            step_id="add_device",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_DEVICE_TYPE): selector.SelectSelector(
                        selector.SelectSelectorConfig(
                            options=list(DEVICE_TYPE_LABELS.keys()),
                            translation_key="device_type",
                            mode=selector.SelectSelectorMode.DROPDOWN,
                        )
                    )
                }
            ),
        )

    async def async_step_device_details(self, user_input=None):
        """Configure device identity and channel count."""
        errors = {}
        draft = self._device_draft or {}
        device_type = self._device_type or draft.get(CONF_DEVICE_TYPE)
        models = models_for_type(device_type)

        if user_input is not None:
            if self._editing_address and user_input.get(CONF_REMOVE_DEVICE):
                devices = [
                    item
                    for item in managed_devices(self._config_entry)
                    if item[CONF_ADDRESS] != self._editing_address
                ]
                return self._save_devices(devices)

            address = validate_physical_address(user_input[CONF_ADDRESS])
            if address is None:
                errors[CONF_ADDRESS] = "invalid_address"
            elif self._address_in_use(address):
                errors[CONF_ADDRESS] = "address_in_use"

            model = user_input[CONF_MODEL]
            if model not in models:
                errors[CONF_MODEL] = "unsupported_model"
            if not user_input[CONF_NAME].strip():
                errors[CONF_NAME] = "name_required"

            if not errors:
                spec = DEVICE_CATALOG[model]
                channel_count = len(spec.get("capabilities", ()))
                if "capabilities" not in spec:
                    channel_count = fixed_channel_count(DEVICE_CATALOG, model)
                    if channel_count is None:
                        channel_count = int(user_input[CONF_CHANNEL_COUNT])
                        if not 1 <= channel_count <= int(spec["channels"]):
                            errors[CONF_CHANNEL_COUNT] = "invalid_channel_count"

            if not errors:
                self._device_draft = {
                    CONF_ADDRESS: address,
                    CONF_NAME: user_input[CONF_NAME].strip(),
                    CONF_MODEL: model,
                    CONF_DEVICE_TYPE: device_type,
                    CONF_CHANNEL_COUNT: channel_count,
                    CONF_CHANNELS: draft.get(CONF_CHANNELS, []),
                }
                return await self.async_step_device_channels()

        form_values = user_input or draft
        default_model = form_values.get(CONF_MODEL, models[0])
        if default_model not in models:
            default_model = models[0]
        spec = DEVICE_CATALOG[default_model]
        t = await _flow_translations(self.hass, "options")
        schema = {
            vol.Required(
                CONF_NAME,
                default=form_values.get(
                    CONF_NAME, DEVICE_TYPE_LABELS.get(device_type, device_type)
                ),
            ): selector.TextSelector(),
            vol.Required(
                CONF_ADDRESS, default=form_values.get(CONF_ADDRESS, "")
            ): selector.TextSelector(),
            vol.Required(CONF_MODEL, default=default_model): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=models,
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
        }
        if (
            "capabilities" not in spec
            and fixed_channel_count(DEVICE_CATALOG, default_model) is None
        ):
            schema[
                vol.Required(
                    CONF_CHANNEL_COUNT,
                    default=int(
                        form_values.get(CONF_CHANNEL_COUNT, spec["channels"])
                    ),
                )
            ] = selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=1,
                    max=max(
                        int(DEVICE_CATALOG[candidate]["channels"])
                        for candidate in models
                    ),
                    step=1,
                    mode=selector.NumberSelectorMode.BOX,
                )
            )
        if self._editing_address is not None:
            schema[vol.Optional(CONF_REMOVE_DEVICE, default=False)] = (
                selector.BooleanSelector()
            )

        return self.async_show_form(
            step_id="device_details",
            data_schema=vol.Schema(schema),
            errors=errors,
        )

    async def async_step_device_channels(self, user_input=None):
        """Configure the user-visible name of each channel or capability."""
        draft = self._device_draft
        spec = DEVICE_CATALOG[draft[CONF_MODEL]]
        if "capabilities" in spec:
            channel_keys = list(spec["capabilities"])
        else:
            channel_keys = list(range(1, draft[CONF_CHANNEL_COUNT] + 1))

        existing = {
            channel[CONF_CHANNEL_NUMBER]: channel
            for channel in draft.get(CONF_CHANNELS, [])
        }
        if user_input is not None:
            names = {
                key: user_input[f"channel_{key}"].strip() for key in channel_keys
            }
            draft[CONF_CHANNELS] = build_channels(
                draft[CONF_ADDRESS],
                draft[CONF_DEVICE_TYPE],
                draft[CONF_NAME],
                channel_keys,
                names,
                existing,
            )
            devices = managed_devices(self._config_entry)
            if self._editing_address is None:
                devices.append(draft)
            else:
                devices = [
                    draft if item[CONF_ADDRESS] == self._editing_address else item
                    for item in devices
                ]
            return self._save_devices(devices)

        schema = {}
        for key in channel_keys:
            current = existing.get(key, {})
            default = current.get(CONF_NAME, "")
            if not current and isinstance(key, str):
                default = (
                    f"{draft[CONF_NAME]} "
                    f"{str(key).replace('_', ' ').title()}"
                )
            schema[vol.Optional(f"channel_{key}", default=default)] = (
                selector.TextSelector()
            )
        return self.async_show_form(
            step_id="device_channels",
            data_schema=vol.Schema(schema),
            description_placeholders={"device_name": draft[CONF_NAME]},
        )

    async def async_step_edit_device(self, user_input=None):
        """Select an existing managed or legacy device to edit."""
        choices = []
        for device in managed_devices(self._config_entry):
            choices.append(
                selector.SelectOptionDict(
                    value=f"managed:{device[CONF_ADDRESS]}",
                    label=f"{device[CONF_NAME]} ({device[CONF_ADDRESS]})",
                )
            )
        for device in self._registry_devices():
            address = self._device_address(device)
            if any(choice["value"] == f"managed:{address}" for choice in choices):
                continue
            choices.append(
                selector.SelectOptionDict(
                    value=f"registry:{device.id}",
                    label=f"{device.name_by_user or device.name or address} ({address})",
                )
            )

        if user_input is not None:
            selection = user_input["device"]
            source, identifier = selection.split(":", 1)
            if source == "managed":
                device = next(
                    item
                    for item in managed_devices(self._config_entry)
                    if item[CONF_ADDRESS] == identifier
                )
                self._device_draft = device
                self._device_type = device[CONF_DEVICE_TYPE]
                self._editing_address = identifier
                return await self.async_step_device_details()

            registry = dr.async_get(self.hass)
            self._legacy_device = registry.async_get(identifier)
            entity_registry = er.async_get(self.hass)
            self._legacy_entities = sorted(
                (
                    entry
                    for entry in entity_registry.entities.values()
                    if entry.device_id == identifier
                ),
                key=lambda entry: entry.entity_id,
            )
            address = self._device_address(self._legacy_device)
            self._legacy_channel_entities = {
                channel: entry
                for entry in self._legacy_entities
                if (
                    channel := channel_number_from_unique_id(
                        entry.unique_id, address
                    )
                )
                is not None
            }
            return await self.async_step_edit_legacy_device()

        return self.async_show_form(
            step_id="edit_device",
            data_schema=vol.Schema(
                {
                    vol.Required("device"): selector.SelectSelector(
                        selector.SelectSelectorConfig(
                            options=choices,
                            mode=selector.SelectSelectorMode.DROPDOWN,
                        )
                    )
                }
            ),
        )

    async def async_step_edit_legacy_device(self, user_input=None):
        """Edit display names of a device still defined through YAML."""
        if user_input is not None:
            device_registry = dr.async_get(self.hass)
            updated_device = device_registry.async_get_or_create(
                config_entry_id=self._config_entry.entry_id,
                identifiers=self._legacy_device.identifiers,
                connections=self._legacy_device.connections,
                manufacturer=self._legacy_device.manufacturer or "HDL",
                model=user_input[CONF_MODEL],
                name=self._legacy_device.name
                or self._device_address(self._legacy_device),
                serial_number=self._device_address(self._legacy_device),
            )
            self._legacy_device = device_registry.async_update_device(
                updated_device.id,
                name_by_user=user_input[CONF_NAME].strip(),
            )
            entity_registry = er.async_get(self.hass)
            channel_entity_ids = {
                entry.entity_id for entry in self._legacy_channel_entities.values()
            }
            for channel, entry in self._legacy_channel_entities.items():
                entity_registry.async_update_entity(
                    entry.entity_id,
                    name=user_input[f"channel_{channel}"].strip(),
                )
            for entry in self._legacy_entities:
                if entry.entity_id in channel_entity_ids:
                    continue
                entity_registry.async_update_entity(
                    entry.entity_id, name=user_input[entry.entity_id].strip()
                )

            return self.async_create_entry(
                title="", data=dict(self._config_entry.options)
            )

        t = await _flow_translations(self.hass, "options")
        unknown_model = _t(t, "options.scan.unknown_model", "Unknown device")
        current_model = self._legacy_device.model or unknown_model
        current_spec = DEVICE_CATALOG.get(current_model, {})
        device_type = current_spec.get(CONF_DEVICE_TYPE)
        model_options = (
            models_for_type(device_type) if device_type is not None else []
        )
        if current_model not in model_options:
            model_options.append(current_model)
        schema = {
            vol.Required(
                CONF_NAME,
                default=self._legacy_device.name_by_user
                or self._legacy_device.name
                or self._device_address(self._legacy_device),
            ): selector.TextSelector(),
            vol.Required(CONF_MODEL, default=current_model): (
                selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=model_options,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    )
                )
            ),
        }
        channel_entity_ids = {
            entry.entity_id for entry in self._legacy_channel_entities.values()
        }
        for channel, entry in sorted(self._legacy_channel_entities.items()):
            schema[
                vol.Required(
                    f"channel_{channel}",
                    default=entry.name or entry.original_name or entry.entity_id,
                )
            ] = selector.TextSelector()
        for entry in self._legacy_entities:
            if entry.entity_id in channel_entity_ids:
                continue
            schema[
                vol.Required(
                    entry.entity_id,
                    default=entry.name or entry.original_name or entry.entity_id,
                )
            ] = selector.TextSelector()
        return self.async_show_form(
            step_id="edit_legacy_device",
            data_schema=vol.Schema(schema),
        )

    def _address_in_use(self, address):
        if address == self._editing_address:
            return False
        if any(
            self._device_address(device) == address
            for device in self._registry_devices()
        ):
            return True
        return any(
            item[CONF_ADDRESS] == address
            for item in managed_devices(self._config_entry)
        )

    def _registry_devices(self):
        registry = dr.async_get(self.hass)
        return sorted(
            (
                device
                for device in registry.devices.values()
                if self._device_address(device) is not None
                and (
                    self._config_entry.entry_id in (device.config_entries or ())
                    or any(
                        len(identifier) >= 1 and identifier[0] == DOMAIN
                        for identifier in device.identifiers
                    )
                )
            ),
            key=lambda device: tuple(
                int(part) for part in self._device_address(device).split(".")
            ),
        )

    @staticmethod
    def _device_address(device):
        for identifier in device.identifiers:
            if len(identifier) >= 2 and identifier[0] == DOMAIN:
                return identifier[1]
        return None

    def _save_devices(self, devices):
        old_devices = managed_devices(self._config_entry)
        removed_unique_ids = removed_managed_unique_ids(old_devices, devices)
        entity_registry = er.async_get(self.hass)
        for entry in list(entity_registry.entities.values()):
            if (
                entry.platform == DOMAIN
                and entry.config_entry_id == self._config_entry.entry_id
                and entry.unique_id in removed_unique_ids
            ):
                entity_registry.async_remove(entry.entity_id)

        old_addresses = {device[CONF_ADDRESS] for device in old_devices}
        active_addresses = {device[CONF_ADDRESS] for device in devices}
        device_registry = dr.async_get(self.hass)
        for address in old_addresses - active_addresses:
            device = device_registry.async_get_device(
                identifiers={(DOMAIN, address)}, connections=set()
            )
            if device is None:
                continue
            for entry in list(entity_registry.entities.values()):
                if (
                    entry.device_id == device.id
                    and entry.platform == DOMAIN
                    and entry.config_entry_id == self._config_entry.entry_id
                ):
                    entity_registry.async_remove(entry.entity_id)
            if not any(
                entry.device_id == device.id
                for entry in entity_registry.entities.values()
            ):
                device_registry.async_remove_device(device.id)

        options = dict(self._config_entry.options)
        options[CONF_MANAGED_DEVICES] = devices
        return self.async_create_entry(title="", data=options)
