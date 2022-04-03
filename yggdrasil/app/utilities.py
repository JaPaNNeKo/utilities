import subprocess
from yggdrasil.logger import logger
from yggdrasil.exceptions import CmdException


def _unique_match(ls):
    if len(ls) == 0:
        raise Exception("Problem: Unrecognised app type")
    if len(ls) > 1:
        raise Exception("Problem: Several apps match this type")
    return ls[0]


def run_cmds(cmds:[]):
    for cmd in cmds:
        output = subprocess.run(cmd, shell=True, check=False, capture_output=True)
        logger.debug("command output:{0}".format(output.stdout.decode("utf-8")))
        logger.debug("return code: {0}".format(output.returncode))
        if output.returncode != 0:
            raise CmdException(output.stderr.decode("utf-8"))


def generate_custom_batch(source: str, destination: str, replacements: []):
    # Generate batch launcher
    with open(source) as f:
        batch = f.readlines()
    for i, row in enumerate(batch):
        for find, repl in replacements:
            row = row.replace(find, repl)
            batch[i] = row
    with open(destination, 'w+') as f:
        f.write("".join(batch))
