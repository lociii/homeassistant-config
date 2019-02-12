from globals import AppDaemon


class ActionCover(AppDaemon):
    def initialize(self):
        self.delayer = self.get_app('util_delayer')

        self.trigger_entity = self.args['trigger_entity']
        self.trigger_status = self.args['trigger_status']
        self.action_scenes = self.args.get('action_scenes', [])
        self.action_entities = self.args.get('action_entities', [])
        self.action_status = self.args.get('action_status', False)

        status_text = 'on' if self.trigger_status else 'off'
        self.listen_state(cb=self.update_status, entity=self.trigger_entity, new=status_text,
                          check_constraint_list=True)

    def update_status(self, *args, **kwargs):
        self.log('{} turned {}'.format(self.trigger_entity, self.trigger_status))

        # handle all entity changes
        for entity in self.action_entities:
            if self.action_status:
                self.delayer.add(hass_func='call_service', service='cover/open_cover', entity_id=entity)
            else:
                self.delayer.add(hass_func='call_service', service='cover/close_cover', entity_id=entity)

        # execute all scenes
        for scene in self.action_scenes:
            self.delayer.add(hass_func='turn_on', entity_id=scene)
