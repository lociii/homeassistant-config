"""
Support for digitalSTROM devices.
"""
import logging

import voluptuous as vol

from homeassistant.helpers import discovery
from homeassistant.exceptions import PlatformNotReady
import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD

_LOGGER = logging.getLogger(__name__)

REQUIREMENTS = ['pydigitalstrom==0.4.1']

DOMAIN = 'digitalstrom'
DOMAIN_LISTENER = DOMAIN + '_listener'

CONF_APARTMENT = 'apartment'

# # Validation of the user's configuration
CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_HOST, default='https://dss.local:8080'): cv.string,
        vol.Required(CONF_USERNAME, default='dssadmin'): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Required(CONF_APARTMENT): cv.string,
    })
}, extra=vol.ALLOW_EXTRA)


async def async_setup(hass, config):
    _LOGGER.info('digitalstrom setup started')
    import urllib3
    from pydigitalstrom.client import DSClient
    from pydigitalstrom.exceptions import DSException

    # disable urllib ssl warnings since most dss servers don't use certificates
    urllib3.disable_warnings()

    # load config
    host = config[DOMAIN][CONF_HOST]
    username = config[DOMAIN][CONF_USERNAME]
    password = config[DOMAIN][CONF_PASSWORD]
    apartment_name = config[DOMAIN][CONF_APARTMENT]
    config_path = hass.config.path('.digitalstrom/auth.json')

    # get/validate apptoken
    hass.data[DOMAIN] = DSClient(
        host=host, username=username, password=password,
        config_path=config_path, apartment_name=apartment_name)
    try:
        await hass.data[DOMAIN].get_application_token()
    except DSException:
        raise PlatformNotReady(
            'Failed to retrieve apptoken from digitalSTROM server at %s', host)
        return False

    _LOGGER.info(
        'Successfully retrieved apptoken from digitalSTROM server at %s', host)

    # load all scenes
    await hass.data[DOMAIN].initialize()

    # register devices
    hass.async_add_job(discovery.async_load_platform(
        hass, 'light', DOMAIN, {}, config))
    hass.async_add_job(discovery.async_load_platform(
        hass, 'cover', DOMAIN, {}, config))
    hass.async_add_job(discovery.async_load_platform(
        hass, 'scene', DOMAIN, {}, config))
    hass.async_add_job(discovery.async_load_platform(
        hass, 'sensor', DOMAIN, {}, config))

    _LOGGER.info('preparing digitalstrom event listener')
    from pydigitalstrom.listener import DSEventListener
    from homeassistant.core import callback
    from homeassistant.const import EVENT_HOMEASSISTANT_START
    from homeassistant.const import EVENT_HOMEASSISTANT_STOP
    hass.data[DOMAIN_LISTENER] = DSEventListener(
        client=hass.data[DOMAIN], event_id=1, event_name='callScene', 
        timeout=1, loop=hass.loop)

    @callback
    def digitalstrom_start_listener(_):
        _LOGGER.info('digitalstrom event listener started')
        hass.async_add_job(hass.data[DOMAIN_LISTENER].start)

    hass.bus.async_listen_once(
        EVENT_HOMEASSISTANT_START, digitalstrom_start_listener)

    @callback
    def digitalstrom_stop_listener(_):
        _LOGGER.info('digitalstrom event listener stopped')
        hass.async_add_job(hass.data[DOMAIN_LISTENER].stop)

    hass.bus.async_listen_once(
        EVENT_HOMEASSISTANT_STOP, digitalstrom_stop_listener)

    return True
