from globals import AppDaemon


class ActionCover(AppDaemon):
    def initialize(self):
        self.delayer = self.get_app('util_delayer')

        self.trigger_entity = self.args['trigger_entity']
        self.trigger_status = self.args['trigger_status']
        self.action_scenes = self.args['action_scenes']

        status_text = 'on' if self.trigger_status else 'off'
        self.listen_state(cb=self.update_status, entity=self.trigger_entity, new=status_text,
                          check_constraint_list=True)

    def update_status(self, *args, **kwargs):
        self.log('{} turned {}'.format(self.trigger_entity, self.trigger_status))

        for scene in self.action_scenes:
            self.delayer.add(hass_func='turn_on', entity_id=scene)
