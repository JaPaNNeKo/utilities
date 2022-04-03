from yggdrasil.app.app_generic import AppGeneric
from yggdrasil.app.utilities import run_cmds, generate_custom_batch
from yggdrasil.logger import logger
import os
from ygg_helpers.main import DistInfo
import shutil

_url_helpers = None

class AppWeb(AppGeneric):
    identifier = 'web'

    @classmethod
    def set_class_constants(cls, *args, **kwargs):
        global _url_helpers
        _url_helpers = kwargs.pop("url_helpers")

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = kwargs.pop("name")
        self.venv_name = 'venv_{0}'.format(self.name)
        self.url_project = kwargs.pop("url")
        self.version_py = kwargs.pop('py_version')
        self.repo_name = self.url_project.split("/")[-1].split(".")[0]

    # TODO Break down in more modular methods?
    def create(self, path_scripts: str, path_venvs: str, path_templates: str, **kwargs):
        path_venv = r'{0}\{1}'.format(path_venvs, self.venv_name)
        # TODO check if any necessary content will be missing (e.g. entry points, etc...)
        logger.info("App creation for {0}: Starting...".format(self.name))
        force_regen = kwargs.pop('force_regen', False)
        debug = kwargs.pop('debug', False)
        if super().check() and force_regen:
            self.remove()
        # Generate virtual environment
        cmds = []
        if not os.path.isdir(path_venv):
            if self.version_py == '':
                cmds.append(r'py -m venv {0}'.format(path_venv))
            else:
                cmds.append(r'py -{0} -m venv {1}'.format(self.version_py, path_venv))
            cmds.append(r'{0}\Scripts\activate && pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org {1} && deactivate'.format(path_venv, self.url_project))
            # TODO parametrise ygg-helpers url
            # TODO remove @improvements
            cmds.append(r'{0}\Scripts\activate && pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org {1} && deactivate'
                        .format(path_venv, _url_helpers))

            # TODO README req for github tools - no dash, no space on repo name (or make ygg replace - with _ for dist info finding?) - Not sure that's actually a problem, to test out
            cmds.append(r"{0}\Scripts\activate && gen_dist_info {1} {0}\ygginfo-{1}.yaml && deactivate".format(path_venv, self.repo_name))
            cmds.append(r"{0}\Scripts\activate && gen_dist_info {1} {0}\ygginfo-{1}.yaml && deactivate".format(path_venv, "dist_meta"))

            run_cmds(cmds)
            cmds = []
            run_cmds(cmds)

            # TODO will leave some trash, clean up dependencies too
            # TODO keep if debug mode, delete otherwise
            info_repo = DistInfo.from_yaml(r'{0}\ygginfo-{1}.yaml'.format(path_venv, self.repo_name))
            info_ygg_help = DistInfo.from_yaml(r'{0}\ygginfo-dist_meta.yaml'.format(path_venv))

            cmds = [r"{0}\Scripts\activate && pip uninstall -y ygg_helpers".format(path_venv)]
            run_cmds(cmds)

            # TODO Parametrise bypassing SSL security
            cmds = [r"{0}\Scripts\activate && pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org  -r {1}".format(path_venv, req.path) for req in info_repo.requirements]
            # import pdb;pdb.set_trace()
            run_cmds(cmds)

        # TODO Reinclude debugging & cmd error management differently

        # Generate batch launcher
        map_replac_eps = [[
            ("#path_venv#", path_venv),
            ("#entry_point#", ep.path),
        ] for ep in info_repo.entry_points]

        for k, map in enumerate(map_replac_eps):
            generate_custom_batch(
                source=r'{0}\template_launcher_web.txt'.format(path_templates),
                destination=r'{0}\{1}.bat'.format(path_scripts, info_repo.entry_points[k].name),
                replacements=map,
            )

        logger.info("App creation for {0}: Completed!".format(self.name))

    def remove(self, path_scripts:str, path_venvs: str, **kwargs):
        """
        Deletes an application
        :param name: Name of the application
        """
        logger.info("App deletion for {0}: Starting...".format(self.name))
        path_venv = r'{0}\{1}'.format(path_venvs, self.venv_name)
        info_repo = DistInfo.from_yaml(r'{0}\ygginfo-{1}.yaml'.format(path_venv, self.repo_name))
        for ep in info_repo.entry_points:
            os.remove('{0}\{1}.bat'.format(path_scripts,ep.name))

        # todo check not a common folder
        if not os.path.exists(r'{0}\pyvenv.cfg'.format(path_venv)) or not os.path.exists(r'{0}\Scripts\activate'.format(path_venv)):
            raise Exception("Error - The folder about to be deleted is not a virtual environment")
        else:
            shutil.rmtree(path_venv)

        logger.info("App creation for {0}: Completed!".format(self.name))
        self.is_installed = False