import os
from collections import namedtuple
import subprocess
from yggdrasil.logger import logger
import yggdrasil.app as app


PATH_YGGDRASIL = os.environ.get("YGGDRASIL_ROOT", os.path.expanduser('~\Documents'))
_PATH_INTERNAL = os.path.join(os.path.dirname(__file__))


class AppManager(object):
    _type_apps = {
        'local': app.AppLocal,
        'web': app.AppWeb,
    }

    def __init__(self, apps: [], root: str):
        self.root = root
        self.apps = apps
        # TODO Crash if multiple app with same name
        # TODO Add log functionality (logging which app are installed etc...) + crash if log non resolvable

    @classmethod
    def from_root(cls, root: str):
        # TODO update
        return AppManager(apps=cls._get_apps(root), root=root)

    @classmethod
    def _get_apps(cls, root):
        #TODO Not a fan of concatenating settings path at different levels
        apps = []
        for type_app, App in cls._type_apps.items():
            apps.extend(App.extract_settings('{0}\settings'.format(root)))
        return apps

    def create(self, app: str):
        pass
        # TODO Error handling if name isn't recorded in logs / settings
        # Find app in self.app
        # Call app.create()

    def remove(self, app: str):
        pass
        # TODO Error handling if name isn't recorded in logs / settings
        # Find app in self.app
        # Call app.remove()