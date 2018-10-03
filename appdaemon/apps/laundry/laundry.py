import appdaemon.plugins.hass.hassapi as hass


class HandleMachineState(hass.Hass):
    def initialize(self):
        self.listen_state(cb=self.handle_power_usage, entity=self.args['sensor'])
        self.listen_state(cb=self.handle_state_change, entity=self.args['input_select'], 
            new='Fertig', old='Aktiv')

    def handle_power_usage(self, entity, attribute, old, new, **kwargs):
        usage = int(float(new))

        if usage < self.args['usage_off']:
            self.set_state(entity_id=self.args['input_select'], state='Aus')
        elif usage > self.args['usage_active']: 
            self.set_state(entity_id=self.args['input_select'], state='Aktiv')
        else:
            self.set_state(entity_id=self.args['input_select'], state='Fertig')

    def handle_state_change(self, *args, **kwargs):
        self.log('laundry machine is done: {}'.format('a'))
        self.speak(message=self.args['message'])

    def speak(self, message):
        self.call_service('media_player/volume_set', entity_id=self.args['media_player'], volume_level=0.5)
        self.call_service('tts/google_say', entity_id=self.args['media_player'], message=message)
