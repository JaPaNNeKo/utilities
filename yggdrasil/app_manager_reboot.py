import os
from collections import namedtuple
import subprocess
from yggdrasil.logger import logger
import yggdrasil.app as app
from yggdrasil.app.utilities import _parse_settings

PATH_YGGDRASIL = os.environ.get("YGGDRASIL_ROOT", os.path.expanduser('~\Documents'))
_PATH_INTERNAL = os.path.join(os.path.dirname(__file__))


class AppManager(object):
    classes_apps = app.AppGeneric.__subclasses__()

    def __init__(self, apps: [], root: str):
        self.path_root = root
        self.path_settings = r'{0}\settings'.format(self.path_root)
        self.path_template_scripts = r'{0}\data'.format(_PATH_INTERNAL)
        self.path_scripts = r'{0}\scripts'.format(self.path_root)
        self.path_envs = r'{0}\venvs'.format(self.path_root)

        self.apps = apps
        # TODO Crash if multiple app with same name
        # TODO Add log functionality (logging which app are installed etc...) + crash if log non resolvable

    def _get_status(self):
        pass
        # List all apps that are fully installed, i.e. have a venv & an external entry point
        # Cross reference against settings

    @classmethod
    def from_root(cls, root: str):
        return AppManager(apps=cls._load_configs(r'{0}\settings'.format(root)), root=root)

    @classmethod
    def _load_configs(cls, root):
        #TODO Not a fan of concatenating settings path at different levels
        apps = []
        for App in cls.classes_apps:
            settings = _parse_settings('{0}\{1}'.format(root, App.name_settings_file))
            for config in settings:
                name_app = config.pop('name')
                apps.append(App(name_app, **config))
        return apps

    @classmethod
    def _seed_configs(cls, root):
        for type_app, App in cls.classes_apps:
            with open(r'{0}\settings\{1}'.format(root, App.name_settings_file), 'w+') as f:
                f.write('\t'.join(App.parameters))

    def _find_app(self, name):
        apps_match = [app for app in self.apps if app.name == name]
        if len(apps_match) == 0:
            raise Exception("App not found - Please check app name called")
        if len(apps_match) > 1:
            raise Exception("Several apps with this name - Please update base configuration")
        return apps_match[0]

    def create(self, app: str, **kwargs):
        _app = self._find_app(app)
        venv_match = [app for app in self.apps if app.venv_name == _app.venv_name and app.is_installed]
        _app.create(
            path_scripts=self.path_scripts,
            path_venvs=self.path_envs,
            path_templates=self.path_template_scripts,
            create_venv=len(venv_match) == 0, #TODO carry impact into functions
            **kwargs
        )
        # TODO Error handling if name isn't recorded in logs / settings

    def remove(self, app: str, **kwargs):
        _app = self._find_app(app)
        venv_match = [app for app in self.apps if app.venv_name == _app.venv_name and app.is_installed]
        _app.remove(
            path_scripts=self.path_scripts,
            path_venvs=self.path_envs,
            path_templates=self.path_template_scripts,
            delete_venv=len(venv_match) == 1,
            **kwargs
        )
        # TODO Error handling if name isn't recorded in logs / settings


if __name__ == "__main__":
    mger = AppManager.from_root(r"C:\Users\maxim\Documents\Yggdrasil")
    mger.create("tool_flat", debug=True)
    import pdb; pdb.set_trace()