"""The tests for the WSDOT platform."""

from pytest_homeassistant.common import MockConfigEntry
from pytest_homeassistant.test_util.aiohttp import AiohttpClientMocker

from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant
from homeassistant.helpers import issue_registry as ir


async def test_travel_sensor_setup_no_auth(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_failed_travel_time: None,
    issue_registry: ir.IssueRegistry,
) -> None:
    """Test the wsdot Travel Time sensor does not create an entry with a bad API key."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.SETUP_ERROR


async def test_api_requests_use_https(
    hass: HomeAssistant,
    mock_https_api: AiohttpClientMocker,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test the access code is only sent to the WSDOT API over HTTPS."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.LOADED
    assert hass.states.get("sensor.seattle_bellevue_via_i_90_eb_am").state == "11"
    assert mock_https_api.call_count == 2
    assert {url.scheme for _, url, _, _ in mock_https_api.mock_calls} == {"https"}
