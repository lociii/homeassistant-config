"""Config flow to configure the digitalSTROM component."""
from collections import OrderedDict

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD
from homeassistant.core import callback

from .const import DOMAIN, CONF_APARTMENT, CONFIG_PATH


@callback
def configured_digitalstrom(hass):
    """Return the digitalSTROM configuration if set up"""
    entries = hass.config_entries.async_entries(DOMAIN)
    if entries:
        return entries[0]
    return None


@config_entries.HANDLERS.register(DOMAIN)
class DigitalStromFlowHandler(config_entries.ConfigFlow):
    """Handle a digitalSTROM config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    @callback
    def _show_form(self, errors=None):
        """Show the form to the user."""
        data_schema = OrderedDict()

        data_schema[vol.Required(
            CONF_HOST, default='https://dss.local:8080')] = str
        data_schema[vol.Required(CONF_USERNAME, default='dssadmin')] = str
        data_schema[vol.Required(CONF_PASSWORD)] = str
        data_schema[vol.Required(CONF_APARTMENT)] = str

        return self.async_show_form(
            step_id='user',
            data_schema=vol.Schema(data_schema),
            errors=errors or {}
        )

    async def async_step_import(self, import_config):
        """Import a config entry from configuration.yaml."""
        return await self.async_step_user(user_input=import_config)

    async def async_step_user(self, user_input=None):
        """Handle the start of the config flow."""

        # already configuered
        if configured_digitalstrom(self.hass) is not None:
            return self.async_abort(reason="already_configured")

        # no input sent
        if not user_input:
            return self._show_form()

        # validate input
        from pydigitalstrom.client import DSClient
        from pydigitalstrom.exceptions import DSException
        config_path = hass.config.path(CONFIG_PATH)
        client = DSClient(
            host=user_input[CONF_HOST], username=user_input[CONF_USERNAME],
            password=user_input[CONF_PASSWORD], config_path=config_path,
            apartment_name=user_input[CONF_APARTMENT])
        try:
            await client.get_application_token()
        except DSException:
            return self._show_form({CONF_HOST: 'communication_error'})

        return self.async_create_entry(
            title='digitalSTROM', data=user_input)
