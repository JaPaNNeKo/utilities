import os
from collections import namedtuple
from yggdrasil.app.utilities import logger, _run_cmds

# TODO Write __repr__ & __str__ for all classes
# TODO unmix between app 'name' (i.e. how it's called in settings file) and its 'name i.e. entry points' (how it's called once installed from cmd)


class AppGeneric(object):
    # _replacements = [
    #     ('#name_venv#', 'env'),
    #     ('#entry_point#', 'entry_point'),
    # ]

    name_settings_file = None
    parameters = None

    def __init__(self, name: str, **kwargs):
        self.name = name
        self.names_callable = None # To refine, list?
        self.venv_name = kwargs.pop('venv_name')
        self.is_installed = kwargs.pop('is_installed')

        # TODO remove / replace?
        self.functions = {
            'remove': self.remove,
            'create': self.create,
        }
        # TODO Parametrise
        self.is_installed = 'NOOO'

    def create(self, path_scripts: str, path_venvs: str, path_templates: str, **kwargs):
        raise Exception("Function should be overriden by subclass")

    def remove(self, path_scripts:str, path_venvs: str, path_templates: str, delete_venv: bool, **kwargs):
        """
        Deletes an application
        :param name: Name of the application
        """
        logger.info("App deletion for {0}: Starting...".format(self.name))
        if delete_venv:
            _run_cmds(['rmvirtualenv {0}'.format(self.venv_name)])
        if os.path.exists(r"{0}\{1}.bat".format(path_scripts, self.name)):
            os.remove(r"{0}\{1}.bat".format(path_scripts, self.name))

        logger.info("App creation for {0}: Completed!".format(self.name))
        self.is_installed = False

    @classmethod
    def seed_settings(cls, root):
        raise Exception ("Should be implemented by each ")

    @classmethod
    def load_settings(self, root) -> []:
        raise Exception ("Should be implemented by each ")

    def check(self):
        pass