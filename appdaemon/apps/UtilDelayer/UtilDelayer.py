import appdaemon.plugins.hass.hassapi as hass


class DelayedItem(object):
    def __init__(self, hass_func, *args, **kwargs):
        self.hass_func = hass_func
        self.args = args
        self.kwargs = kwargs
    
    def execute(self, delayer, simulate):
        delayer.log('executing {} with args {} and kwargs {}'.format(
            self.hass_func, self.args, self.kwargs))

        if simulate:
            return

        hass_func = getattr(delayer, self.hass_func, None)
        if hass_func:
            hass_func(*self.args, **self.kwargs)


class UtilDelayer(hass.Hass):
    stack = list()

    def initialize(self):
        self.simulate_switch = self.args['simulate']
        self.listen_state(self.update_simulation_status, self.simulate_switch)
        self.update_simulation_status()

        self.loop()
    
    def update_simulation_status(self, *args, **kwargs):
        self.simulate = self.get_state(self.simulate_switch) == 'on'
        if self.simulate:
            self.log('SIMULATION MODE ACTIVED, NO ACTIONS WILL BE EXECUTED')
        else:
            self.log('SIMULATION MODE DEACTIVATED, ALL ACTIONS WILL BE EXECUTED')

    @staticmethod
    def add(hass_func, *args, **kwargs):
        UtilDelayer.stack.append(DelayedItem(hass_func=hass_func, *args, **kwargs))

    def loop(self, *args, **kwargs):
        self.run_in(callback=self.loop, delay=1)
        self.execute()

    def execute(self):
        if not self.stack:
            return

        item = self.stack.pop(0)
        item.execute(delayer=self, simulate=self.simulate)
