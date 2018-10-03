import appdaemon.plugins.hass.hassapi as hass
import asyncio
from globals import DAY_START, NIGHT_START
from globals import COVERS_ALL, LIGHTS_ALL
from globals import COVERS_NIGHT_ABSENT, LIGHTS_NIGHT_RETURNING
from globals import FANS
from globals import GOOGLE_TTS_DEVICE
from globals import SENSOR_APARTMENT_PRESENCE


class HandlePresence(hass.Hass):
    def initialize(self):
        self.fan_handle = None

        self.listen_state(self.leaving, SENSOR_APARTMENT_PRESENCE, new='False', old='True')
        # leaving during the night
        self.listen_state(self.leaving_night, SENSOR_APARTMENT_PRESENCE, new='False', old='True', 
            constrain_start_time=NIGHT_START, constrain_end_time=DAY_START)
        # leaving during the day
        self.listen_state(self.leaving_day, SENSOR_APARTMENT_PRESENCE, new='False', old='True', 
            constrain_start_time=DAY_START, constrain_end_time=NIGHT_START)

        # returning home
        self.listen_state(self.returning, SENSOR_APARTMENT_PRESENCE, new='True', old='False')
        # returning home at night
        self.listen_state(self.returning_night, SENSOR_APARTMENT_PRESENCE, new='True', old='False', 
            constrain_start_time=NIGHT_START, constrain_end_time=DAY_START)

    def speak(self, message):
        self.call_service('media_player/volume_set', entity_id=GOOGLE_TTS_DEVICE, volume_level=0.5)
        self.call_service('tts/google_say', entity_id=GOOGLE_TTS_DEVICE, message=message)

    def leaving(self, entity, attribute, old, new, kwargs):
        self.log('leaving')
        self.speak('Komm gesund wieder!')

        # start fan loop, activate for 10 minutes every 15 minutes
        self.absent_turn_on_fans()

    def absent_turn_on_fans(self, *args, **kwargs):
        self.log('absent - turn fans on')

        # turn fans on
        for fan in FANS:
            self.turn_on(fan)
            asyncio.sleep(0.5)
        # callback in 10 minutes
        self.fan_handle = self.run_in(self.absent_turn_off_fans, 10 * 60)

    def absent_turn_off_fans(self, *args, **kwargs):
        self.log('absent - turn fans off')

        # turn fans off
        for fan in FANS:
            self.turn_off(fan)
            asyncio.sleep(0.5)
        # callback in 5 minutes
        self.fan_handle = self.run_in(self.absent_turn_on_fans, 5 * 60)

    def leaving_night(self, entity, attribute, old, new, kwargs):
        self.log('leaving at night')

        # close all covers
        for cover in COVERS_ALL:
            self.set_state(entity_id=cover, state='closed')
            asyncio.sleep(0.5)

        # turn most lights off
        for light in LIGHTS_ALL:
            if light in LIGHTS_NIGHT_ABSENT:
                self.turn_on(entity_id=light)
            else:
                self.turn_off(entity_id=light)
            asyncio.sleep(0.5)

    def leaving_day(self, entity, attribute, old, new, kwargs):
        self.log('leaving at day')

        # turn all lights off
        for light in LIGHTS_ALL:
            self.turn_off(entity_id=light)
            asyncio.sleep(0.5)

    def returning(self, entity, attribute, old, new, kwargs):
        self.log('returning')
        self.speak('Willkommen zurück!')

        # cancel fan loop
        if self.fan_handle is not None:
            self.cancel_timer(self.fan_handle)

        # turn fans off
        for fan in FANS:
            self.turn_off(fan)
            asyncio.sleep(0.5)

    def returning_night(self, entity, attribute, old, new, kwargs):
        self.log('returning at night')

        # turn on some lights
        for light in LIGHTS_NIGHT_RETURNING:
            self.turn_on(entity_id=light)
            asyncio.sleep(0.5)
