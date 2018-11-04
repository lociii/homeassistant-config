import appdaemon.plugins.hass.hassapi as hass
import datetime


class HandleActionCover(hass.Hass):
    def __init__(self, *args, **kwargs):
        self.listener_sunprotection = None
        super().__init__(*args, **kwargs)

    def initialize(self):
        self.cover_entity = self.args['cover_entity']
        self.delayer = self.get_app('util_delayer')

        # indicators
        self.indicator_darkness = self.args['indicator_darkness']
        self.indicator_open = self.args['indicator_open']
        self.indicator_sleeping = self.args['indicator_sleeping']
        self.indicator_presence = self.args['indicator_presence']
        self.indicator_sunprotection = self.args['indicator_sunprotection']
        self.begin_sunprotection = self.args['begin_sunprotection']
        self.shutdown = self.args['shutdown']

        # actions
        self.cover_scene_open = self.args['cover_scene_open']
        self.cover_scene_close = self.args['cover_scene_close']
        self.cover_scene_ajar = self.args['cover_scene_ajar']
        self.cover_scene_catmode = self.args['cover_scene_catmode']
        self.cover_scene_sunprotection = self.args['cover_scene_sunprotection']
        self.cover_scene_night_present = self.args['cover_scene_night_present']
        self.cover_scene_night_absent = self.args['cover_scene_night_absent']

        # add status listeners for each indicator
        if self.indicator_darkness:
            self.listen_state(cb=self.update_status, entity=self.indicator_darkness)
        if self.indicator_open:
            self.listen_state(cb=self.update_status, entity=self.indicator_open)
        if self.indicator_sleeping:
            self.listen_state(cb=self.update_status, entity=self.indicator_sleeping)
        if self.indicator_presence:
            self.listen_state(cb=self.update_status, entity=self.indicator_presence)

        # sunprotection indicator is special since it's not directly triggering the update
        # but sets another timer
        if self.indicator_sunprotection:
            self.set_sunprotection_listener()
            self.listen_state(cb=self.set_sunprotection_listener, entity=self.indicator_sunprotection)
            self.listen_state(cb=self.set_sunprotection_listener, entity=self.begin_sunprotection)

    def set_sunprotection_listener(self, *args, **kwargs):
        # cancel existing timer
        if self.listener_sunprotection:
            self.cancel_timer(self.listener_sunprotection)

        # sunprotection mode is off
        if self.get_state(entity=self.indicator_sunprotection) != 'True':
            return
        
        # add timer
        begin_sunprotection = self.parse_time(self.get_state(self.begin_sunprotection))
        self.listener_sunprotection = self.run_daily(callback=self.update_status, start=begin_sunprotection)

    def update_status(self, *args, **kwargs):
        is_dark = False
        if self.indicator_darkness:
            is_dark = self.get_state(entity=self.indicator_darkness) == 'on'

        is_open = False
        if self.indicator_open:
            is_open = self.get_state(entity=self.indicator_open) == 'on'

        is_sleeping = False
        if self.indicator_sleeping:
            is_sleeping = self.get_state(entity=self.indicator_sleeping) == 'True'

        is_present = False
        if self.indicator_presence:
            is_present = self.get_state(entity=self.indicator_presence) == 'True'

        is_sunprotection = False
        if self.indicator_sunprotection and self.get_state(self.indicator_sunprotection) == 'True':
            is_sunprotection = self.now_is_between(self.get_state(self.begin_sunprotection), "23:59:59")

        self.log('cover {} updated: dark {}, open {}, sleeping {}, present {}, sunprotection {}'.format(
            self.cover_entity, is_dark, is_open, is_sleeping, is_present, is_sunprotection))

        # --------------------------------------
        # security settings
        # --------------------------------------

        # window open, away => close cover for security reasons
        if is_open and not is_present:
            self.log('window open, away')
            self.close()
            return

        # --------------------------------------
        # night modes
        # --------------------------------------

        # night, window open, at home => keep ajar for ventilation
        if is_dark and is_open and is_present:
            self.log('night, window open, at home')
            self.ajar()
            return

        # night, window closed, sleeping
        if is_dark and not is_open and is_sleeping:
            self.log('night, window closed, sleeping')
            self.close()
            return

        # night, window closed, awake, at home
        if is_dark and not is_open and not is_sleeping and is_present:
            self.log('night, window closed, awake, at home')
            self.night_present()
            return

        # night, window closed, awake, away
        if is_dark and not is_open and not is_sleeping and not is_present:
            # catmode before shutdown
            shutdown = self.parse_time(self.get_state(self.shutdown))
            if self.time() < shutdown:
                self.log('night, window closed, awake, away => before shutdown')
                self.catmode()
                self.run_once(self.night_absent, shutdown)
            else:
                self.log('night, window closed, awake, away => after shutdown')
                self.night_absent()
            return

        # --------------------------------------
        # day modes
        # --------------------------------------

        # day, sleeping => keep the light out
        if not is_dark and is_sleeping:
            self.log('day, sleeping')
            self.close()
            return

        # day, window open, awake, at home => let the air in
        if not is_dark and is_open and not is_sleeping and is_present:
            self.log('day, window open, awake, at home')
            self.open()
            return

        # day, window closed, awake => let the light in, except during sunprotection
        if not is_dark and not is_open and not is_sleeping:
            if is_sunprotection:
                self.log('day, window closed, awake => with sunprotection')
                self.sunprotection()
            else:
                self.log('day, window closed, awake => without sunprotection')
                self.open()
            return

    def open(self, *args, **kwargs):
        self.log('cover {} open'.format(self.cover_entity))
        self.delayer.add(hass_func='turn_on', entity_id=self.cover_scene_open)

    def close(self, *args, **kwargs):
        self.log('cover {} close'.format(self.cover_entity))
        self.delayer.add(hass_func='turn_on', entity_id=self.cover_scene_close)

    def ajar(self, *args, **kwargs):
        self.log('cover {} ajar'.format(self.cover_entity))
        self.delayer.add(hass_func='turn_on', entity_id=self.cover_scene_ajar)

    def catmode(self, *args, **kwargs):
        self.log('cover {} catmode'.format(self.cover_entity))
        self.delayer.add(hass_func='turn_on', entity_id=self.cover_scene_catmode)

    def sunprotection(self, *args, **kwargs):
        self.log('cover {} sunprotection'.format(self.cover_entity))
        self.delayer.add(hass_func='turn_on', entity_id=self.cover_scene_sunprotection)

    def night_present(self, *args, **kwargs):
        self.log('cover {} night present'.format(self.cover_entity))
        self.delayer.add(hass_func='turn_on', entity_id=self.cover_scene_night_present)

    def night_absent(self, *args, **kwargs):
        self.log('cover {} night absent'.format(self.cover_entity))
        self.delayer.add(hass_func='turn_on', entity_id=self.cover_scene_night_absent)
