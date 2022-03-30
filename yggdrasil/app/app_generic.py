import os
from collections import namedtuple


# TODO Write __repr__ & __str__ for all classes

class AppGeneric(object):
    _replacements = [
        ('#name_venv#', 'env'),
        ('#entry_point#', 'entry_point'),
    ]

    def __init__(self, name: str, **kwargs):
        self.name = name
        # TODO remove / replace?
        self.functions = {
            'remove': self.remove,
            'create': self.create,
        }
        # TODO Parametrise
        self.is_installed = 'NOOO'

    def create(self, **kwargs):
        raise Exception("Function should be overriden by subclass")

    def remove(self, **kwargs):
        """
        Deletes an application
        :param name: Name of the application
        """
        # logger.info("App deletion for {0}: Starting...".format(self.name))
        # nb_venv_uses = len([elt for elt in self.app if self.app[elt].env == self.app[self.name].env])
        # if nb_venv_uses == 1:
        #     _run_cmds(['rmvirtualenv {0}'.format(self.app[self.name].env)])
        # if os.path.exists(r"{0}\scripts\{1}.bat".format(self.root,self.name)):
        #     os.remove(r"{0}\scripts\{1}.bat".format(self.root,self.name))
        # logger.info("App creation for {0}: Completed!".format(self.name))

    @classmethod
    def seed_settings(cls, root):
        raise Exception ("Should be implemented by each ")

    @classmethod
    def load_settings(self, root) -> []:
        raise Exception ("Should be implemented by each ")

