# -*- coding: UTF-8 -*-
import logging

from homeassistant.components.cover import CoverDevice, ENTITY_ID_FORMAT, \
    SUPPORT_CLOSE, SUPPORT_OPEN
from homeassistant.helpers.restore_state import async_get_last_state
from homeassistant.const import STATE_ON

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['digitalstrom']


async def async_setup_platform(hass, config, async_add_devices,
                               discovery_info=None):
    from custom_components.digitalstrom import DOMAIN, DOMAIN_LISTENER
    from pydigitalstrom.devices.scene import DSColorScene

    client = hass.data[DOMAIN]
    listener = hass.data[DOMAIN_LISTENER]
    devices = []
    scenes = client.get_scenes()
    for scene in scenes.values():
        # only handle cover (color 2) scenes
        if not isinstance(scene, DSColorScene) or scene.color != 2:
            continue
        # not an area or broadcast turn off scene
        if scene.scene_id > 4:
            continue

        # get turn on counterpart
        scene_on = scenes.get('{zone_id}.{color}.{scene_id}'.format(
            zone_id=scene.zone_id, color=scene.color, 
            scene_id=scene.scene_id + 5), None)

        # no turn on scene found, skip
        if not scene_on:
            continue

        # add cover
        _LOGGER.info('adding cover {}: {}'.format(scene.scene_id, scene.name))
        devices.append(DigitalstromCover(hass=hass, scene_on=scene_on, 
            scene_off=scene, listener=listener))

    async_add_devices(device for device in devices)


class DigitalstromCover(CoverDevice):
    def __init__(self, hass, scene_on, scene_off, listener, *args, **kwargs):
        self._hass = hass
        self._scene_on = scene_on
        self._scene_off = scene_off
        self._listener = listener
        self._state = None
        super().__init__(*args, **kwargs)

    @property
    def supported_features(self):
        """Flag supported features."""
        return SUPPORT_OPEN | SUPPORT_CLOSE

    @property
    def name(self):
        return self._scene_off.name

    @property
    def unique_id(self):
        return 'dscover.{id}'.format(id=self._scene_off.unique_id)

    @property
    def available(self):
        return True

    @property
    def is_closed(self):
        return None

    async def async_open_cover(self, **kwargs):
        _LOGGER.info('calling cover scene {}'.format(self._scene_on.scene_id))
        await self._scene_on.turn_on()

    async def async_close_cover(self, **kwargs):
        _LOGGER.info('calling cover scene {}'.format(self._scene_off.scene_id))
        await self._scene_off.turn_on()

    def should_poll(self):
        return False
