import appdaemon.plugins.hass.hassapi as hass
import time


class HandleActionLight(hass.Hass):
    def initialize(self):
        self.light_entity = self.args['light_entity']
        self.delayer = self.get_app('util_delayer')

        # indicators
        self.indicator_darkness = self.args['indicator_darkness']
        self.indicator_sleeping = self.args['indicator_sleeping']
        self.indicator_presence = self.args['indicator_presence']
        
        # actions
        self.status_present = self.args['status_present']
        self.status_absent = self.args['status_absent']
        self.status_sleeping = self.args['status_sleeping']
        self.flash_when_leaving = self.args['flash_when_leaving']

        # add status listeners for each indicator
        if self.indicator_darkness:
            self.listen_state(cb=self.update_status, entity=self.indicator_darkness)
        if self.indicator_sleeping:
            self.listen_state(cb=self.update_status, entity=self.indicator_sleeping)
        if self.indicator_presence:
            self.listen_state(cb=self.update_status, entity=self.indicator_presence)
            self.listen_state(cb=self.flash, entity=self.indicator_presence, old='True', new='False')

    def flash(self, *args, **kwargs):
        if not self.flash_when_leaving:
            return

        self.turn_on(self.light_entity)
        time.sleep(1)
        self.turn_off(self.light_entity)
        time.sleep(1)
        self.turn_on(self.light_entity)
        time.sleep(1)
        self.turn_off(self.light_entity)
        time.sleep(1)

    def update_status(self, *args, **kwargs):
        is_dark = False
        if self.indicator_darkness:
            is_dark = self.get_state(entity=self.indicator_darkness) == 'on'

        is_sleeping = False
        if self.indicator_sleeping:
            is_sleeping = self.get_state(entity=self.indicator_sleeping) == 'True'

        is_present = False
        if self.indicator_presence:
            is_present = self.get_state(entity=self.indicator_presence) == 'True'

        self.log('light {} updated: dark {}, sleeping {}, present {}'.format(
            self.light_entity, is_dark, is_sleeping, is_present))

        # --------------------------------------
        # settings
        # --------------------------------------

        # sleeping
        if is_sleeping:
            self.handle_action(status=self.status_sleeping)
            return

        # night, awake, present
        if is_dark and not is_sleeping and is_present:
            self.handle_action(status=self.status_present)
            return

        # night, awake, absent
        if is_dark and not is_sleeping and not is_present:
            self.handle_action(status=self.status_absent)
            return

    def handle_action(self, status):
        if status is None:
            return
        if status:
            self.delayer.add(hass_func='turn_on', entity_id=self.light_entity)
        else:
            self.delayer.add(hass_func='turn_off', entity_id=self.light_entity)
