import appdaemon.plugins.hass.hassapi as hass
import datetime
from globals import WATERING_AREA_1, WATERING_AREA_2, WATERING_AREA_3


class HandleWatering(hass.Hass):
    def initialize(self):
        self.timer_night = None
        self.timers = []
        self.listen_state(self.watering_activate, self.args['input_boolean'], new='on')
        self.listen_state(self.watering_deactivate, self.args['input_boolean'], new='off')

    def watering_activate(self, event_name, data, *args, **kwargs):
        self.speak(self.args['message_on'])
        if self.args['start_hour']:
            self.timer_night = self.run_once(
                self.watering_start, datetime.time(self.args['start_hour'], 0, 0))
        else:
            self.watering_start()

    def watering_deactivate(self, event_name, data, *args, **kwargs):
        self.watering_stop()

    def watering_start(self, *args, **kwargs):
        start_area_1 = 0
        stop_area_1 = start_area_1 + self.args['duration_area_1']
        start_area_2 = stop_area_1 + self.args['delay']
        stop_area_2 = start_area_2 + self.args['duration_area_2']
        start_area_3 = stop_area_2 + self.args['delay']
        stop_area_3 = start_area_3 + self.args['duration_area_3']
        end_automation = stop_area_3 + self.args['delay']

        self.log('area1: {} bis {}, area2: {} bis {}, area3: {} bis {}'.format(
            start_area_1, stop_area_1, start_area_2, stop_area_2, start_area_3, stop_area_3
        ))

        self.timers.append(self.run_in(callback=self.area_1_on, seconds=start_area_1))
        self.timers.append(self.run_in(callback=self.area_1_off, seconds=stop_area_1))
        self.timers.append(self.run_in(callback=self.area_2_on, seconds=start_area_2))
        self.timers.append(self.run_in(callback=self.area_2_off, seconds=stop_area_2))
        self.timers.append(self.run_in(callback=self.area_3_on, seconds=start_area_3))
        self.timers.append(self.run_in(callback=self.area_3_off, seconds=stop_area_3))
        self.timers.append(self.run_in(callback=self.stop_automation, seconds=end_automation))

    def area_1_on(self, *args, **kwargs):
        self.turn_on(entity_id=WATERING_AREA_1)

    def area_1_off(self, *args, **kwargs):
        self.turn_off(entity_id=WATERING_AREA_1)

    def area_2_on(self, *args, **kwargs):
        self.turn_on(entity_id=WATERING_AREA_2)

    def area_2_off(self, *args, **kwargs):
        self.turn_off(entity_id=WATERING_AREA_2)

    def area_3_on(self, *args, **kwargs):
        self.turn_on(entity_id=WATERING_AREA_3)

    def area_3_off(self, *args, **kwargs):
        self.turn_off(entity_id=WATERING_AREA_3)

    def stop_automation(self, *args, **kwargs):
        self.watering_stop()

    def watering_stop(self, *args, **kwargs):
        # stop watering timers
        for timer in self.timers:
            self.cancel_timer(timer)
        self.timers = []

        # stop all areas
        self.turn_off(entity_id=WATERING_AREA_1)
        self.turn_off(entity_id=WATERING_AREA_2)
        self.turn_off(entity_id=WATERING_AREA_3)

        # remove night timer
        if self.timer_night is not None:
            self.cancel_timer(self.timer_night)
            self.timer_night = None

        # turn trigger off
        self.turn_off(entity_id=self.args['input_boolean'])

        # notify
        if 'message_off' in self.args:
            self.speak(self.args['message_off'])

    def speak(self, message):
        self.call_service('media_player/volume_set', entity_id=self.args['media_player'], volume_level=0.5)
        self.call_service('tts/amazon_polly_say', entity_id=self.args['media_player'], message=message)
