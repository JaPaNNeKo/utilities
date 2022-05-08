import os
import warnings
from yggdrasil.app_manager import AppManager, PATH_YGGDRASIL, PATH_INTERNAL
from yggdrasil.utilities.logger import logger
import shutil


def seed():
    """
    Generates yggdrasil base folder template.
    If a path is defined in YGGDRASIL_ROOT environment variable, it will be created under the given path.
    If not, it will resort to a default path (under user Documents).
    Under the Yggdradil root folder, will be generated:
    - tools folder: Store base code repos
    - venvs folder: Store virtual environments for each drivers
    - settings: Store congiguration file for drivers creation
    - scripts: Store batch files for each drivers
    At runtime, this function will also create a settings.yaml template (under settings folder) and a
    ls_tools.bat file (under scripts folder), listing the drivers installed under yggdrasil
    """
    path_root = PATH_YGGDRASIL
    os.mkdir(path_root)
    os.mkdir(r'{0}\venvs'.format(path_root))
    os.mkdir(r'{0}\scripts'.format(path_root))
    os.mkdir(r'{0}\settings'.format(path_root))
    shutil.copy(
        r'{0}\data\ls_tools.txt'.format(PATH_INTERNAL),
        r'{0}\scripts\ls_tools.bat'.format(path_root)
    )
    shutil.copy(
        r'{0}\data\template_settings.yaml'.format(PATH_INTERNAL),
        r'{0}\settings\settings.yaml'.format(path_root)
    )
    if r"{0}\scripts".format(path_root) not in os.environ['Path'].split(";"):
        warnings.warn(r"Please add {0}\scripts to your Path variable for easier access to utilities".format(path_root))


def run(cmd: str, **kwargs):
    """
    Base runner for AppManager.
    :param cmd: Command to run ("make", "update" or "remove")
    :param kwargs: Depending on the command run (debug parameter for all functions, force_regen for drivers creation)
    This function gives access to the underlying runner for any command on the AppManager, in case finer control
    / more agnostic code is needed instead of the simpler functions of the module (create, remove, update)
    """
    apps = kwargs.pop("apps", None)
    debug = kwargs.get("debug")
    if debug:
        logger.setLevel("DEBUG")
    else:
        logger.setLevel("INFO")
    mger = AppManager.from_default()
    if apps == '*':
        apps = [app.name for app in mger.apps]
    elif isinstance(apps, str):
        apps = [apps]
    for name_app in apps:
        mger.functions[cmd](name_app, **kwargs)


def create(apps, debug=False, force_regen=False):
    """
    Creates an application
    :param apps: Name of the application (as per settings file)
    :param debug: Run in debug mode (True) or standard mode (False), affecting level of logging & drivers creation behaviour.
    False by default
    :param force_regen: Force re-creation of the drivers if it already exists or not. If False & the drivers already exists,
    creation will be skipped. If True, then drivers will be completely removed before being re-created
    """
    run("create", apps=apps, debug=debug, force_regen=force_regen)


def remove(apps, debug=False):
    """
    Removes an application
    :param apps: Name of the application (as per settings file)
    :param debug: Run in debug mode (True) or standard mode (False), affecting level of logging & drivers creation behaviour.
    False by default
    """
    run("remove", apps=apps, debug=debug)


def show():
    run("show", apps='*')
    # mger = AppManager.from_default()
    # print(mger.show_apps())