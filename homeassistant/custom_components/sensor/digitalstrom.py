# -*- coding: UTF-8 -*-
import logging

from homeassistant.helpers.entity import Entity
from homeassistant.helpers.restore_state import async_get_last_state
from homeassistant.const import STATE_ON

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['digitalstrom']


async def async_setup_platform(hass, config, async_add_devices,
                               discovery_info=None):
    from custom_components.digitalstrom import DOMAIN, DOMAIN_LISTENER
    from pydigitalstrom.devices.scene import DSScene

    client = hass.data[DOMAIN]
    listener = hass.data[DOMAIN_LISTENER]
    devices = []
    scenes = client.get_scenes()
    for scene in scenes.values():
        # only handle scenes
        if not isinstance(scene, DSScene):
            continue
        # only sleeping and present
        if scene.scene_id not in [69, 71]:
            continue

        # get turn on counterpart
        scene_off = scenes.get('{zone_id}.{scene_id}'.format(
            zone_id=scene.zone_id, scene_id=scene.scene_id + 1), None)

        # no turn off scene found, skip
        if not scene_off:
            continue

        # add sensors
        devices.append(DigitalstromSensor(hass=hass, scene_on=scene, 
            scene_off=scene_off, listener=listener))

    async_add_devices(device for device in devices)


class DigitalstromSensor(Entity):
    def __init__(self, hass, scene_on, scene_off, listener, *args, **kwargs):
        self._hass = hass
        self._scene_on = scene_on
        self._scene_off = scene_off
        self._listener = listener
        self._state = None

        # sleeping default is false
        if self._scene_on.scene_id == 69:
            self._state = False
        # present default is true
        elif self._scene_on.scene_id == 71:
            self._state = True
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
            if 'zoneID' not in event['properties']:
                return

            # cast event data
            zone_id = int(event['properties']['zoneID'])
            scene_id = int(event['properties']['sceneID'])

            # turn on scene called
            if self._scene_on.zone_id == zone_id and \
                    self._scene_on.scene_id == scene_id:
                self._state = True
                await self.async_update_ha_state()
            # turn off scene called
            elif self._scene_off.zone_id == zone_id and \
                    self._scene_off.scene_id == scene_id:
                self._state = False
                await self.async_update_ha_state()

        self._listener.register(callback=event_callback)

    @property
    def name(self):
        return self._scene_on.name

    @property
    def unique_id(self):
        return 'dslight.{id}'.format(id=self._scene_on.unique_id)

    @property
    def available(self):
        return True

    @property
    def state(self):
        return self._state

    async def async_added_to_hass(self):
        state = await async_get_last_state(self._hass, self.entity_id)
        if state:
            self._state = state.state == STATE_ON

    def should_poll(self):
        return False
