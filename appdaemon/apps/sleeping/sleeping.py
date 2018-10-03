import appdaemon.plugins.hass.hassapi as hass
import asyncio
from globals import LIGHTS_ALL, COVERS_ALL


class HandleSleeping(hass.Hass):
    def initialize(self):
        self.listen_state(self.sleep, 'sensor.apartment__sleeping', new='True', old='False')
        self.listen_state(self.wakeup, 'sensor.apartment__sleeping', new='False', old='True')

    def sleep(self, *args, **kwargs):
        self.log('sleep')

        for cover in COVERS_ALL:
            self.set_state(entity_id=cover, state='closed')
            asyncio.sleep(0.5)
        for light in LIGHTS_ALL:
            self.turn_off(entity_id=light)
            asyncio.sleep(0.5)

    def wakeup(self, *args, **kwargs):
        self.log('wake up')

        for cover in COVERS_ALL:
            self.set_state(entity_id=cover, state='open')
            asyncio.sleep(0.5)
