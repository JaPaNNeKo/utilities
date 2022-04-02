from yggdrasil.app.app_generic import AppGeneric
from yggdrasil.app.utilities import run_cmds, CmdError, generate_custom_batch
from yggdrasil.logger import logger
import os


class AppLocal(AppGeneric):
    _identifier = 'local'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = kwargs.pop("name")
        self.venv_name = kwargs.pop("venv_name") #TODO Align naming settings vs internal?
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
            run_cmds(cmds=cmds)
        except CmdError as e:
            if not debug:
                logger.error("App {0} could not be created - Rolling back".format(self.name))
                self.remove()
                return
            else:
                raise e

        replacements = [
            ('#name_venv#', self.venv_name),
            ('#entry_points#', self.entry_point),
        ]

        generate_custom_batch(
            source=r'{0}\template_launcher_local.txt'.format(path_templates),
            destination=r'{0}\{1}.bat'.format(path_scripts, self.name),
            replacements=replacements,
        )
        logger.info("App creation for {0}: Completed!".format(self.name))
