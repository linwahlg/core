"""Common fixtures for the Sveriges Radio tests."""
from collections.abc import Generator
from unittest.mock import AsyncMock, patch

import aiohttp
import pytest

from homeassistant.components.sveriges_radio.sveriges_radio import SverigesRadio


@pytest.fixture
def mock_setup_entry() -> Generator[AsyncMock, None, None]:
    """Override async_setup_entry."""
    with patch(
        "homeassistant.components.sveriges_radio.async_setup_entry",
        return_value=True,
    ) as mock_setup_entry:
        yield mock_setup_entry


@pytest.fixture
async def mock_sveriges_radio():
    """Create a mock Sveriges Radio instance."""
    mock_session = AsyncMock(spec=aiohttp.ClientSession)
    user_agent = "TestUserAgent"
    return SverigesRadio(session=mock_session, user_agent=user_agent)
