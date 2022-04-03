import os
from collections import namedtuple
import subprocess
from yggdrasil.logger import logger
import yaml
import yggdrasil.app as app

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
        # todo List all apps that are fully installed, i.e. have a venv & an external entry point
        # todo Cross reference against settings

    @classmethod
    def from_root(cls, root: str):
        return AppManager(apps=cls._load_configs(r'{0}\settings'.format(root)), root=root)

    @classmethod
    def _load_configs(cls, root):
        apps = []
        with open(r"{0}\settings_yaml.yaml".format(root)) as file:
            try:
                settings = yaml.safe_load(file)
            except yaml.YAMLError as exc:
                print(exc)
        for config in settings['configurations']:
            AppsMatching = [App for App in cls.classes_apps if config['type']==App._identifier]
            # TODO exception management if no type field in yaml
            if len(AppsMatching) == 0:
                raise Exception("Problem: Unrecognised app type")
            if len(AppsMatching) > 1:
                raise Exception("Problem: Several apps match this type")
            AppMatch = AppsMatching[0]
            try:
                apps.append(AppMatch(**config))
            except KeyError as e:
                raise Exception("Settings file misdefined - missing value for xxx") # TODO refine
        return apps

    @classmethod
    def _seed_configs(cls, root):
        with open(r'{0}\data\template_settings.yaml'.format(_PATH_INTERNAL)) as f:
            batch_ls = f.readlines()
        with open(r'{0}\settings\settings.yaml'.format(root), 'w+') as f:
            f.write("".join(batch_ls))

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
        _app.remove(
            path_scripts=self.path_scripts,
            path_venvs=self.path_envs,
            path_templates=self.path_template_scripts,
            **kwargs
        )
        # TODO Error handling if name isn't recorded in logs / settings


if __name__ == "__main__":
    from pprint import pprint
    mger = AppManager.from_root(r"C:\Users\maxim\Documents\Yggdrasil")
    # mger.create("tool_local", debug=True)
    # mger.create("tool_git", debug=True)


    mger.remove("tool_local", debug=True)
    mger.remove("tool_git", debug=True)


    # local based tests
    # mger.create("tool_local", debug=True)
    # mger.remove("tool_local", debug=True)

    # git based tests
    # mger.create("tool_git", debug=True)
    # mger.remove("tool_git", debug=True)
    import pdb; pdb.set_trace()

# todo add list apps function