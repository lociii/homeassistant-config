import appdaemon.plugins.hass.hassapi as hass


class ActionWatering(hass.Hass):
    def initialize(self):
        self.announcer = self.get_app('util_announcer')
        self.delayer = self.get_app('util_delayer')

        self.area_timers = []

        self.trigger = self.args['trigger']
        self.areas = self.args['areas']
        self.message_on = self.args['message_on']
        self.message_off = self.args['message_off']

        # triggers for instant watering
        self.listen_state(self.activate, self.trigger, new='on', old='off')
        self.listen_state(self.deactivate, self.trigger, new='off', old='on')

    def activate(self, *args, **kwargs):
        delay = 0
        for area in self.areas:
            self.area_timers.append(self.run_in(
                callback=self.start_area, delay=delay, start_action='turn_on', start_entity=area['entity']))
            delay += int(float(self.get_state(area['duration']))) * 60
            self.area_timers.append(self.run_in(
                callback=self.start_area, delay=delay, start_action='turn_off', start_entity=area['entity']))
            delay += 15

        # turn the trigger off
        self.area_timers.append(self.run_in(callback=self.finalize, delay=delay))

        # announce start
        self.announcer.speak(self.message_on)
        self.log('watering cycle started')

    def finalize(self, *args, **kwargs):
        # turn the trigger off which will also deactivate everyting and announce the end of the cycle
        self.turn_off(self.trigger)

    def start_area(self, kwargs):
        self.delayer.add(hass_func=kwargs.get('start_action'), entity_id=kwargs.get('start_entity'))

    def deactivate(self, *args, **kwargs):
        # stop timers
        for timer in self.area_timers:
            self.cancel_timer(timer)
        self.area_timers = []

        # turn off all areas
        for area in self.areas:
            self.delayer.add(hass_func='turn_off', entity_id=area['entity'])

        self.announcer.speak(self.message_off)
        self.log('watering cycle finished')
