import appdaemon.plugins.hass.hassapi as hass

class HandleReadinglight(hass.Hass):
    """
    a digitalstrom hardware button will be used to turn the readinglight on and off.
    since digitalstrom doesn't integrate with mqtt, we have to listen to an empty
    digitalstrom scene when pushing the button and turn the reading light on and off.
    """
    def initialize(self):
        self.listen_state(self.ds_readinglight_on, 'light.wohnzimmer__leselampe', new='on', old='off')
        self.listen_state(self.ds_readinglight_off, 'light.wohnzimmer__leselampe', new='off', old='on')

    def ds_readinglight_on(self, entity, attribute, old, new, kwargs):
        self.turn_on('switch.osram_plug_readinglight')

    def ds_readinglight_off(self, entity, attribute, old, new, kwargs):
        self.turn_off('switch.osram_plug_readinglight')
