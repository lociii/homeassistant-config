import appdaemon.plugins.hass.hassapi as hass


class HandleStateDarkness(hass.Hass):
    def __init__(self, *args, **kwargs):
        self.timer_sunset = None
        self.timer_sunrise = None
        super().__init__(*args, **kwargs)

        self.indicator = self.args['indicator']
        self.offset = self.args['offset']

    def initialize(self):
        self.set_timers()

        # listen to state changes on the offset inputs and reset the timers
        self.listen_state(cb=self.set_timers, entity=self.offset)

    def set_timers(self, *args, **kwargs):
        self.log('(re)setting sunset/sunrise timers for {}'.format(self.indicator))

        # cancel existing timers
        if self.timer_sunset:
            self.cancel_timer(self.timer_sunset)
        if self.timer_sunrise:
            self.cancel_timer(self.timer_sunrise)

        offset = int(float(self.get_state(self.offset)))
        self.timer_sunset = self.run_at_sunset(self.callback_sunset, offset=offset)
        self.timer_sunrise = self.run_at_sunrise(self.callback_sunrise, offset=offset * -1)

    def callback_sunset(self, *args, **kwargs):
        self.log('sunset for {}'.format(self.indicator))
        self.turn_on(self.indicator)

    def callback_sunrise(self, *args, **kwargs):
        self.log('sunrise for {}'.format(self.indicator))
        self.turn_off(self.indicator)
