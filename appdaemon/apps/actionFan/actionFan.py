import appdaemon.plugins.hass.hassapi as hass


class HandleActionFan(hass.Hass):

    def initialize(self):
        self.delayer = self.get_app('util_delayer')
        self.timer_trigger = None
        self.timer_cycle = None
        self.fan = self.args['fan']
        self.trigger = self.args['trigger']
        self.delay = self.args['delay']
        self.indicator_presence = self.args['indicator_presence']
        self.absent_on_duration = self.args['absent_on_duration']
        self.absent_off_duration = self.args['absent_off_duration']

        """
        turn the bathroom fans on when the main bathroom light has been activated.
        keep them running for two minutes after the main bathroom light has been turned off.
        """
        self.listen_state(cb=self.trigger_on, entity=self.trigger, new='on', old='off')
        self.listen_state(cb=self.trigger_off, entity=self.trigger, new='off', old='on')

        """
        run a fan on/off cycle when noone's home to exchange more air in the apartment
        """
        self.listen_state(self.leaving, self.indicator_presence, new='False', old='True')
        self.listen_state(self.returning, self.indicator_presence, new='True', old='False')

    def trigger_on(self, *args, **kwargs):
        self.log('{} turned on, now turn on {}'.format(self.trigger, self.fan))
        self.delayer.add(hass_func='turn_on', entity_id=self.fan)

        # cancel last scheduler
        if self.timer_trigger is not None:
            self.cancel_timer(self.timer_trigger)

    def trigger_off(self, *args, **kwargs):
        self.log('{} turned off, turn off {} in {} minutes'.format(self.trigger, self.fan, self.delay))
        self.timer_trigger = self.run_in(callback=self.trigger_off_delayed, seconds=int(self.delay) * 60)

    def trigger_off_delayed(self, *args, **kwargs):
        self.log('{} minutes over, turn off {}'.format(self.delay, self.fan))
        self.delayer.add(hass_func='turn_off', entity_id=self.fan)
        self.timer_trigger = None

    def leaving(self, *args, **kwargs):
        self.absent_turn_on()

    def returning(self, *args, **kwargs):
        if self.timer_cycle is not None:
            self.cancel_timer(self.timer_cycle)

    def absent_turn_on(self, *args, **kwargs):
        self.log('absent - turn fan {} on'.format(self.fan))
        self.delayer.add(hass_func='turn_on', entity_id=self.fan)

        # set callback to turn fan back off
        self.timer_cycle = self.run_in(self.absent_turn_off_fans, self.absent_on_duration * 60)

    def absent_turn_off(self, *args, **kwargs):
        self.log('absent - turn fan {} off'.format(self.fan))
        self.delayer.add(hass_func='turn_off', entity_id=self.fan)

        # set callback to turn fan back on
        self.timer_cycle = self.run_in(self.absent_turn_on_fans, self.absent_off_duration * 60)
