import appdaemon.plugins.hass.hassapi as hass


class HandleActionLeavingHome(hass.Hass):
    def initialize(self):
        self.announce = self.get_app('announce')
        self.indicator_presence = self.args['indicator_presence']

        self.listen_state(self.leaving, self.indicator_presence, new='False', old='True')

    def leaving(self, *args, **kwargs):
        self.announce.speak(message='Komm gesund wieder!')
