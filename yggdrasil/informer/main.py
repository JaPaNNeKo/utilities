import importlib_metadata as imp_md
import yaml
import sys
from os.path import exists
from collections import namedtuple

def get_internal_info(distribution: str) -> {}:
    dist = imp_md.distribution(distribution)
    eps_console = dist.entry_points.select(group="console_scripts")
    entry_points = [{'name': ep.name, 'path': r'{0}\Scripts\{1}'.format(sys.prefix, ep.name)} for ep in eps_console]
    pkgs = [pkg for pkg, dists in imp_md.packages_distributions().items() if distribution in dists] # packages names
    libraries = [{'name': pkg, 'path': str(dist.locate_file(pkg))} for pkg in pkgs]
    requirements = [{"requirements":r'{0}\requirements.txt'.format(lib['path'])} for lib in libraries if exists(r'{0}\requirements.txt'.format(lib['path']))]

    return {
        "environment": {'name': sys.prefix.split("\\")[-1], 'path': sys.prefix},
        "entry_points": entry_points,
        "libraries": libraries,
        "requirements": requirements
    }


def dump_internal_info(distribution: str, path_dump: str):
    with open(path_dump, "w") as f:
        yaml.dump(get_internal_info(distribution), f)


def dump_internal_info_venv():
    distribution = sys.argv[1]
    path_dump = r'{0}\ygginfo-{1}.yaml'.format(sys.prefix, distribution)
    dump_internal_info(distribution, path_dump)


class DistInfo(object):
    PathInfo = namedtuple("PathInfo", ["name", "path"])

    def __init__(self, configs):
        self._configs = configs

    @classmethod
    def from_yaml(cls, path):
        with open(path) as file:
            try:
                configs = yaml.safe_load(file)
            except yaml.YAMLError as exc:
                print(exc)
        return DistInfo(configs)

    @property
    def entry_points(self):
        return [self.__class__.PathInfo(name=ep['name'], path=ep['path']) for ep in self._configs['entry_points']]

    @property
    def environment(self):
        return self.__class__.PathInfo(name=self._configs['environment']['name'], path=self._configs['environment']['path'])

    @property
    def libraries(self):
        return [self.__class__.PathInfo(name=lib['name'], path=lib['path']) for lib in self._configs['libraries']]

    @property
    def requirements(self):
        return [self.__class__.PathInfo(name=lib['name'], path=lib['path']) for lib in self._configs['requirements']]
