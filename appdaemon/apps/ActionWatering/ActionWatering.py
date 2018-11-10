import appdaemon.plugins.hass.hassapi as hass


class ActionWatering(hass.Hass):
    def initialize(self):
        self.announcer = self.get_app('util_announcer')
        self.delayer = self.get_app('util_delayer')

        self.timer_night = None
        self.area_timers = []

        self.trigger = self.args['trigger']
        self.trigger_night = self.args['trigger_night']
        self.start_night = self.args['start_night']
        self.areas = self.args['areas']
        self.message_on = self.args['message_on']
        self.message_off = self.args['message_off']
        self.message_started = self.args['message_started']
        self.message_stopped = self.args['message_stopped']

        # triggers for instant watering
        self.listen_state(self.watering_start, self.trigger, new='on')
        self.listen_state(self.watering_stop, self.trigger, new='off')

        # triggers for planned watering
        self.listen_state(cb=self.set_timer_night, entity=self.trigger_night)

    def set_timer_night(self, entity, attribute, old, new, *args, **kwargs):
        self.log('(re)setting timers for {}'.format(self.indicator))

        # cancel existing timer
        if self.timer_night:
            self.cancel_timer(self.timer_night)

        if new == 'on':
            start_time = self.parse_time(self.get_state(self.start_night))
            self.timer_night = self.run_once(self.watering_start, start_time)
            self.announcer.speak(self.message_on)
        else:
            self.watering_stop()
            self.announcer.speak(self.message_off)

    def watering_start(self, *args, **kwargs):
        delay = 0
        for area in self.areas:
            self.area_timers.append(self.run_in(
                callback=self.start_area, seconds=delay, start_action='turn_on', start_entity=area['entity']))
            delay += int(float(self.get_state(area['duration']))) * 60
            self.area_timers.append(self.run_in(
                callback=self.start_area, seconds=delay, start_action='turn_off', start_entity=area['entity']))
            delay += 15

    def start_area(self, kwargs):
        action = kwargs.get('start_action')
        entity = kwargs.get('start_entity')
        self.delayer.add(hass_func=action, entity_id=entity)

    def watering_stop(self, *args, **kwargs):
        # stop timers
        for timer in self.area_timers:
            self.cancel_timer(timer)
        self.area_timers = []

        # turn off all areas
        for area in self.areas:
            self.delayer.add(hass_func='turn_off', entity_id=area['entity'])
