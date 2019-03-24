# -*- coding: UTF-8 -*-
import logging

from homeassistant.components.light import Light, ENTITY_ID_FORMAT
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.const import STATE_ON

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['digitalstrom']


async def async_setup_platform(hass, config, async_add_devices,
                               discovery_info=None):
    from ..digitalstrom.const import DOMAIN, DOMAIN_LISTENER
    from pydigitalstrom.devices.scene import DSColorScene

    client = hass.data[DOMAIN]
    listener = hass.data[DOMAIN_LISTENER]
    devices = []
    scenes = client.get_scenes()
    for scene in scenes.values():
        # only handle light (color 1) scenes
        if not isinstance(scene, DSColorScene) or scene.color != 1:
            continue
        # not an area or broadcast turn off scene
        if scene.scene_id > 4:
            continue

        # get turn on counterpart
        scene_on = scenes.get('{zone_id}_{color}_{scene_id}'.format(
            zone_id=scene.zone_id, color=scene.color,
            scene_id=scene.scene_id + 5), None)

        # no turn on scene found, skip
        if not scene_on:
            continue

        # add light
        _LOGGER.info('adding light {}: {}'.format(scene.scene_id, scene.name))
        devices.append(DigitalstromLight(hass=hass, scene_on=scene_on,
            scene_off=scene, listener=listener))

    async_add_devices(device for device in devices)


class DigitalstromLight(RestoreEntity, Light):
    def __init__(self, hass, scene_on, scene_off, listener, *args, **kwargs):
        self._hass = hass
        self._scene_on = scene_on
        self._scene_off = scene_off
        self._listener = listener
        self._state = None
        super().__init__(*args, **kwargs)

        self.register_callback()

    def register_callback(self):
        async def event_callback(event):
            # sanity checks
            if 'name' not in event:
                return
            if event['name'] != 'callScene':
                return
            if 'properties' not in event:
                return
            if 'sceneID' not in event['properties']:
                return
            if 'groupID' not in event['properties']:
                return
            if 'zoneID' not in event['properties']:
                return

            # cast event data
            zone_id = int(event['properties']['zoneID'])
            group_id = int(event['properties']['groupID'])
            scene_id = int(event['properties']['sceneID'])

            # device turned on or broadcast turned on
            if self._scene_on.zone_id == zone_id and \
                self._scene_on.color == group_id and \
                    (self._scene_on.scene_id == scene_id or 5 == scene_id):
                self._state = True
                await self.async_update_ha_state()
            # device turned off or broadcast turned off
            elif self._scene_off.zone_id == zone_id and \
                self._scene_off.color == group_id and \
                    (self._scene_off.scene_id == scene_id or 0 == scene_id):
                self._state = False
                await self.async_update_ha_state()

        self._listener.register(callback=event_callback)

    @property
    def name(self):
        return self._scene_off.name

    @property
    def unique_id(self):
        return 'dslight_{id}'.format(id=self._scene_off.unique_id)

    @property
    def available(self):
        return True

    @property
    def is_on(self):
        return self._state

    async def async_turn_on(self, **kwargs):
        await self._scene_on.turn_on()
        self._state = True

    async def async_turn_off(self, **kwargs):
        await self._scene_off.turn_on()
        self._state = False

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        state = await self.async_get_last_state()
        if not state:
            return

        _LOGGER.debug('trying to restore state of entity {} to {}'.format(self.entity_id, state.state))
        self._state = state.state == STATE_ON

    def should_poll(self):
        return False
