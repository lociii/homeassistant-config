import appdaemon.plugins.hass.hassapi as hass


class AppDaemon(hass.Hass):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register_constraint('check_constraint_list')

    def check_constraint_list(self, *args, **kwargs):
        constraints = self.args.get('constraint_list', None)

        if constraints is None:
            return True

        for constraint in constraints:
            entity, value = constraint.split(',')
            if self.get_state(entity) != value:
                return False

        return True
