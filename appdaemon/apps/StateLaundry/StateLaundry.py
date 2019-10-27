import appdaemon.plugins.hass.hassapi as hass


class StateLaundry(hass.Hass):
    def initialize(self):
        self.announcer = self.get_app('util_announcer')

        self.trigger = self.args['trigger']
        self.trigger_attribute = self.args['trigger_attribute']
        self.target = self.args['target']
        self.usage_off = self.args['usage_off']
        self.usage_active = self.args['usage_active']

        self.listen_state(callback=self.callback, entity=self.trigger, attribute=self.trigger_attribute)

    def callback(self, entity, attribute, old, new, *args, **kwargs):
        if new == 'unknown':
            return
        usage = int(float(new))

        if usage < self.usage_off:
            self.set_state(entity_id=self.target, state='Aus')
        elif usage > self.usage_active:
            self.set_state(entity_id=self.target, state='Aktiv')
        else:
            self.set_state(entity_id=self.target, state='Fertig')
