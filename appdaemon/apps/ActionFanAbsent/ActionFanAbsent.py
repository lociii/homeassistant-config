import appdaemon.plugins.hass.hassapi as hass


class ActionFanAbsent(hass.Hass):
    def initialize(self):
        self.delayer = self.get_app('util_delayer')
        self.timer_cycle = None
        self.fan = self.args['fan']
        self.indicator_presence = self.args['indicator_presence']
        self.absent_on_duration = self.args['absent_on_duration']
        self.absent_off_duration = self.args['absent_off_duration']

        self.listen_state(self.leaving, self.indicator_presence, new='False', old='True')
        self.listen_state(self.returning, self.indicator_presence, new='True', old='False')

    def leaving(self, *args, **kwargs):
        self.absent_turn_on()

    def returning(self, *args, **kwargs):
        if self.timer_cycle is not None:
            self.cancel_timer(self.timer_cycle)
            self.delayer.add(hass_func='turn_off', entity_id=self.fan)

    def absent_turn_on(self, *args, **kwargs):
        self.log('absence fan cycle - turn fan {} on'.format(self.fan))
        self.delayer.add(hass_func='turn_on', entity_id=self.fan)

        # set callback to turn fan back off
        self.timer_cycle = self.run_in(self.absent_turn_off, self.absent_on_duration * 60)

    def absent_turn_off(self, *args, **kwargs):
        self.log('absence fan cycle - turn fan {} off'.format(self.fan))
        self.delayer.add(hass_func='turn_off', entity_id=self.fan)

        # set callback to turn fan back on
        self.timer_cycle = self.run_in(self.absent_turn_on, self.absent_off_duration * 60)
