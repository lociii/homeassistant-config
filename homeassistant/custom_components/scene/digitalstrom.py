# -*- coding: UTF-8 -*-
import logging

from homeassistant.components.scene import Scene

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['digitalstrom']


async def async_setup_platform(hass, config, async_add_devices,
                               discovery_info=None):
    from custom_components.digitalstrom import DOMAIN
    from pydigitalstrom.devices.scene import DSColorScene

    client = hass.data[DOMAIN]
    scenes = []
    for scene in client.get_scenes().values():
        _LOGGER.info('adding scene {}: {}'.format(scene.scene_id, scene.name))
        scenes.append(DigitalstromScene(scene=scene))
    async_add_devices(scene for scene in scenes)


class DigitalstromScene(Scene):
    """Representation of a digitalSTROM scene."""
    def __init__(self, scene, *args, **kwargs):
        self._scene = scene
        super().__init__(*args, **kwargs)

    @property
    def name(self):
        return self._scene.name

    @property
    def unique_id(self):
        return 'dsscene.{id}'.format(id=self._scene.unique_id)

    async def async_activate(self):
        _LOGGER.info('calling scene {}'.format(self._scene.scene_id))
        await self._scene.turn_on()

    def should_poll(self):
        return False
