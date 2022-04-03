from yggdrasil.app.app_generic import AppGeneric
from yggdrasil.app.utilities import run_cmds, CmdException, generate_custom_batch
from yggdrasil.logger import logger
import os
import shutil


class AppLocal(AppGeneric):
    identifier = 'local'
    atts_required = None
    atts_optional = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = kwargs.pop("name")
        self.venv_name = r'venv_{0}'.format(self.name)
        self.directory = kwargs.pop("directory")
        self.entry_points = kwargs.pop("entry_points")
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
            self.remove(path_scripts, path_venvs, path_templates)
        # Generate virtual environment
        cmds = []
        if not self.is_installed:
            path_venv = r'{0}\{1}'.format(path_venvs, self.venv_name)
            if self.version_py == '':
                cmds.append(r'py -m venv {0}'.format(path_venv))
            else:
                cmds.append(r'py -{0} -m venv {1}'.format(self.version_py, path_venv))
            cmds.append(
                r'{0}\Scripts\activate && pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r "{1}\requirements.txt" && deactivate'
                .format(path_venv,self.directory))
        try:
            run_cmds(cmds=cmds)
        except CmdException as e:
            if not debug:
                logger.error("App {0} could not be created - Rolling back".format(self.name))
                self.remove(path_scripts, path_venvs, path_templates)
                return
            else:
                raise e

        map_replac_eps = [[
                ('#path_venv#', path_venv),
                ('#directory#', self.directory),
                ('#entry_point#', ep['script']),
            ] for ep in self.entry_points]

        for k, replacement in enumerate(map_replac_eps):
            generate_custom_batch(
                source=r'{0}\template_launcher_local.txt'.format(path_templates),
                destination=r'{0}\{1}.bat'.format(path_scripts, self.entry_points[k]['name']),
                replacements=replacement,
            )
        logger.info("App creation for {0}: Completed!".format(self.name))

    def remove(self, path_scripts:str, path_venvs: str, path_templates: str, **kwargs):
        """
        Deletes an application
        :param name: Name of the application
        """
        logger.info("App deletion for {0}: Starting...".format(self.name))
        path_venv = r'{0}\{1}'.format(path_venvs, self.venv_name)
        # todo check not a common folder
        if not os.path.exists(r'{0}\pyvenv.cfg'.format(path_venv)) or not os.path.exists(r'{0}\Scripts\activate'.format(path_venv)):
            raise Exception("Error - The folder about to be deleted is not a virtual environment")
        else:
            shutil.rmtree(path_venv)


        for ep in self.entry_points:
            if os.path.exists(r"{0}\{1}.bat".format(path_scripts, ep['name'])):
                os.remove(r"{0}\{1}.bat".format(path_scripts, ep['name']))

        logger.info("App creation for {0}: Completed!".format(self.name))
        self.is_installed = False
