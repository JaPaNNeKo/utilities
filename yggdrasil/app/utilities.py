import subprocess
from yggdrasil.logger import logger


class CmdError(Exception):
    def __init__(self, error: str):
        self.message = 'Aborting, error in commands communicated:\n{0}'.format(error)
        super().__init__(self.message)


def _run_cmds(cmds:[]):
    for cmd in cmds:
        output = subprocess.run(cmd, shell=True, check=False, capture_output=True)
        logger.debug("command output:{0}".format(output.stdout.decode("utf-8")))
        logger.debug("return code: {0}".format(output.returncode))
        if output.returncode != 0:
            raise CmdError(output.stderr.decode("utf-8"))


def _parse_settings(path_file:str) -> []:
    with open(path_file) as f:
        ls_settings = [[elt.rstrip("\n") for elt in line.split("\t")] for line in f.readlines()]
    return [{ls_settings[0][k]: ls_settings[i][k] for k in range(len(ls_settings[0]))} for i in
                range(1, len(ls_settings))]
