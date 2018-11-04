import appdaemon.plugins.hass.hassapi as hass


class HandleActionComingHome(hass.Hass):
    def initialize(self):
        self.entities = self.args['entities']
        self.delayer = self.get_app('util_delayer')
        self.announce = self.get_app('announce')

        # indicators
        self.indicator_darkness = self.args['indicator_darkness']
        self.indicator_sleeping = self.args['indicator_sleeping']
        self.indicator_presence = self.args['indicator_presence']

        # execute when coming home
        self.listen_state(self.update_status, self.indicator_presence, new='True', old='False')

    def update_status(self, *args, **kwargs):
        self.announce.speak(message='Willkommen zurück!')

        is_dark = False
        if self.indicator_darkness:
            is_dark = self.get_state(entity=self.indicator_darkness) == 'on'

        is_sleeping = False
        if self.indicator_sleeping:
            is_sleeping = self.get_state(entity=self.indicator_sleeping) == 'True'

        self.log('comingHome updated: dark {}, sleeping {}'.format(
            is_dark, is_sleeping))

        # --------------------------------------
        # settings
        # --------------------------------------

        if not is_sleeping and is_dark:
            for entity in self.entities:
                self.delayer.add(hass_func='turn_on', entity_id=entity)
            return
