import appdaemon.plugins.hass.hassapi as hass


class HandleActionLeavingHome(hass.Hass):
    def initialize(self):
        self.delayer = self.get_app('util_delayer')
        self.announce = self.get_app('announce')

        self.fans = self.args['fans']
        self.fan_on_duration = int(self.args['fan_on_duration'])
        self.fan_off_duration = int(self.args['fan_off_duration'])

        # indicators
        self.indicator_presence = self.args['indicator_presence']

        # execute when coming home
        self.listen_state(self.update_status, self.indicator_presence, new='False', old='True')

    def update_status(self, *args, **kwargs):
        self.announce.speak(message='Komm gesund wieder!')
        self.absent_turn_on_fans()

    def absent_turn_on_fans(self, *args, **kwargs):
        self.log('absent - turn fans on')

        # turn fans on
        for fan in self.fans:
            self.delayer.add(hass_func='turn_on', entity_id=fan)

        # callback in 10 minutes
        self.fan_handle = self.run_in(self.absent_turn_off_fans, self.fan_on_duration * 60)

    def absent_turn_off_fans(self, *args, **kwargs):
        self.log('absent - turn fans off')

        # turn fans off
        for fan in self.fans:
            self.delayer.add(hass_func='turn_off', entity_id=fan)

        # callback in 5 minutes
        self.fan_handle = self.run_in(self.absent_turn_on_fans, self.fan_off_duration * 60)
