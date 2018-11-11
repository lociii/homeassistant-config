import appdaemon.plugins.hass.hassapi as hass


class StateDarknessCoverProtection(hass.Hass):
    def initialize(self):
        self.timer = None

        self.indicator = self.args['indicator']
        self.offset = self.args['offset']

        # set the shutdown timer
        self.set_timer()

        # listen to state changes on the offset inputs and reset the timers
        self.listen_state(cb=self.set_timer, entity=self.offset)

        # deactivate protection on sunrise
        self.run_at_sunrise(self.deactivate)

    def set_timer(self, *args, **kwargs):
        self.log('(re)setting timer for {}'.format(self.indicator))

        # cancel existing timer
        if self.timer:
            self.cancel_timer(self.timer)

        offset = int(float(self.get_state(self.offset)))
        self.timer = self.run_at_sunrise(self.activate, offset=offset)

    def activate(self, *args, **kwargs):
        self.log('darkness sunlight protection turned on for {}'.format(self.indicator))
        self.turn_on(self.indicator)

    def deactivate(self, *args, **kwargs):
        self.log('darkness sunlight protection turned off for {}'.format(self.indicator))
        self.turn_off(self.indicator)
