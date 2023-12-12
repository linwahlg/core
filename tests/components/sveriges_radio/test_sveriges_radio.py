"""Test sveriges_radio.py."""

from unittest.mock import patch

import defusedxml.ElementTree as ET
import pytest

from homeassistant.components.media_source.error import Unresolvable
from homeassistant.components.sveriges_radio.sveriges_radio import Source, SverigesRadio

pytestmark = pytest.mark.usefixtures("mock_sveriges_radio")

mock_sveriges_radio_call_method = 'homeassistant.components.sveriges_radio.sveriges_radio.SverigesRadio.call'
mock_failure_xml = '<sr>test</sr>'
mock_channels_xml = '<sr><channels><channel id="1" name="Test Channel"><image>https://content.presentermedia.com/files/clipart/00026000/26395/single_easter_egg_800_wht.jpg</image><color>ffffff</color><siteurl>https://test.com</siteurl><liveaudio><url>https://test.mp3</url></liveaudio></channel></channels></sr>'
mock_programs_xml = '<sr><programs><program id="1" name="test program"><programurl>https://test.com</programurl><programimage>https://content.presentermedia.com/files/clipart/00026000/26395/single_easter_egg_800_wht.jpg</programimage><haspod>true</haspod></program></programs></sr>'
mock_podfiles_xml = '<sr><podfiles><podfile id="1"><url>https://test.mp3</url><title>test podcast</title></podfile></podfiles></sr>'
mock_channel_xml = '<sr><channel id="1" name="Test Channel"><image>https://content.presentermedia.com/files/clipart/00026000/26395/single_easter_egg_800_wht.jpg</image><color>ffffff</color><siteurl>https://test.com</siteurl><liveaudio><url>https://test.mp3</url></liveaudio></channel></sr>'
mock_podfile_xml = '<sr><podfile id="1"><url>https://test.mp3</url><title>test podcast</title></podfile></sr>'
mock_program_xml = '<sr><program id="1" name="test program"><programurl>https://test.com</programurl><programimage>https://content.presentermedia.com/files/clipart/00026000/26395/single_easter_egg_800_wht.jpg</programimage></program></sr>'


async def test_no_data_channels_method(mock_sveriges_radio: SverigesRadio) -> None:
    """Test channels method from SverigesRadio class if there are no channels."""
    with patch(
        mock_sveriges_radio_call_method,
        return_value=ET.fromstring(mock_failure_xml),
    ):
        channels = await mock_sveriges_radio.channels()
        assert channels == []


async def test_channels_method(mock_sveriges_radio: SverigesRadio) -> None:
    """Test channels method from SverigesRadio class with an example channel."""
    with patch(
        mock_sveriges_radio_call_method,
        return_value=ET.fromstring(mock_channels_xml),
    ):
        channels = await mock_sveriges_radio.channels()
        assert type(channels[0]) is Source


async def test_no_data_programs_method(mock_sveriges_radio: SverigesRadio) -> None:
    """Test programs method from SverigesRadio class if there are no programs."""
    with patch(
        mock_sveriges_radio_call_method,
        return_value=ET.fromstring(mock_failure_xml),
    ):
        programs = await mock_sveriges_radio.programs([])
        assert programs == []


async def test_programs_method(mock_sveriges_radio: SverigesRadio) -> None:
    """Test programs method from SverigesRadio class with an example program."""
    with patch(
        mock_sveriges_radio_call_method,
        return_value=ET.fromstring(mock_programs_xml),
    ):
        programs = await mock_sveriges_radio.programs([])
        assert type(programs[0]) is Source


async def test_no_data_podcasts_method(mock_sveriges_radio: SverigesRadio) -> None:
    """Test podcasts method from SverigesRadio class if there are no podcasts."""
    with patch(
        mock_sveriges_radio_call_method,
        return_value=ET.fromstring(mock_failure_xml),
    ):
        podcasts = await mock_sveriges_radio.podcasts(1, [])
        assert podcasts == []


async def test_podcasts_method(mock_sveriges_radio: SverigesRadio) -> None:
    """Test podcasts method from SverigesRadio class with an example podcasts."""
    with patch(
        mock_sveriges_radio_call_method,
        return_value=ET.fromstring(mock_podfiles_xml),
    ):
        podcasts = await mock_sveriges_radio.podcasts(1, [])
        assert type(podcasts[0]) is Source


async def test_channel_resolve_station_method(
    mock_sveriges_radio: SverigesRadio,
) -> None:
    """Test resolve_station method from SverigesRadio class with an example channel."""
    with patch(
        mock_sveriges_radio_call_method,
        return_value=ET.fromstring(mock_channel_xml),
    ):
        channel = await mock_sveriges_radio.resolve_station(1)
        assert type(channel) is Source


async def test_podcast_resolve_station_method(
    mock_sveriges_radio: SverigesRadio,
) -> None:
    """Test resolve_station method from SverigesRadio class with an example podcast."""
    with patch(
        mock_sveriges_radio_call_method,
        return_value=ET.fromstring(mock_podfile_xml),
    ):
        podcast = await mock_sveriges_radio.resolve_station(1)
        assert type(podcast) is Source


async def test_error_resolve_station_method(mock_sveriges_radio: SverigesRadio) -> None:
    """Test resolve_station method from SverigesRadio class with no channel or podcast."""
    with patch(
        mock_sveriges_radio_call_method,
        return_value=ET.fromstring(mock_failure_xml),
    ) and pytest.raises(Unresolvable):
        await mock_sveriges_radio.resolve_station(1)


async def test_program_method(mock_sveriges_radio: SverigesRadio) -> None:
    """Test program method from SverigesRadio class with an example program."""
    with patch(
        mock_sveriges_radio_call_method, return_value=ET.fromstring(mock_program_xml)
    ):
        program = await mock_sveriges_radio.program(1)
        assert type(program) is Source
