"""Expose Sveriges Radio as a Media Source."""
from __future__ import annotations

from homeassistant.components.media_player import BrowseError, MediaClass, MediaType
from homeassistant.components.media_source.error import Unresolvable
from homeassistant.components.media_source.models import (
    BrowseMediaSource,
    MediaSource,
    MediaSourceItem,
    PlayMedia,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback

from .const import DOMAIN, ERROR_MESSAGE_NOT_INITIALIZED, FOLDERNAME
from .sveriges_radio import Source, SverigesRadio


async def async_get_media_source(hass: HomeAssistant) -> SverigesRadioMediaSource:
    """Set up the Media Source."""
    return SverigesRadioMediaSource(hass, hass.config_entries.async_entries(DOMAIN)[0])


class SverigesRadioMediaSource(MediaSource):
    """Class for representing the Media Source."""

    name = "Sveriges Radio"

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the RadioMediaSource class."""
        super().__init__(DOMAIN)
        self.hass = hass
        self.entry = entry

    @property
    def radio(self) -> SverigesRadio | None:
        """Retrieve the Sveriges Radio instance from Home Assistant's data."""
        return self.hass.data.get(DOMAIN)

    async def async_resolve_media(self, item: MediaSourceItem) -> PlayMedia:
        """Resolve a selected Radio station to a streaming URL and returns a PlayMedia object."""
        radio = self.radio or _raise_unresolvable(ERROR_MESSAGE_NOT_INITIALIZED)

        station = await radio.resolve_station(
            station_id=item.identifier
        ) or _raise_unresolvable("Radio station is no longer available")

        return PlayMedia(station.url, "audio/mpeg")

    async def async_browse_media(self, item: MediaSourceItem) -> BrowseMediaSource:
        """Return media items for browsing, structured as BrowseMediaSource objects."""
        category, _, program_info = (item.identifier or "").partition("/")

        if category == FOLDERNAME and program_info:
            program = await radio.program(program_info)
            title = program.name
        elif category == FOLDERNAME:
            title = FOLDERNAME
        else:
            title = "Sveriges Radio"

        return BrowseMediaSource(
            domain=DOMAIN,
            identifier=None,
            media_class=MediaClass.DIRECTORY,
            media_content_type=MediaType.MUSIC,
            title=title,
            can_play=False,
            can_expand=True,
            children_media_class=MediaClass.DIRECTORY,
            children=await self._build_media_children(item, category),
        )

    async def _build_media_children(
        self, item: MediaSourceItem, category: str
    ) -> list[BrowseMediaSource]:
        """Build and return a list of BrowseMediaSource objects as children media items based on the category specified in the MediaSourceItem."""
        if category == FOLDERNAME:
            return await self._async_build_programs(item)
        return await self._async_build_channels(item)

    @callback
    async def _async_build_channels(
        self, item: MediaSourceItem
    ) -> list[BrowseMediaSource]:
        """Build a list of channel BrowseMediaSource objects for the given media item."""
        category, _, _ = (item.identifier or "").partition("/")
        if category:
            return []

        radio = self.radio or _raise_browse_error()
        channels = await radio.channels()

        return [
            _create_browse_media_source(channel, MediaType.MUSIC, True)
            for channel in channels
        ]

    @callback
    async def _async_build_programs(
        self, item: MediaSourceItem
    ) -> list[BrowseMediaSource]:
        radio = self.radio or _raise_browse_error()
        category, _, program_code = (item.identifier or "").partition("/")

        if not item.identifier:
            return [_create_podcast_root()]

        if program_code:
            program = await radio.program(program_code)
            return await self._async_build_podcasts(program)

        programs = await radio.programs(programs_list=[])
        return [
            _create_browse_media_source(
                program, MediaType.MUSIC, False, f"{FOLDERNAME}/{program.station_id}"
            )
            for program in programs
        ]

    @callback
    async def _async_build_podcasts(self, program: Source) -> list[BrowseMediaSource]:
        radio = self.radio or _raise_browse_error()
        podcasts = await radio.podcasts(program_id=program.station_id, podcasts_list=[])

        return [
            _create_browse_media_source(podcast, MediaType.MUSIC, True)
            for podcast in podcasts
        ]


def _create_browse_media_source(entity, media_content_type, can_play, identifier=None):
    return BrowseMediaSource(
        domain=DOMAIN,
        identifier=identifier or str(entity.station_id),
        media_class=MediaClass.MUSIC,
        media_content_type=media_content_type,
        title=entity.name,
        can_play=can_play,
        can_expand=not can_play,
        thumbnail=entity.image,
    )


def _raise_unresolvable(error_message: str):
    """Raise an Unresolvable error with the given message."""
    raise Unresolvable(error_message)


def _raise_browse_error():
    """Raise a BrowseError when the radio is not initialized."""
    raise BrowseError(ERROR_MESSAGE_NOT_INITIALIZED)


def _create_podcast_root() -> BrowseMediaSource:
    """Create a root BrowseMediaSource for podcasts."""
    return BrowseMediaSource(
        domain=DOMAIN,
        identifier=FOLDERNAME,
        media_class=MediaClass.DIRECTORY,
        media_content_type=MediaType.MUSIC,
        title=FOLDERNAME,
        can_play=False,
        can_expand=True,
        thumbnail="https://www.pngarts.com/files/7/Podcast-Symbol-Transparent-Background-PNG.png",
    )


def _determine_title(category: str, program_info: str) -> str:
    """Determine the title for the media based on category and program information."""
    if category == FOLDERNAME and program_info:
        return program_info  # Or a more appropriate title based on program_info
    if category == FOLDERNAME:
        return FOLDERNAME
    return "Sveriges Radio"
