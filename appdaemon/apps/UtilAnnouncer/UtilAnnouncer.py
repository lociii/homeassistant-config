import appdaemon.plugins.hass.hassapi as hass


class UtilAnnouncer(hass.Hass):
    def initialize(self):
        self.device = self.args['device']

    def speak(self, message):
        self.call_service('media_player/volume_set', entity_id=self.device, volume_level=0.5)
        self.call_service('tts/amazon_polly_say', entity_id=self.device, message=message)
