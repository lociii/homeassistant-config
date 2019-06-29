import appdaemon.plugins.hass.hassapi as hass


class ActionSwitch(hass.Hass):
    def initialize(self):
        self.delayer = self.get_app('util_delayer')

        self.trigger_entity = self.args['trigger_entity']
        self.trigger_status = self.args['trigger_status']
        self.action_entities = self.args['action_entities']
        self.action_status = self.args['action_status']

        status_text = 'on' if self.trigger_status else 'off'
        self.listen_state(cb=self.update_status, entity=self.trigger_entity, new=status_text)

    def update_status(self, *args, **kwargs):
        self.log('{} turned {}'.format(self.trigger_entity, self.trigger_status))

        for entity in self.action_entities:
            if self.action_status:
                self.delayer.add(hass_func='turn_on', entity_id=entity)
            else:
                self.delayer.add(hass_func='turn_off', entity_id=entity)
