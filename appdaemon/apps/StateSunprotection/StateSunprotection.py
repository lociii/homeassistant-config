import appdaemon.plugins.hass.hassapi as hass


class StateSunprotection(hass.Hass):
    def initialize(self):
        self.timer_begin = None
        self.timer_end = None

        self.switch = self.args['switch']
        self.start_time = self.args['start_time']
        self.end_time = self.args['end_time']
        self.indicator = self.args['indicator']

        # global setting turned off
        self.listen_state(cb=self.deactivate, entity=self.switch, new='off')

        # update begin timer when start time changes
        self.listen_state(cb=self.set_timer_begin, entity=self.start_time)

        # add begin and end timers
        self.set_timer_begin()
        self.set_timer_end()

    def set_timer_begin(self, *args, **kwargs):
        if self.timer_begin is not None:
            self.cancel_timer(self.timer_begin)

        start_time = self.parse_time(self.get_state(self.start_time))
        self.timer_begin = self.run_daily(callback=self.check_activate, start=start_time)

    def set_timer_end(self, *args, **kwargs):
        if self.timer_end is not None:
            self.cancel_timer(self.timer_end)

        end_time = self.parse_time(self.get_state(self.end_time))
        self.timer_end = self.run_daily(callback=self.check_deactivate, start=end_time)

    def check_activate(self, *args, **kwargs):
        # automation is deactivated
        if self.get_state(self.switch) == 'off':
            return
        self.activate()

    def check_deactivate(self, *args, **kwargs):
        # automation is deactivated
        if self.get_state(self.switch) == 'off':
            return
        self.deactivate()

    def activate(self, *args, **kwargs):
        self.log('sunprotection activated')
        self.turn_on(self.indicator)

    def deactivate(self, *args, **kwargs):
        self.log('sunprotection deactivated')
        self.turn_off(self.indicator)
