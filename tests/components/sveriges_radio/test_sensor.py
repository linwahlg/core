"""Tests for sensor module in Sveriges Radio integrations."""

from unittest.mock import MagicMock, Mock, patch

from requests import Response

from homeassistant.components.sveriges_radio.sensor import TrafficSensor
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er


def _mock_return_value_from_api() -> Response:
    with open(
        "tests/components/sveriges_radio/sr_traffic_api_mock_return_value.txt", "rb"
    ) as mock_api_response:
        content = mock_api_response.read()

    mock_requests_response = Response()
    mock_requests_response._content = content

    return mock_requests_response


async def test_entity_registry(
    hass: HomeAssistant, async_setup_sr, entity_registry: er.EntityRegistry
) -> None:
    """Test that all 4 sensors are registered."""

    await async_setup_sr()

    assert "sensor.sveriges_radio_message" in entity_registry.entities
    assert "sensor.sveriges_radio_area" in entity_registry.entities
    assert "sensor.sveriges_radio_timestamp" in entity_registry.entities
    assert "sensor.sveriges_radio_exact_location" in entity_registry.entities


@patch("requests.get", Mock(return_value=_mock_return_value_from_api()))
async def test_get_traffic_info() -> None:
    """Test expected behaviour from _get_traffic_info."""
    hass = MagicMock()
    entry = MagicMock()
    traffic_area = "Värmland"

    # check most used branches
    traffic_sensor = TrafficSensor(
        hass, traffic_area, ("description", "Message", "mdi:message"), entry, "???"
    )
    message = traffic_sensor._get_traffic_info()
    assert (
        message
        == "Stockholm-Västerås. Risk för förseningar. Reducerad spårkapacitet vid Bålsta."
    )

    traffic_sensor = TrafficSensor(
        hass, traffic_area, ("area", "Area", "mdi:map-marker"), entry, "???"
    )
    area = traffic_sensor._get_traffic_info()
    assert area == traffic_area

    traffic_sensor = TrafficSensor(
        hass, traffic_area, ("createddate", "Timestamp", "mdi:update"), entry, "???"
    )
    date_time = traffic_sensor._get_traffic_info()
    assert date_time == "11:55, 2013-01-09"
