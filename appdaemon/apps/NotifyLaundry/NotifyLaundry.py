import appdaemon.plugins.hass.hassapi as hass


class NotifyLaundry(hass.Hass):
    def initialize(self):
        self.announcer = self.get_app('util_announcer')
        self.trigger = self.args['trigger']
        self.message = self.args['message']

        self.listen_state(callback=self.callback, entity=self.trigger, new='Fertig', old='Aktiv')

    def callback(self, *args, **kwargs):
        self.log('laundry is done')
        self.announcer.speak(message=self.message)
