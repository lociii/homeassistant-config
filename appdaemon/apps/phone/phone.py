import appdaemon.plugins.hass.hassapi as hass


class NotifyCall(hass.Hass):
    def initialize(self):
        self.listen_state(cb=self.handle_incoming_call, entity='sensor.fritzbox_callmonitor', old='idle', new='ringing')

    def handle_incoming_call(self, entity, attribute, old, new, *args, **kwargs):
        title = 'Anruf'
        message = 'Eingehender Anruf'

        # try to get caller data
        state = self.get_state(entity='sensor.fritzbox_callmonitor', attribute='all')
        if 'attributes' in state:
            if 'from_name' in state['attributes'] and 'from' in state['attributes']:
                message = 'Eingehender Anruf von {name} ({number})'.format(
                    name=state['attributes']['from_name'],
                    number=state['attributes']['from'])
            elif 'from' in state['attributes']:
                message = 'Eingehender Anruf von {number}'.format(
                    number=state['attributes']['from'])

        # pause fire tv living room
        self.call_service('notify/notify_firetv_living_room', title=title, message=message)
        # TODO: reactivate as soon as paused firetv is not reported as playing anymore
        # if self.get_state(entity='media_player.firetv_living_room') == 'playing':
        #     self.call_service('media_player/media_pause', entity_id='media_player.firetv_living_room')
        # pause fire tv bedroom
        self.call_service('notify/notify_firetv_bedroom', title=title, message=message)
        # TODO: reactivate as soon as paused firetv is not reported as playing anymore
        # if self.get_state(entity='media_player.firetv_bedroom') == 'playing':
        #     self.call_service('media_player/media_pause', entity_id='media_player.firetv_bedroom')
