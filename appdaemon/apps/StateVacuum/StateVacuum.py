import appdaemon.plugins.hass.hassapi as hass


class StateVacuum(hass.Hass):
    def initialize(self):
        self.timer = None

        self.presence = self.args['presence']
        self.delay = self.args['delay']
        self.target = self.args['target']

        self.listen_state(cb=self.set_timer, entity=self.presence, new='off', old='on')
        self.listen_state(cb=self.deactivate, entity=self.presence, new='on', old='off')

    def set_timer(self, *args, **kwargs):
        # cancel existing timer
        self.deactivate()

        # set timer to start cleaning
        delay = int(float(self.get_state(self.delay))) * 60
        self.timer = self.run_in(callback=self.activate, seconds=delay)

        self.log('start cleaning cycle in {} seconds'.format(delay))

    def activate(self, *args, **kwargs):
        # start cleaning
        self.turn_on(self.target)

    def deactivate(self, *args, **kwargs):
        # reset timer
        if self.timer is not None:
            self.cancel_timer(self.timer)
            self.timer = None

        # deactivate cleaning
        self.turn_off(self.target)