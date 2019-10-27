import appdaemon.plugins.hass.hassapi as hass
import time


class ActionVacuum(hass.Hass):
    def initialize(self):
        self.listener_done = None

        self.entity = self.args['entity']
        self.trigger = self.args['trigger']
        self.target = self.args['target']

        self.listen_state(callback=self.activate, entity=self.trigger, new='on', old='off')
        self.listen_state(callback=self.deactivate, entity=self.trigger, new='off', old='on')

    def activate(self, *args, **kwargs):
        # check for cleaning finished
        self.listener_done = self.listen_state(callback=self.cleaning_done, entity=self.entity, new='docked')

        # start cleaning
        self.call_service('vacuum/start', entity_id=self.entity)

        self.log('cleaning cycle started')

    def deactivate(self, *args, **kwargs):
        # cancel finish timer
        if self.listener_done is not None:
            self.cancel_listen_event(self.listener_done)
            self.listener_done = None

        # cycle not yet finished, go to dock and wait for next call
        if self.get_state(self.target) == 'off':
            self.call_service('vacuum/pause', entity_id=self.entity)
            time.sleep(1)
            self.call_service('vacuum/return_to_base', entity_id=self.entity)

            self.log('cleaning cycle paused')

    def cleaning_done(self, *args, **kwargs):
        # mark cycle done
        self.turn_on(self.target)
        # turn off active indicator
        self.turn_off(self.trigger)

        self.log('cleaning cycle done')