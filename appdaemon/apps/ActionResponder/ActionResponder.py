import appdaemon.plugins.hass.hassapi as hass


class ActionResponder(hass.Hass):
    """
    trigger on/off actions on a list of devices triggered by a single device

    might be used to trigger non-digitalstrom devices based on digitalstrom scene changes
    """
    def initialize(self):
        self.delayer = self.get_app('util_delayer')

        self.trigger_entity = self.args['trigger_entity']
        self.action_entities = self.args['action_entities']

        self.listen_state(self.trigger_on, self.trigger_entity, new='on', old='off')
        self.listen_state(self.trigger_off, self.trigger_entity, new='off', old='on')

    def trigger_on(self, entity, attribute, old, new, kwargs):
        for entity in self.action_entities:
            self.delayer.add(hass_func='turn_on', entity_id=entity)

    def trigger_off(self, entity, attribute, old, new, kwargs):
        for entity in self.action_entities:
            self.delayer.add(hass_func='turn_off', entity_id=entity)
