import os
from collections import namedtuple
from yggdrasil.app.utilities import logger, run_cmds
from typing import overload
from abc import ABC, abstractmethod, abstractclassmethod

# TODO Write __repr__ & __str__ for all classes
# TODO Enforce some class attributes to be implemented in subclasses


class AppGeneric(object):
    identifier = None
    name_settings_file = None
    parameters = None

    def __init__(self, *args, **kwargs):
        # TODO Parametrise
        self.is_installed = False

    @classmethod
    def set_class_constants(cls, *args, **kwargs):
        pass

    def create(self, path_scripts: str, path_venvs: str, path_templates: str, **kwargs):
        raise Exception("Function should be overriden by subclass")

    def remove(self, *args, **kwargs):
        raise Exception("Function should be overriden by subclass")

    @classmethod
    def seed_settings(cls, root):
        raise Exception("Should be implemented by each ")

    @classmethod
    def load_settings(self, root) -> []:
        raise Exception("Should be implemented by each ")

    def check(self):
        pass


class Apps(object):
    def __init__(self):
        self.classes_apps = AppGeneric.__subclasses__()

    def select(self, **kwargs):
        for class_app in self.classes_apps:
            condition_out = True
            for att, val in kwargs.items():
                if getattr(class_app, att) != val:
                    condition_out = False
            if condition_out: return class_app
