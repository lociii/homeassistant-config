import appdaemon.plugins.hass.hassapi as hass
import time
from globals import LIGHTS_ALL, COVERS_ALL


class HandleSleeping(hass.Hass):
    def initialize(self):
        self.listen_state(self.sleep, 'sensor.apartment__sleeping', new='True', old='False')
        self.listen_state(self.wakeup, 'sensor.apartment__sleeping', new='False', old='True')

    def sleep(self, *args, **kwargs):
        self.log('sleep')

        for cover in COVERS_ALL:
            self.call_service('cover/close_cover', entity_id=cover)
            time.sleep(0.5)
        for light in LIGHTS_ALL:
            self.turn_off(entity_id=light)
            time.sleep(0.5)

    def wakeup(self, *args, **kwargs):
        self.log('wake up')

        for cover in COVERS_ALL:
            self.call_service('cover/open_cover', entity_id=cover)
            time.sleep(0.5)
