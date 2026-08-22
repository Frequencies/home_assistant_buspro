"""Event entities for HDL Buspro button panels."""

from homeassistant.components.event import EventDeviceClass, EventEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers import device_registry as dr, entity_registry as er

from .const import CONF_MANAGED_DEVICES, DATA_BUSPRO_CONFIG, DOMAIN
from .device_catalog import DEVICE_CATALOG
from .entity_helpers import registry_device_definitions, registry_device_metadata
from .managed_devices import managed_device_info
from .logic_controller import (
    logic_controller_coordinator,
    logic_controller_definitions,
)
from .pybuspro.helpers.enums import OperateCode

EVENT_ON = "on"
EVENT_OFF = "off"
EVENT_CHANNEL_ON = "channel_on"
EVENT_CHANNEL_OFF = "channel_off"
EVENT_CHANNEL_LEVEL = "channel_level"
EVENT_SCENE = "scene"
EVENT_UNIVERSAL_SWITCH_ON = "universal_switch_on"
EVENT_UNIVERSAL_SWITCH_OFF = "universal_switch_off"
EVENT_LOGIC_TELEGRAM = "telegram"


def _channel_entity(hass, target_address, channel):
    """Resolve a physical Buspro output channel to its HA entity."""
    if hass is None or not target_address:
        return None
    device_registry = dr.async_get(hass)
    device = device_registry.async_get_device(
        identifiers={(DOMAIN, target_address)}, connections=set()
    )
    if device is None:
        return None

    suffix = f"-{channel}"
    entity_registry = er.async_get(hass)
    # Look up only this device's entries instead of scanning the whole registry
    # on every decoded channel telegram.
    candidates = [
        entry
        for entry in er.async_entries_for_device(
            entity_registry, device.id, include_disabled_entities=True
        )
        if entry.platform == DOMAIN
        and entry.unique_id.endswith(suffix)
        and entry.entity_id.split(".", 1)[0] in {"cover", "fan", "light", "switch"}
    ]
    if len(candidates) != 1:
        return None
    entry = candidates[0]
    return {
        "entity_id": entry.entity_id,
        "name": entry.name or entry.original_name or entry.entity_id,
    }


def _decode_action(telegram, hass=None):
    """Decode a panel command into an event type and readable attributes."""
    payload = list(telegram.payload or ())
    target_address = tuple(telegram.target_address or ())
    target_key = ".".join(str(part) for part in target_address)
    target = (
        registry_device_metadata(hass, target_key)
        if hass is not None and len(target_address) == 2
        else {}
    )
    attributes = {
        "target_address": target_key,
        "target_device": target.get("name", f"HDL Buspro {target_key}"),
        "target_model": target.get("model", "Buspro device"),
        "raw_payload": payload,
    }

    if telegram.operate_code == OperateCode.SingleChannelControl:
        if len(payload) < 2:
            return None
        channel = int(payload[0])
        level = int(payload[1])
        transition_seconds = (
            int(payload[2]) * 60 + int(payload[3]) if len(payload) >= 4 else 0
        )
        if level == 0:
            event_type = EVENT_CHANNEL_OFF
            action = "off"
        elif level == 100:
            event_type = EVENT_CHANNEL_ON
            action = "on"
        else:
            event_type = EVENT_CHANNEL_LEVEL
            action = f"{level}%"
        channel_entity = _channel_entity(hass, target_key, channel)
        output_name = (
            channel_entity["name"]
            if channel_entity is not None
            else f"{attributes['target_device']}, channel {channel}"
        )
        attributes.update(
            {
                "channel": channel,
                "level": level,
                "transition_seconds": transition_seconds,
                "summary": f"{output_name}: {action}",
            }
        )
        if channel_entity is not None:
            attributes["target_entity"] = channel_entity["entity_id"]
            attributes["target_entity_name"] = channel_entity["name"]
        return event_type, attributes

    if telegram.operate_code == OperateCode.SceneControl:
        if len(payload) < 2:
            return None
        attributes.update(
            {
                "area": int(payload[0]),
                "scene": int(payload[1]),
                "summary": (
                    f"{attributes['target_device']}: area {payload[0]}, "
                    f"scene {payload[1]}"
                ),
            }
        )
        return EVENT_SCENE, attributes

    if telegram.operate_code == OperateCode.UniversalSwitchControl:
        if len(payload) < 2:
            return None
        switch_number = int(payload[0])
        status = int(payload[1])
        action = "off" if status == 0 else "on"
        event_type = (
            EVENT_UNIVERSAL_SWITCH_OFF
            if status == 0
            else EVENT_UNIVERSAL_SWITCH_ON
        )
        attributes.update(
            {
                "switch_number": switch_number,
                "status": status,
                "summary": (
                    f"{attributes['target_device']}, universal switch "
                    f"{switch_number}: {action}"
                ),
            }
        )
        return event_type, attributes

    return None


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up button events for supported catalog and UI-managed panels."""
    module = hass.data[DATA_BUSPRO_CONFIG]["entry_modules"][config_entry.entry_id]
    panels = panel_definitions(hass, config_entry)
    entities = []
    for address, (name, button_count, device_info) in panels.items():
        device_address = tuple(int(part) for part in address.split("."))
        entities.extend(
            BusproPanelButtonEvent(
                module.hdl,
                device_address,
                address,
                name,
                button_number,
                device_info,
            )
            for button_number in range(1, button_count + 1)
        )
        entities.append(
            BusproPanelActionEvent(
                hass,
                module.hdl,
                device_address,
                address,
                device_info,
            )
        )

    for address, device_info in logic_controller_definitions(
        hass, config_entry
    ).items():
        entities.append(
            BusproLogicControllerEvent(
                hass,
                logic_controller_coordinator(module, address),
                address,
                device_info,
            )
        )

    async_add_entities(entities)


class BusproLogicControllerEvent(EventEntity):
    """Commands and broadcasts transmitted by an HDL logic controller."""

    _attr_event_types = [
        EVENT_CHANNEL_ON,
        EVENT_CHANNEL_OFF,
        EVENT_CHANNEL_LEVEL,
        EVENT_SCENE,
        EVENT_UNIVERSAL_SWITCH_ON,
        EVENT_UNIVERSAL_SWITCH_OFF,
        EVENT_LOGIC_TELEGRAM,
    ]
    _attr_has_entity_name = True
    _attr_name = "Logic event"
    _attr_should_poll = False

    def __init__(self, hass, coordinator, address, device_info):
        self._hass = hass
        self._coordinator = coordinator
        self._telegram_cb = self._handle_telegram
        self._attr_unique_id = f"{DOMAIN}-{address}-logic-event"
        self._attr_device_info = device_info

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        self._coordinator.register_telegram_cb(self._telegram_cb)

    async def async_will_remove_from_hass(self):
        self._coordinator.unregister_telegram_cb(self._telegram_cb)
        await super().async_will_remove_from_hass()

    def _handle_telegram(self, telegram):
        if telegram.operate_code in {
            OperateCode.IsDeviceOnlineResponse,
            OperateCode.ReadFirmwareVersionResponse,
        }:
            return

        decoded = _decode_action(telegram, self._hass)
        if decoded is not None:
            event_type, attributes = decoded
        else:
            operate_code = telegram.operate_code
            value = getattr(operate_code, "value", b"")
            attributes = {
                "operate_code": getattr(operate_code, "name", str(operate_code)),
                "operate_code_hex": (
                    value.hex().upper() if isinstance(value, bytes) else str(value)
                ),
                "source_address": ".".join(
                    str(part) for part in (telegram.source_address or ())
                ),
                "target_address": ".".join(
                    str(part) for part in (telegram.target_address or ())
                ),
                "raw_payload": list(telegram.payload or ()),
            }
            event_type = EVENT_LOGIC_TELEGRAM

        self._trigger_event(event_type, attributes)
        self.async_write_ha_state()


def panel_definitions(hass, config_entry):
    """Return supported panel addresses and their entity metadata."""
    panels = {}

    for device in registry_device_definitions(hass, config_entry):
        spec = DEVICE_CATALOG.get(device.get("model"), {})
        if spec.get("panel_actions") or spec.get("button_count"):
            panels[device["address"]] = (
                device["name"],
                int(spec.get("button_count", 0)),
                device["device_info"],
            )

    for device_config in config_entry.options.get(CONF_MANAGED_DEVICES, []):
        spec = DEVICE_CATALOG.get(device_config.get("model"), {})
        if spec.get("panel_actions") or spec.get("button_count"):
            panels[device_config["address"]] = (
                device_config["name"],
                int(spec.get("button_count", 0)),
                managed_device_info(device_config),
            )

    return panels


class BusproPanelButtonEvent(EventEntity):
    """A panel key configured as a Buspro Universal Switch command."""

    _attr_device_class = EventDeviceClass.BUTTON
    _attr_event_types = [EVENT_ON, EVENT_OFF]
    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(
        self,
        buspro,
        device_address,
        address,
        device_name,
        button_number,
        device_info,
    ):
        self._buspro = buspro
        self._device_address = device_address
        self._button_number = button_number
        self._telegram_cb = self._handle_telegram
        self._attr_name = f"Button {button_number}"
        self._attr_unique_id = f"{DOMAIN}-{address}-button-{button_number}"
        self._attr_device_info = device_info
        self._attr_extra_state_attributes = {
            "button_number": button_number,
            "panel_name": device_name,
        }

    async def async_added_to_hass(self):
        """Subscribe to telegrams involving this physical panel."""
        await super().async_added_to_hass()
        self._buspro.register_telegram_received_device_cb(
            self._telegram_cb, self._device_address
        )

    async def async_will_remove_from_hass(self):
        """Unsubscribe from panel telegrams."""
        self._buspro.unregister_telegram_received_device_cb(
            self._telegram_cb, self._device_address
        )
        await super().async_will_remove_from_hass()

    def _handle_telegram(self, telegram):
        payload = telegram.payload or []
        if (
            tuple(telegram.source_address or ()) != self._device_address
            or telegram.operate_code != OperateCode.UniversalSwitchControl
            or len(payload) < 2
            or payload[0] != self._button_number
        ):
            return

        status = int(payload[1])
        event_type = EVENT_OFF if status == 0 else EVENT_ON
        self._trigger_event(
            event_type,
            {
                "button_number": self._button_number,
                "status": status,
                "target_address": list(telegram.target_address or ()),
            },
        )
        self.async_write_ha_state()


class BusproPanelActionEvent(EventEntity):
    """All identifiable commands transmitted by a supported panel."""

    _attr_event_types = [
        EVENT_CHANNEL_ON,
        EVENT_CHANNEL_OFF,
        EVENT_CHANNEL_LEVEL,
        EVENT_SCENE,
        EVENT_UNIVERSAL_SWITCH_ON,
        EVENT_UNIVERSAL_SWITCH_OFF,
    ]
    _attr_has_entity_name = True
    _attr_name = "Action"
    _attr_should_poll = False

    def __init__(self, hass, buspro, device_address, address, device_info):
        self._hass = hass
        self._buspro = buspro
        self._device_address = device_address
        self._telegram_cb = self._handle_telegram
        self._attr_unique_id = f"{DOMAIN}-{address}-action"
        self._attr_device_info = device_info

    async def async_added_to_hass(self):
        """Subscribe to telegrams involving this physical panel."""
        await super().async_added_to_hass()
        self._buspro.register_telegram_received_device_cb(
            self._telegram_cb, self._device_address
        )

    async def async_will_remove_from_hass(self):
        """Unsubscribe from panel telegrams."""
        self._buspro.unregister_telegram_received_device_cb(
            self._telegram_cb, self._device_address
        )
        await super().async_will_remove_from_hass()

    def _handle_telegram(self, telegram):
        if tuple(telegram.source_address or ()) != self._device_address:
            return

        decoded = _decode_action(telegram, self._hass)
        if decoded is None:
            return
        event_type, attributes = decoded
        self._trigger_event(event_type, attributes)
        self.async_write_ha_state()


class BusproPanelLastActionSensor(SensorEntity):
    """Readable summary of the most recent command transmitted by a panel."""

    _attr_has_entity_name = True
    _attr_name = "Last action"
    _attr_should_poll = False

    def __init__(self, hass, buspro, device_address, address, device_info):
        self._hass = hass
        self._buspro = buspro
        self._device_address = device_address
        self._telegram_cb = self._handle_telegram
        self._attr_unique_id = f"{DOMAIN}-{address}-last-action"
        self._attr_device_info = device_info

    async def async_added_to_hass(self):
        """Subscribe to telegrams involving this physical panel."""
        await super().async_added_to_hass()
        self._buspro.register_telegram_received_device_cb(
            self._telegram_cb, self._device_address
        )

    async def async_will_remove_from_hass(self):
        """Unsubscribe from panel telegrams."""
        self._buspro.unregister_telegram_received_device_cb(
            self._telegram_cb, self._device_address
        )
        await super().async_will_remove_from_hass()

    def _handle_telegram(self, telegram):
        if tuple(telegram.source_address or ()) != self._device_address:
            return
        decoded = _decode_action(telegram, self._hass)
        if decoded is None:
            return
        event_type, attributes = decoded
        self._attr_native_value = attributes["summary"]
        self._attr_extra_state_attributes = {
            "action_type": event_type,
            **attributes,
        }
        self.async_write_ha_state()
