import appdaemon.plugins.hass.hassapi as hass


class StateDarknessCoverShutdown(hass.Hass):
    def initialize(self):
        self.timer = None

        self.indicator = self.args['indicator']
        self.time = self.args['time']

        # set the shutdown timer
        self.set_timer()

        # listen to state changes on the time input and reset the timer
        self.listen_state(callback=self.set_timer, entity=self.time)

        # deactivate shutdown on sunrise
        self.run_at_sunrise(self.deactivate)

    def set_timer(self, *args, **kwargs):
        self.log('(re)setting timer for {}'.format(self.indicator))

        # cancel existing timer
        if self.timer:
            self.cancel_timer(self.timer)

        start_time = self.parse_time(self.get_state(self.time))
        self.timer = self.run_daily(callback=self.activate, start=start_time)

    def activate(self, *args, **kwargs):
        self.log('darkness shutdown turned on for {}'.format(self.indicator))
        self.turn_on(self.indicator)

    def deactivate(self, *args, **kwargs):
        self.log('darkness shutdown turned off for {}'.format(self.indicator))
        self.turn_off(self.indicator)
