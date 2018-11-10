import appdaemon.plugins.hass.hassapi as hass


class StateWateringNight(hass.Hass):
    def initialize(self):
        self.announcer = self.get_app('util_announcer')

        self.timer = None

        self.trigger = self.args['trigger']
        self.start = self.args['start']
        self.target = self.args['target']
        self.message_on = self.args['message_on']
        self.message_off = self.args['message_off']

        self.listen_state(cb=self.set_timer, entity=self.trigger, new='on', old='off')
        self.listen_state(cb=self.deactivate, entity=self.trigger, new='off', old='on')

    def set_timer(self, *args, **kwargs):
        self.log('setting timer for {}'.format(self.trigger))

        # cancel existing timer
        self.deactivate()

        # set timer
        start_time = self.parse_time(self.get_state(self.start))
        self.timer = self.run_once(self.activate, start_time)

        # announce status
        self.announcer.speak(self.message_on)

    def activate(self, *args, **kwargs):
        self.turn_on(self.target)

    def deactivate(self, *args, **kwargs):
        if self.timer is not None:
            self.cancel_timer(self.timer)

        # announce status
        self.announcer.speak(self.message_off)
