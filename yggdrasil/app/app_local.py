from yggdrasil.app.app_generic import AppGeneric
from yggdrasil.app.utilities import _parse_settings, _run_cmds, CmdError

class AppLocal(AppGeneric):
    _name_settings_file = 'settings-local.txt'


    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.venv_name = kwargs.pop("venv_name")
        self.directory = kwargs.pop("directory")
        self.entry_point = kwargs.pop("entry_point")
        self.version_py = kwargs.pop('py_version')

    def create(self):
        pass

    @classmethod
    def seed_settings(cls, root):
        with open(r'{0}\settings\{1}'.format(root, cls._name_settings_file), 'w+') as f:
            f.write('name\tpy_version\tvenv\tdirectory\tentry_point')

    @classmethod
    def load_settings(cls, root) -> []:
        settings = _parse_settings('{0}\{1}'.format(root, cls._name_settings_file))
        return [
            AppLocal(
                name=config['name'],
                py_version=config['py_version'],
                venv_name=config['venv'],
                directory=config['directory'],
                entry_point=config['entry_point'],
            )
            for config in settings
        ]
