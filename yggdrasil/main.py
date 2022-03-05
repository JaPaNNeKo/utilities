import os
import yggdrasil.app_manager as app_manager
import warnings
from yggdrasil.logger import logger


def create_seed():
    path_root = '{0}\Yggdrasil'.format(app_manager.PATH_YGGDRASIL)
    os.mkdir(path_root)
    os.mkdir(r'{0}\venvs'.format(path_root))
    os.mkdir(r'{0}\scripts'.format(path_root))
    os.mkdir(r'{0}\settings'.format(path_root))

    with open(r'{0}\data\ls_tools.txt'.format(app_manager._PATH_INTERNAL)) as f:
        batch_ls = f.readlines()
    with open(r'{0}\scripts\ls_tools.bat'.format(path_root), 'w+') as f:
        f.write("".join(batch_ls))
    with open(r'{0}\settings\settings.txt'.format(path_root), 'w+') as f:
        f.write('name\tpy_version\tvenv\tdirectory\tentry_point')
    if r"{0}\scripts".format(path_root) not in os.environ['Path'].split(";"):
        warnings.warn(r"Please add {0}\scripts to your Path variable for easier access to utilities".format(path_root))


def run(cmd: str, **kwargs):
    apps = kwargs.pop("apps", None)
    debug = kwargs.get("debug")
    if debug:
        logger.setLevel("DEBUG")
    else:
        logger.setLevel("INFO")
    mger = app_manager.AppManager.from_root(r'{0}\Yggdrasil'.format(app_manager.PATH_YGGDRASIL))
    if apps is None:
        apps = mger.apps.keys()
    elif isinstance(apps, str):
        apps = [apps]
    for name_app in apps:
        mger.functions[cmd](name_app, **kwargs)


def create(apps, debug=False, force_regen=False):
    run("make", apps=apps, debug=debug)


def remove(apps, debug=False):
    run("remove", apps=apps, debug=debug)


def update(apps, debug=False):
    run("update", apps=apps, debug=debug)
