from yggdrasil.app.app_generic import AppGeneric
from yggdrasil.app.utilities import run_cmds, CmdError, generate_custom_batch
from yggdrasil.logger import logger
import os
import yaml
import yggdrasil.informer.main as informer

class AppWeb(AppGeneric):
    _identifier = 'web'

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = kwargs.pop("name")
        self.venv_name = 'venv_{0}'.format(self.name)
        self.url = kwargs.pop("url")
        self.version_py = kwargs.pop('py_version')
        self.repo_name = self.url.split("/")[-1].split(".")[0] # TODO a bit ugly

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
            cmds.append(r'{0}\Scripts\activate && pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org {1}'.format(path_venv, self.url))
            # TODO parametrise ygg-helpers url
            # TODO remove @improvements
            cmds.append(r'{0}\Scripts\activate && pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org {1}'
                        .format(path_venv,'git+https://github.com/mx-personal/yggdrasil.git@improvements'))
            run_cmds(cmds)
            cmds = []
            cmds.append(r"{0}\Scripts\activate && gen_dist_info {1}".format(path_venv, self.repo_name))
            cmds.append(r"{0}\Scripts\activate && gen_dist_info {1}".format(path_venv, "ygg-helpers"))
            run_cmds(cmds)

            # TODO will leave some trash, clean up dependencies too
            # TODO keep if debug mode, delete otherwise
            info_repo = informer.DistInfo.from_yaml(r'{0}\ygginfo-{1}.yaml'.format(path_venv, self.repo_name))
            info_ygg_help = informer.DistInfo.from_yaml(r'{0}\ygginfo-ygg-helpers.yaml'.format(path_venv))

            cmds = [r"{0}\Scripts\activate && pip uninstall ygg-helpers"]
            run_cmds(cmds)

            # TODO Parametrise bypassing SSL security
            cmds = [r"{0}\Scripts\activate && pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org  -r {1}".format(path_venv, req.path) for req in info_repo.requirements]
            run_cmds(cmds)

        # TODO Reinclude debugging & cmd error management differently

        # Generate batch launcher
        map_replac_eps = [[
            ("#path_venvs#", path_venv),
            ("#name_venv#", self.venv_name),
            ("#entry_point#", ep.path),
        ] for ep in info_repo.entry_points]

        for map in map_replac_eps:
            generate_custom_batch(
                source=r'{0}\template_launcher_web.txt'.format(path_templates),
                destination=r'{0}\{1}.bat'.format(path_scripts, self.name),
                replacements=map,
            )

        logger.info("App creation for {0}: Completed!".format(self.name))

