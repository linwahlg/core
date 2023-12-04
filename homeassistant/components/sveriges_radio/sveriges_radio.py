"""Sveriges radio classes."""
import aiohttp
from defusedxml import ElementTree

from homeassistant.components.media_source.error import Unresolvable

from .const import API_URL


class Source:
    """Class for an audio source."""

    def __init__(
        self,
        sveriges_radio,
        name=None,
        station_id=None,
        siteurl=None,
        color=None,
        image=None,
        url=None,
        **kwargs,
    ):
        """Init function for audio source class."""
        self.sveriges_radio = sveriges_radio

        if not station_id:
            raise Unresolvable("No such audio source")

        self.station_id = station_id
        self.name = name
        self.siteurl = siteurl
        self.color = color
        self.image = image
        self.url = url

    def __repr__(self):
        """Represent an audio source."""

        return "Source(%s)" % self.name


class SverigesRadio:
    """Class for Sveriges Radio API."""

    api_url = API_URL

    def __init__(self, session: aiohttp.ClientSession, user_agent: str) -> None:
        """Init function for Sveriges Radio."""
        self.session = session
        self.user_agent = user_agent

    async def call(self, method):
        """Asynchronously call the API."""
        try:
            async with self.session.get(
                f"{self.api_url}{method}", timeout=8
            ) as response:
                if response.status != 200:
                    return {}

                response_text = await response.text()
                return ElementTree.fromstring(response_text)
        except aiohttp.ClientError as error:
            raise Unresolvable("Client Error") from error

    async def resolve_station(self, station_id):
        """Resolve whether a station is a channel or a podcast."""
        channel_data = await self.call(f"channels/{station_id}")
        podcast_data = await self.call(f"podfiles/{station_id}")

        if channel_data != {}:
            channel_id = channel_data.find("channel").attrib.get("id")
            return await self.channel(channel_id)
        if podcast_data != {}:
            podcast_id = podcast_data.find("podfile").attrib.get("id")
            return await self.podcast(podcast_id)
        raise Unresolvable("No valid id.")

    def create_channel(self, data):
        """Create a channel object."""
        return Source(
            sveriges_radio=self,
            name=data.attrib.get("name"),
            station_id=data.attrib.get("id"),
            siteurl=data.find("siteurl").text,
            color=data.find("color").text,
            image=data.find("image").text,
            url=data.find("liveaudio/url").text,
        )

    def create_program(self, data):
        """Create a program object."""
        return Source(
            sveriges_radio=self,
            name=data.attrib.get("name"),
            station_id=data.attrib.get("id"),
            siteurl=data.find("programurl").text,
            image=data.find("programimage").text,
        )

    def create_podcast(self, data):
        """Create a podcast object."""
        return Source(
            sveriges_radio=self,
            name=data.find("title").text,
            station_id=data.attrib.get("id"),
            url=data.find("url").text,
        )

    async def channels(self):
        """Asynchronously get all channels."""
        data = await self.call("channels")
        channels = []

        for channel_data in data.find("channels"):
            channels.append(self.create_channel(channel_data))

        return channels

    async def channel(self, station_id):
        """Asynchronously get a specific channel."""
        data = await self.call(f"channels/{station_id}")
        return self.create_channel(data.find("channel"))

    async def programs(self, programs_list, page_nr=1):
        """Asynchronously get all programs that contains podcasts."""
        data = await self.call(f"programs?page={page_nr}")

        # End recursion
        if not data:
            return programs_list

        if data.find("pagination") is not None:
            if int(data.find("pagination/page").text) != page_nr:
                raise Unresolvable(f"Page {page_nr} doesn't exist")

        for program_data in data.find("programs"):
            if program_data.find("haspod").text != "true":
                continue

            programs_list.append(self.create_program(program_data))

        if data.find("pagination") is not None:
            if (
                page_nr < int(data.find("pagination/totalpages").text)
                and data.find("pagination/nextpage") is not None
            ):
                programs_list = await self.programs(
                    programs_list=programs_list, page_nr=page_nr + 1
                )

        return programs_list

    async def program(self, program_id):
        """Asynchronously get a program."""
        data = await self.call(f"programs/{program_id}")
        return self.create_program(data.find("program"))

    async def podcasts(self, program_id, podcasts_list, page_nr=1):
        """Asynchronously get all podcasts."""
        data = await self.call(f"podfiles?programid={program_id}&page={page_nr}")

        # End recursion
        if not data:
            return podcasts_list

        if data.find("pagination") is not None:
            if int(data.find("pagination/page").text) != page_nr:
                raise Unresolvable(f"Page {page_nr} doesn't exist")

        for podcast_data in data.find("podfiles"):
            podcasts_list.append(self.create_podcast(podcast_data))

        if data.find("pagination") is not None:
            if (
                page_nr < int(data.find("pagination/totalpages").text)
                and page_nr < 24
                and data.find("pagination/nextpage") is not None
            ):
                podcasts_list = await self.podcasts(
                    program_id=program_id,
                    podcasts_list=podcasts_list,
                    page_nr=page_nr + 1,
                )

        return podcasts_list

    async def podcast(self, podcast_id):
        """Asynchronously get a podcast."""
        data = await self.call(f"podfiles/{podcast_id}")
        return self.create_podcast(data.find("podfile"))
