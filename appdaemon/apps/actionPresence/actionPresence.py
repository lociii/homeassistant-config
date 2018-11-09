import appdaemon.plugins.hass.hassapi as hass


class HandleActionPresence(hass.Hass):
    def initialize(self):
        self.announce = self.get_app('announce')
        self.indicator_presence = self.args['indicator_presence']

        self.listen_state(self.present, self.indicator_presence, new='on', old='off')
        self.listen_state(self.absent, self.indicator_presence, new='off', old='on')

    def present(self, *args, **kwargs):
        self.announce.speak(message='Willkommen zurück!')

    def absent(self, *args, **kwargs):
        self.announce.speak(message='Komm gesund wieder!')
