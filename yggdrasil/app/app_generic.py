import os
from collections import namedtuple
from yggdrasil.app.utilities import logger, run_cmds

# TODO Write __repr__ & __str__ for all classes
# TODO unmix between app 'name' (i.e. how it's called in settings file) and its 'name i.e. entry points' (how it's called once installed from cmd)
# TODO Enforce some class attributes to be implemented in subclasses

class AppGeneric(object):
    _identifier = None
    name_settings_file = None
    parameters = None

    def __init__(self, *args, **kwargs):
        # self.name = kwargs.pop("name")
        # self.names_callable = None # To refine, list?
        # self.venv_name = kwargs.pop('venv_name')
        # self.is_installed = kwargs.pop('is_installed')
        # TODO parametrise
        # self.is_installed = False

        # TODO remove / replace?
        self.functions = {
            'remove': self.remove,
            'create': self.create,
        }
        # TODO Parametrise
        self.is_installed = False

    def create(self, path_scripts: str, path_venvs: str, path_templates: str, **kwargs):
        raise Exception("Function should be overriden by subclass")

    def remove(self, *args, **kwargs):
        raise Exception("Function should be overriden by subclass")

    @classmethod
    def seed_settings(cls, root):
        raise Exception ("Should be implemented by each ")

    @classmethod
    def load_settings(self, root) -> []:
        raise Exception ("Should be implemented by each ")

    def check(self):
        pass
