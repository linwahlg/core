"""Test media_source.py."""
from unittest.mock import MagicMock

import pytest

from homeassistant.components.media_player import MediaClass, MediaType
from homeassistant.components.media_source.models import (
    BrowseMediaSource,
    MediaSourceItem,
)
from homeassistant.components.sveriges_radio.const import DOMAIN, FOLDERNAME
from homeassistant.components.sveriges_radio.media_source import (
    SverigesRadioMediaSource,
)

pytestmark = pytest.mark.usefixtures("mock_sveriges_radio")

hass = MagicMock()
entry = MagicMock()


async def test_create_root_directory_podcast() -> None:
    """Test creating root directory for podcasts."""
    media = SverigesRadioMediaSource(hass=hass, entry=entry)
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

    actualRes = await media._async_build_programs(item=general_item, program_info="")

    assert actualRes[0].domain == expectedRes.domain
    assert actualRes[0].identifier == expectedRes.identifier
    assert actualRes[0].media_class == expectedRes.media_class
    assert actualRes[0].media_content_type == expectedRes.media_content_type
    assert actualRes[0].title == expectedRes.title
    assert actualRes[0].can_play == expectedRes.can_play
    assert actualRes[0].can_expand == expectedRes.can_expand
    assert actualRes[0].thumbnail == expectedRes.thumbnail
