import appdaemon.plugins.hass.hassapi as hass


class NotifyCall(hass.Hass):
    def initialize(self):
        self.listen_state(cb=self.handle_incoming_call, entity='sensor.fritzbox_callmonitor', old='idle', new='ringing')

    def handle_incoming_call(self, entity, attribute, old, new, *args, **kwargs):
        self.log(args)
        self.log(kwargs)
        title = 'Anruf'
        message = 'Eingehender Anruf'

        # pause fire tv living room
        if self.get_state(entity='media_player.firetv_living_room') == 'playing':
            self.call_service('media_player.media_play_pause', entity_id='media_player.firetv_living_room')
            self.call_service('notify.notify_firetv_living_room', title=title, message=message)
        # pause fire tv bedroom
        if self.get_state(entity='media_player.firetv_bedroom') == 'playing':
            self.call_service('media_player.media_play_pause', entity_id='media_player.firetv_bedroom')
            self.call_service('notify.notify_firetv_bedroom', title=title, message=message)
