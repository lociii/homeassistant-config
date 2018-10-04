import appdaemon.plugins.hass.hassapi as hass


class HandleFan(hass.Hass):
    def initialize(self):
        self.handler = None
        self.listen_state(cb=self.turn_target_device_on, entity=self.args['source_device'], new='on', old='off')
        self.listen_state(cb=self.turn_target_device_off, entity=self.args['source_device'], new='off', old='on')

    def turn_target_device_on(self, *args, **kwargs):
        self.log('{} turned on, now turn on {}'.format(self.args['source_device'], self.args['target_device']))
        self.turn_on(entity_id=self.args['target_device'])

        # cancel last scheduler
        if self.handler is not None:
            self.cancel_timer(self.handler)

    def turn_target_device_off(self, *args, **kwargs):
        self.log('{} turned off, turn off {} in 10 minutes'.format(self.args['source_device'], self.args['target_device']))
        self.handler = self.run_in(callback=self.turn_target_device_off_delayed, seconds=2*60)

    def turn_target_device_off_delayed(self, *args, **kwargs):
        self.log('10 minutes gone, turn off {}'.format(self.args['target_device']))
        self.turn_off(entity_id=self.args['target_device'])
        self.handler = None
