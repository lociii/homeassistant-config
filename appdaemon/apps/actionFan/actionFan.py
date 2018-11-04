import appdaemon.plugins.hass.hassapi as hass


class HandleActionFan(hass.Hass):
    """
    turn the bathroom fans on when the main bathroom light has been activated.
    keep them running for two minutes after the main bathroom light has been turned off.
    """
    def initialize(self):
        self.timer = None

        # listen to state changes of triggering device
        self.listen_state(cb=self.turn_target_device_on, entity=self.args['source_device'], new='on', old='off')
        self.listen_state(cb=self.turn_target_device_off, entity=self.args['source_device'], new='off', old='on')

    def turn_target_device_on(self, *args, **kwargs):
        self.log('{} turned on, now turn on {}'.format(self.args['source_device'], self.args['target_device']))
        self.turn_on(entity_id=self.args['target_device'])

        # cancel last scheduler
        if self.timer is not None:
            self.cancel_timer(self.handler)

    def turn_target_device_off(self, *args, **kwargs):
        self.log('{} turned off, turn off {} in 10 minutes'.format(self.args['source_device'], self.args['target_device']))
        self.timer = self.run_in(callback=self.turn_target_device_off_delayed, seconds=int(self.args['delay'])*60)

    def turn_target_device_off_delayed(self, *args, **kwargs):
        self.log('10 minutes gone, turn off {}'.format(self.args['target_device']))
        self.turn_off(entity_id=self.args['target_device'])
        self.timer = None
