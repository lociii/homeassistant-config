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

    def trigger_on(self, entity, attribute, old, new, kwargs):
        if self.on_delay is None:
            self.trigger_on_delayed()
        else:
            self.timer_on = self.run_in(callback=self.trigger_on_delayed, seconds=int(self.on_delay))

    def trigger_on_delayed(self, *args, **kwargs):
        for entity in self.action_entities:
            self.delayer.add(hass_func='turn_on', entity_id=entity)
        self.timer_on = None

    def trigger_off(self, entity, attribute, old, new, kwargs):
        # directly turn off if no delay is set or the start delay is not yet over
        if self.off_delay is None or self.timer_on is not None:
            self.trigger_off_delayed()
        else:
            self.timer_off = self.run_in(callback=self.trigger_off_delayed, seconds=int(self.off_delay))

    def trigger_off_delayed(self, *args, **kwargs):
        for entity in self.action_entities:
            self.delayer.add(hass_func='turn_off', entity_id=entity)
        self.timer_off = None

        # cancel on timer to prevent delayed activation
        if self.timer_on is not None:
            self.cancel_timer(self.timer_on)
            self.timer_on = None
