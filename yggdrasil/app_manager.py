import os

PATH_YGGDRASIL = os.environ.get("YGGDRASIL_ROOT", os.path.expanduser('~\Documents'))
_PATH_INTERNAL = os.path.join(os.path.dirname(__file__))


class App(object):
    def __init__(self, name: str, path_project: str, version_py: str, entry_point: str, env: str):
        self.name = name
        self.env = env
        self.path_project = path_project
        self.version_py = version_py
        self.entry_point = entry_point


class AppManager(object):
    _replacements = [
        ('#name_venv#', 'env'),
        ('#entry_point#', 'entry_point'),
    ]

    def __init__(self, apps: [], root: str):
        self.root = root
        self.apps = apps
        self.functions = {
            'remove': self.rm_app,
            'make': self.mk_app,
            'update': self.up_app,
        }

    @classmethod
    def from_root(cls, root: str):
        return AppManager(apps=cls._get_apps('{0}\settings\settings.txt'.format(root)), root=root)

    @classmethod
    def _get_apps(cls, path_settings: str):
        with open(path_settings) as f:
            ls_settings = [[elt.rstrip("\n") for elt in line.split("\t")] for line in f.readlines()]
        settings = [{ls_settings[0][k]: ls_settings[i][k] for k in range(len(ls_settings[0]))} for i in
                    range(1, len(ls_settings))]
        return {elt['name']:App(name=elt['name'],path_project=elt['directory'],version_py=elt['py_version'],entry_point=elt['entry_point'],env=elt['venv']) for elt in settings}

    def mk_app(self, name: str, **kwargs):
        force_regen = kwargs.pop('force_regen', False)
        if self.check_app(name) and force_regen:
            self.rm_app(name)
        # Generate virtual environment
        if not os.path.isdir(r'{0}\venvs\{1}'.format(self.root,self.apps[name].env)):
            if self.apps[name].version_py == '':
                os.system(r'py -m venv {0}\venvs\{1}'.format(self.root, self.apps[name].env))
            else:
                os.system(r'py -{0} -m venv {1}\venvs\{2}'.format(self.apps[name].version_py, self.root, self.apps[name].env))
            os.system('workon {0} & setprojectdir "{1}" & deactivate'.format(self.apps[name].env,self.apps[name].path_project))
            os.system(r'workon {1} & pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r "{0}\requirements.txt" & deactivate'.format(self.apps[name].path_project,self.apps[name].env))
        # Generate batch launcher
        with open(r'{0}\template_launcher.txt'.format(_PATH_INTERNAL)) as f:
            batch = f.readlines()
        for i, row in enumerate(batch):
            for str_rep, att_name in self.__class__._replacements:
                row = row.replace(str_rep,self.apps[name].__getattribute__(att_name))
                batch[i] = row
        with open(r'{0}\scripts\{1}.bat'.format(self.root,name),'w+') as f:
            f.write("".join(batch))

    def up_app(self, name: str):
        os.system('workon {0} & setprojectdir "{1}" & deactivate'.format(self.apps[name].env,
                                                                         self.apps[name].path_project))
        os.system(r'workon {1} & pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r "{0}\requirements.txt" & deactivate'.format(
            self.apps[name].path_project, self.apps[name].env))

    def rm_app(self, name: str):
        nb_venv_uses = len([elt for elt in self.apps if self.apps[elt].env == self.apps[name].env])
        if nb_venv_uses <= 1:
            os.system('rmvirtualenv {0}'.format(self.apps[name].env))
        os.remove(r"{0}\scripts\{1}.bat".format(self.root,name))

    def check_app(self, name: str):
        return os.path.exists(r"{0}\scripts\{1}.bat".format(self.root, name))
