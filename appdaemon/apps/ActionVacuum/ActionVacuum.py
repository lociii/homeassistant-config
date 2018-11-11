import appdaemon.plugins.hass.hassapi as hass
import time


class ActionVacuum(hass.Hass):
    def initialize(self):
        self.listener_done = None

        self.entity = self.args['entity']
        self.trigger = self.args['trigger']
        self.target = self.args['target']

        self.listen_state(cb=self.activate, entity=self.trigger, new='on', old='off')
        self.listen_state(cb=self.deactivate, entity=self.trigger, new='off', old='on')

    def activate(self, *args, **kwargs):
        self.log('cleaning cycle starting')

        # check for cleaning finished
        self.listener_done = self.listen_state(cb=self.cleaning_done, entity=self.entity, new='docked')

        # start cleaning
        self.call_service('vacuum/start', entity_id=self.entity)

    def deactivate(self, *args, **kwargs):
        # cancel finish timer
        if self.listener_done is not None:
            self.cancel_listen_event(self.listener_done)
            self.listener_done = None

        if self.get_state(self.target) == 'off':
            self.log('cleaning cycle paused')

            # pause and return to dock, waiting to get started again
            self.call_service('vacuum/pause', entity_id=self.entity)
            time.sleep(1)
            self.call_service('vacuum/return_to_base', entity_id=self.entity)

    def cleaning_done(self, *args, **kwargs):
        self.log('cleaning cycle done')

        # mark cycle done
        self.turn_on(self.target)
        # turn off active indicator
        self.turn_off(self.trigger)
