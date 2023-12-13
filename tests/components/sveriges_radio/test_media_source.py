"""Test media_source.py."""
from unittest.mock import AsyncMock, patch

import defusedxml.ElementTree as ET
import pytest

from homeassistant.components.media_player import MediaClass, MediaType
from homeassistant.components.media_source.error import Unresolvable
from homeassistant.components.media_source.models import (
    BrowseMediaSource,
    MediaSourceItem,
    PlayMedia,
)
from homeassistant.components.sveriges_radio.const import DOMAIN, FOLDERNAME
from homeassistant.components.sveriges_radio.media_source import (
    SverigesRadioMediaSource,
)
from homeassistant.components.sveriges_radio.sveriges_radio import Source
from homeassistant.core import HomeAssistant

entry = AsyncMock()

mock_sveriges_radio_call_method = (
    "homeassistant.components.sveriges_radio.sveriges_radio.SverigesRadio.call"
)
pytestmark = pytest.mark.usefixtures("mock_sveriges_radio")
mock_failure_xml = "<sr>test</sr>"
mock_channel_xml = '<sr><channel id="1" name="Test Channel"><image>https://content.presentermedia.com/files/clipart/00026000/26395/single_easter_egg_800_wht.jpg</image><color>ffffff</color><siteurl>https://test.com</siteurl><liveaudio><url>https://test.mp3</url></liveaudio></channel></sr>'
mock_programs_xml = '<sr><programs><program id="1" name="test program"><programurl>https://test.com</programurl><programimage>https://content.presentermedia.com/files/clipart/00026000/26395/single_easter_egg_800_wht.jpg</programimage><haspod>true</haspod></program></programs></sr>'
mock_program_xml = '<sr><program id="1" name="test program"><programurl>https://test.com</programurl><programimage>https://content.presentermedia.com/files/clipart/00026000/26395/single_easter_egg_800_wht.jpg</programimage></program></sr>'
mock_podfiles_xml = '<sr><podfiles><podfile id="1"><url>https://test.mp3</url><title>test podcast</title></podfile></podfiles></sr>'
mock_podfile_xml = '<sr><podfile id="1"><url>https://test.mp3</url><title>test podcast</title></podfile></sr>'


async def test_create_root_directory_podcast(
    hass: HomeAssistant, async_setup_sr
) -> None:
    """Test creating root directory for podcasts."""
    await async_setup_sr()
    media_source = SverigesRadioMediaSource(hass=hass, entry=entry)
    general_item = MediaSourceItem(
        hass=hass, domain=None, identifier=None, target_media_player=None
    )

    expectedRes = BrowseMediaSource(
        domain=DOMAIN,
        identifier=FOLDERNAME,
        media_class=MediaClass.DIRECTORY,
        media_content_type=MediaType.MUSIC,
        title=FOLDERNAME,
        can_play=False,
        can_expand=True,
        thumbnail="https://www.pngarts.com/files/7/Podcast-Symbol-Transparent-Background-PNG.png",
    )

    actualRes = await media_source._async_build_programs(
        item=general_item, program_info=""
    )

    assert actualRes[0].domain == expectedRes.domain
    assert actualRes[0].identifier == expectedRes.identifier
    assert actualRes[0].media_class == expectedRes.media_class
    assert actualRes[0].media_content_type == expectedRes.media_content_type
    assert actualRes[0].title == expectedRes.title
    assert actualRes[0].can_play == expectedRes.can_play
    assert actualRes[0].can_expand == expectedRes.can_expand
    assert actualRes[0].thumbnail == expectedRes.thumbnail
    assert type(actualRes[0]) is BrowseMediaSource


async def test_resolve_media_fail(hass: HomeAssistant, async_setup_sr) -> None:
    """Test unresolvable media."""
    with patch(
        mock_sveriges_radio_call_method,
        return_value=ET.fromstring(mock_failure_xml),
    ):
        await async_setup_sr()
        media_source = SverigesRadioMediaSource(hass=hass, entry=entry)
        general_item = MediaSourceItem(
            hass=hass, domain=None, identifier=None, target_media_player=None
        )

        with pytest.raises(Unresolvable):
            await media_source.async_resolve_media(item=general_item)


async def test_resolve_media_success(hass: HomeAssistant, async_setup_sr) -> None:
    """Test resolvable media."""
    with patch(
        mock_sveriges_radio_call_method,
        return_value=ET.fromstring(mock_channel_xml),
    ):
        await async_setup_sr()
        media_source = SverigesRadioMediaSource(hass=hass, entry=entry)
        general_item = MediaSourceItem(
            hass=hass, domain=None, identifier="1", target_media_player=None
        )

        media_object = await media_source.async_resolve_media(item=general_item)
        assert type(media_object) is PlayMedia
        assert media_object.url == "https://test.mp3"
        assert media_object.mime_type == "audio/mpeg"


async def test_browse_media(hass: HomeAssistant, async_setup_sr) -> None:
    """Test the browse_media function."""
    with patch(
        mock_sveriges_radio_call_method,
        return_value=ET.fromstring(mock_programs_xml),
    ):
        await async_setup_sr()
        media_source = SverigesRadioMediaSource(hass=hass, entry=entry)
        general_item = MediaSourceItem(
            hass=hass, domain=None, identifier="1", target_media_player=None
        )

        media_result = await media_source.async_browse_media(general_item)

        assert type(media_result) is BrowseMediaSource
        assert type(media_result.children[0]) is BrowseMediaSource
        assert media_result.title == "Sveriges Radio"
        assert media_result.domain == "sveriges_radio"


async def test_build_podcasts(hass: HomeAssistant, async_setup_sr) -> None:
    """Test the build_podcasts function."""
    with patch(
        mock_sveriges_radio_call_method,
        return_value=ET.fromstring(mock_podfiles_xml),
    ):
        await async_setup_sr()
        media_source = SverigesRadioMediaSource(hass=hass, entry=entry)

        test_program = Source(
            sveriges_radio="sveriges_radio",
            name="test program",
            station_id="1",
            siteurl="https://test.com",
            image="https://content.presentermedia.com/files/clipart/00026000/26395/single_easter_egg_800_wht.jpg",
        )

        podcast_list_res = await media_source._async_build_podcasts(test_program)

        assert len(podcast_list_res) == 1

        podcast_res = podcast_list_res[0]

        assert type(podcast_res) is BrowseMediaSource
        assert podcast_res.title == "test podcast"
        assert podcast_res.domain == "sveriges_radio"
