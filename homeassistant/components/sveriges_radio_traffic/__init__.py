"""The Sveriges Radio Traffic integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN
from .coordinator import SverigesRadioTrafficCoordinator

# Should fix: List the platforms that you want to support.
# For your initial PR, limit it to 1 platform.
PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Sveriges Radio Traffic from a config entry."""

    # hass.data.setdefault(DOMAIN, {})
    # Should fix: 1. Create API instance
    # Should fix: 2. Validate the API connection (and authentication)
    # Should fix: 3. Store an API object for your platforms to access
    # hass.data[DOMAIN][entry.entry_id] = MyApi(...)
    session = async_get_clientsession(hass)
    area = entry.data.get("area")

    coordinator = SverigesRadioTrafficCoordinator(
        hass,
        entry,
        area,
        session,  # to_station, from_station, entry.options.get(CONF_FILTER_PRODUCT)
    )
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
