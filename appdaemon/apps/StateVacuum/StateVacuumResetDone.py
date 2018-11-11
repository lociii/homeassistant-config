import appdaemon.plugins.hass.hassapi as hass
import datetime


class StateVacuumResetDone(hass.Hass):
    def initialize(self):
        self.timer = None
        self.target = self.args['target']

        self.run_daily(callback=self.deactivate, start=datetime.time(23, 59, 59))

    def deactivate(self, *args, **kwargs):
        self.turn_off(self.target)
