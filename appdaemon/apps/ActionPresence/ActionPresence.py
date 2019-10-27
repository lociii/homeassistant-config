import appdaemon.plugins.hass.hassapi as hass


class ActionPresence(hass.Hass):
    def initialize(self):
        self.announcer = self.get_app('util_announcer')
        self.indicator_presence = self.args['indicator_presence']

        self.listen_state(callback=self.present, entity=self.indicator_presence, new='on', old='off')
        self.listen_state(callback=self.absent, entity=self.indicator_presence, new='off', old='on')

    def present(self, *args, **kwargs):
        self.announcer.speak(message='Willkommen zurück!')

    def absent(self, *args, **kwargs):
        self.announcer.speak(message='Komm gesund wieder!')
