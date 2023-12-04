"""Test sveriges_radio.py."""
# pylint: disable=protected-access
import aiohttp
from aresponses import ResponsesMockServer

from homeassistant.components.sveriges_radio.sveriges_radio import SverigesRadio


async def test_api_request(aresponses: ResponsesMockServer) -> None:
    """Test API response is handled correctly."""
    aresponses.add(
        host_pattern="test.com",
        method_pattern="GET",
        response=aresponses.Response(
            status=200,
            text="<sr></sr>",
        ),
    )
    async with aiohttp.ClientSession() as session:
        radio = SverigesRadio(session=session, user_agent="Test")
        radio.api_url = "test.com"
        channel_response = await radio.call("test.com")
        assert channel_response != {}
