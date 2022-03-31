from yggdrasil.app.app_generic import AppGeneric
from yggdrasil.app.utilities import _parse_settings, _run_cmds, CmdError


class AppWeb(AppGeneric):
    name_settings_file = 'settings-web.txt'
    _replacements = [
        ('#name_venv#', 'env'),
        ('#entry_point#', 'entry_point'),
    ]

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.url = kwargs.pop("url")
        self.version_py = kwargs.pop('py_version')

    def create(self):
        # TODO check if any necessary content will be missing (e.g. entry points, etc...)
        pass

    @classmethod
    def seed_settings(cls, root):
        with open(r'{0}\settings\{1}'.format(root, cls._name_settings_file), 'w+') as f:
            f.write('name\tpy_version\turl')

    # @classmethod
    # def load_settings(cls, root) -> []:
    #     settings = _parse_settings('{0}\{1}'.format(root, cls._name_settings_file))
    #     return [
    #         AppWeb(
    #             name=config['name'],
    #             py_version=config['py_version'],
    #             url=config['url'],
    #         )
    #         for config in settings
    #     ]
