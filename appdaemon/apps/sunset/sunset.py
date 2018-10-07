import appdaemon.plugins.hass.hassapi as hass
import time
from globals import COVERS_NIGHT_PRESENT, COVERS_NIGHT_ABSENT
from globals import LIGHTS_NIGHT_PRESENT, LIGHTS_NIGHT_ABSENT
from globals import NIGHT_OFFSET_LIGHT, NIGHT_OFFSET_COVER
from globals import SENSOR_APARTMENT_PRESENCE, SENSOR_APARTMENT_SLEEPING


class HandleSunset(hass.Hass):
    def initialize(self):
        self.run_at_sunset(self.sunset_light, offset=NIGHT_OFFSET_LIGHT)
        self.run_at_sunset(self.sunset_cover, offset=NIGHT_OFFSET_COVER)

    def sunset_light(self, *args, **kwargs):
        self.log('sunset, turn lights on')

        # don't do anything when we're already sleeping
        if self.get_state(entity=SENSOR_APARTMENT_SLEEPING) == 'True':
            return

        # presence
        if self.get_state(entity=SENSOR_APARTMENT_PRESENCE) == 'True':
            lights = LIGHTS_NIGHT_PRESENT
        # absence
        else:
            lights = LIGHTS_NIGHT_ABSENT
        
        # turn on lights
        for light in lights:
            self.turn_on(entity_id=light)
            time.sleep(0.5)

    def sunset_cover(self, *args, **kwargs):
        self.log('sunset, close covers')

        # don't do anything when we're already sleeping
        if self.get_state(entity=SENSOR_APARTMENT_SLEEPING) == 'True':
            return

        # presence
        if self.get_state(entity=SENSOR_APARTMENT_PRESENCE) == 'True':
            covers = COVERS_NIGHT_PRESENT
        # absence
        else:
            covers = COVERS_NIGHT_ABSENT
        
        # close covers
        for cover in covers:
            self.call_service('cover/close_cover', entity_id=cover)
            time.sleep(0.5)
