"""Test sveriges_radio.py."""

from unittest.mock import patch

import defusedxml.ElementTree as ET
import pytest

from homeassistant.components.media_source.error import Unresolvable
from homeassistant.components.sveriges_radio.sveriges_radio import Source, SverigesRadio

pytestmark = pytest.mark.usefixtures("mock_sveriges_radio")


async def test_no_data_channels_method(mock_sveriges_radio: SverigesRadio) -> None:
    """Test channels method from SverigesRadio class if there are no channels."""
    with patch(
        "homeassistant.components.sveriges_radio.sveriges_radio.SverigesRadio.call",
        return_value=ET.fromstring("<sr>test</sr>"),
    ):
        channels = await mock_sveriges_radio.channels()
        assert channels == []


async def test_channels_method(mock_sveriges_radio: SverigesRadio) -> None:
    """Test channels method from SverigesRadio class with an example channel."""
    with patch(
        "homeassistant.components.sveriges_radio.sveriges_radio.SverigesRadio.call",
        return_value=ET.fromstring(
            '<sr><channels><channel id="1" name="Test Channel"><image>https://content.presentermedia.com/files/clipart/00026000/26395/single_easter_egg_800_wht.jpg</image><color>ffffff</color><siteurl>https://test.com</siteurl><liveaudio><url>https://test.mp3</url></liveaudio></channel></channels></sr>'
        ),
    ):
        channels = await mock_sveriges_radio.channels()
        assert type(channels[0]) is Source


async def test_no_data_programs_method(mock_sveriges_radio: SverigesRadio) -> None:
    """Test programs method from SverigesRadio class if there are no programs."""
    with patch(
        "homeassistant.components.sveriges_radio.sveriges_radio.SverigesRadio.call",
        return_value=ET.fromstring("<sr>test</sr>"),
    ):
        programs = await mock_sveriges_radio.programs([])
        assert programs == []


async def test_programs_method(mock_sveriges_radio: SverigesRadio) -> None:
    """Test programs method from SverigesRadio class with an example program."""
    with patch(
        "homeassistant.components.sveriges_radio.sveriges_radio.SverigesRadio.call",
        return_value=ET.fromstring(
            '<sr><programs><program id="1" name="test program"><programurl>https://test.com</programurl><programimage>https://content.presentermedia.com/files/clipart/00026000/26395/single_easter_egg_800_wht.jpg</programimage><haspod>true</haspod></program></programs></sr>'
        ),
    ):
        programs = await mock_sveriges_radio.programs([])
        assert type(programs[0]) is Source


async def test_no_data_podcasts_method(mock_sveriges_radio: SverigesRadio) -> None:
    """Test podcasts method from SverigesRadio class if there are no podcasts."""
    with patch(
        "homeassistant.components.sveriges_radio.sveriges_radio.SverigesRadio.call",
        return_value=ET.fromstring("<sr>test</sr>"),
    ):
        podcasts = await mock_sveriges_radio.podcasts(1, [])
        assert podcasts == []


async def test_podcasts_method(mock_sveriges_radio: SverigesRadio) -> None:
    """Test podcasts method from SverigesRadio class with an example podcasts."""
    with patch(
        "homeassistant.components.sveriges_radio.sveriges_radio.SverigesRadio.call",
        return_value=ET.fromstring(
            '<sr><podfiles><podfile id="1"><url>https://test.mp3</url><title>test podcast</title></podfile></podfiles></sr>'
        ),
    ):
        podcasts = await mock_sveriges_radio.podcasts(1, [])
        assert type(podcasts[0]) is Source


async def test_channel_resolve_station_method(
    mock_sveriges_radio: SverigesRadio,
) -> None:
    """Test resolve_station method from SverigesRadio class with an example channel."""
    with patch(
        "homeassistant.components.sveriges_radio.sveriges_radio.SverigesRadio.call",
        return_value=ET.fromstring(
            '<sr><channel id="1" name="Test Channel"><image>https://content.presentermedia.com/files/clipart/00026000/26395/single_easter_egg_800_wht.jpg</image><color>ffffff</color><siteurl>https://test.com</siteurl><liveaudio><url>https://test.mp3</url></liveaudio></channel></sr>'
        ),
    ):
        channel = await mock_sveriges_radio.resolve_station(1)
        assert type(channel) is Source


async def test_podcast_resolve_station_method(
    mock_sveriges_radio: SverigesRadio,
) -> None:
    """Test resolve_station method from SverigesRadio class with an example podcast."""
    with patch(
        "homeassistant.components.sveriges_radio.sveriges_radio.SverigesRadio.call",
        return_value=ET.fromstring(
            '<sr><podfile id="1"><url>https://test.mp3</url><title>test podcast</title></podfile></sr>'
        ),
    ):
        podcast = await mock_sveriges_radio.resolve_station(1)
        assert type(podcast) is Source


async def test_error_resolve_station_method(mock_sveriges_radio: SverigesRadio) -> None:
    """Test resolve_station method from SverigesRadio class with no channel or podcast."""
    with patch(
        "homeassistant.components.sveriges_radio.sveriges_radio.SverigesRadio.call",
        return_value=ET.fromstring("<sr>test</sr>"),
    ) and pytest.raises(Unresolvable):
        await mock_sveriges_radio.resolve_station(1)
