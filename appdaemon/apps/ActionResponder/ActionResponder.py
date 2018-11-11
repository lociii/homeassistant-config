import appdaemon.plugins.hass.hassapi as hass


class ActionResponder(hass.Hass):
    """
    trigger on/off actions on a list of devices triggered by a single other device
    supports on/off delay (in seconds)

    might be used to trigger non-digitalstrom devices based on digitalstrom scene changes
    """
    def initialize(self):
        self.delayer = self.get_app('util_delayer')
        self.timer_on = None
        self.timer_off = None

        self.trigger_entity = self.args['trigger_entity']
        self.action_entities = self.args['action_entities']
        self.on_delay = self.args.get('on_delay', None)
        self.off_delay = self.args.get('off_delay', None)

        self.listen_state(self.trigger_on, self.trigger_entity, new='on', old='off')
        self.listen_state(self.trigger_off, self.trigger_entity, new='off', old='on')

    def trigger_on(self, *args, **kwargs):
        # instant on or responder still active
        if self.on_delay is None or self.timer_off is not None:
            self.trigger_on_delayed()
        else:
            self.log('{} turned on, delayed responder in {} seconds'.format(self.trigger_entity, int(self.on_delay)))
            self.timer_on = self.run_in(callback=self.trigger_on_delayed, seconds=int(self.on_delay))

    def trigger_on_delayed(self, *args, **kwargs):
        for entity in self.action_entities:
            self.log('{} turned on, now turn on {} as response'.format(self.trigger_entity, entity))
            self.delayer.add(hass_func='turn_on', entity_id=entity)

        # reset on timer
        if self.timer_on is not None:
            self.cancel_timer(self.timer_on)
            self.timer_on = None

        # cancel on timer to prevent delayed deactivation
        if self.timer_off is not None:
            self.cancel_timer(self.timer_off)
            self.timer_off = None

    def trigger_off(self, *args, **kwargs):
        if self.off_delay is None or self.timer_on is not None:
            self.trigger_off_delayed()
        else:
            self.log('{} turned off, delayed responder in {} seconds'.format(self.trigger_entity, int(self.off_delay)))
            self.timer_off = self.run_in(callback=self.trigger_off_delayed, seconds=int(self.off_delay))

    def trigger_off_delayed(self, *args, **kwargs):
        for entity in self.action_entities:
            self.log('{} turned off, now turn off {} as response'.format(self.trigger_entity, entity))
            self.delayer.add(hass_func='turn_off', entity_id=entity)

        # reset off timer
        if self.timer_off is not None:
            self.cancel_timer(self.timer_off)
            self.timer_off = None

        # cancel on timer to prevent delayed activation
        if self.timer_on is not None:
            self.cancel_timer(self.timer_on)
            self.timer_on = None
