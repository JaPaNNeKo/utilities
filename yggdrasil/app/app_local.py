from yggdrasil.app.app_generic import AppGeneric
from yggdrasil.app.utilities import _parse_settings, _run_cmds, CmdError
from yggdrasil.logger import logger
import os

class AppLocal(AppGeneric):
    name_settings_file = 'settings-local.txt'
    _parameters = [
        'name',
        'venv_name',
        'directory',
        'entry_point',
        'py_version'
    ]

    _replacements = [
        ('#name_venv#', 'venv_name'),
        ('#entry_point#', 'entry_point'),
    ]

    def __init__(self, name: str, **kwargs):
        super().__init__(name, **kwargs)
        self.venv_name = kwargs.pop("venv") #TODO Align naming settings vs internal?
        self.directory = kwargs.pop("directory")
        self.entry_point = kwargs.pop("entry_point")
        self.version_py = kwargs.pop('py_version')

    def create(self, path_scripts:str, path_venvs: str, path_templates: str, **kwargs):
        """
        Creates an application.
        :param force_regen: Default is False. If True, app will be entirely removed before being re-created
        :param debug: Default is False. If False, crashing on cmds execution will skip the rest of the creation
        If True, then it will raise a CmdError.
        """
        logger.info("App creation for {0}: Starting...".format(self.name))
        force_regen = kwargs.pop('force_regen', False)
        debug = kwargs.pop('debug', False)
        if super().check() and force_regen:
            self.remove()
        # Generate virtual environment
        cmds = []
        if not os.path.isdir(r'{0}\{1}'.format(path_venvs, self.venv_name)):
            if self.version_py == '':
                cmds.append(r'py -m venv {0}\{1}'.format(path_venvs, self.venv_name))
            else:
                cmds.append(r'py -{0} -m venv {1}\{2}'.format(self.version_py, path_venvs, self.venv_name))
            cmds.append('workon {0} & setprojectdir "{1}"'.format(self.venv_name, self.directory))
            cmds.append(
                r'workon {1} & pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r "{0}\requirements.txt"'
                .format(self.directory, self.venv_name))
        try:
            _run_cmds(cmds=cmds)
        except CmdError as e:
            if not debug:
                logger.error("App {0} could not be created - Rolling back".format(self.name))
                self.remove()
                return
            else:
                raise e

        # Generate batch launcher
        with open(r'{0}\template_launcher_local.txt'.format(path_templates)) as f:
            batch = f.readlines()
        for i, row in enumerate(batch):
            for str_rep, att_name in self.__class__._replacements:
                row = row.replace(str_rep,self.__getattribute__(att_name))
                batch[i] = row
        with open(r'{0}\{1}.bat'.format(path_scripts,self.name),'w+') as f:
            f.write("".join(batch))
        logger.info("App creation for {0}: Completed!".format(self.name))

    @classmethod
    def seed_settings(cls, root):
        with open(r'{0}\settings\{1}'.format(root, cls.name_settings_file), 'w+') as f:
            f.write('name\tpy_version\tvenv\tdirectory\tentry_point')
