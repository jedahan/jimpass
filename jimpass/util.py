""" Util functions """
from subprocess import PIPE, DEVNULL, run, Popen
from os import environ, path, listdir
from jimpass.config import DEFAULTS
import yaml


def read_config_file(file: str) -> dict:
    """
    Complement context with user configuration
    TODO: schema verification
    """
    with open(file, 'r') as f:
        return yaml.safe_load(f)


def get_config() -> dict:
    """
    Provide configuration based on canonical paths or default
    """
    if 'XDG_CONFIG_HOME' in environ:
        xdg_h = environ['XDG_CONFIG_HOME']
        if path.isdir(f"{xdg_h}/jimpass"):
            for f in listdir(f"{xdg_h}/jimpass"):
                if f.startswith("conf") and f.endswith(".yaml" or ".yml"):
                    return read_config_file("/".join([xdg_h, 'jimpass', f]))
    if 'HOME' in environ:
        for f in listdir(f"{environ['HOME']}"):
            if f.startswith(".jimpass") and f.endswith(".yaml" or ".yml"):
                return read_config_file(f"{environ['HOME']}/{f}")
    return DEFAULTS


def srun(input_cmd: str, stdin: str = None, no_output: bool = False) -> (int, str):
    """
    Wrapper for subprocess_run
    """
    if stdin:
        res = Popen(input_cmd, stdout=DEVNULL if no_output else PIPE, stderr=DEVNULL, stdin=PIPE, shell=True)
        output = None if no_output else res.communicate(bytes(stdin, 'utf-8'))[0].decode()
        return res.returncode, output
    else:
        res = run(input_cmd, stdout=DEVNULL if no_output else PIPE, stderr=DEVNULL, encoding="utf-8", shell=True)
        return res.returncode, res.stdout

def prun(runner: str = "rofi", mode: str = "dmenu", prompt: str = None, options: list = None,
         keybindings: list = None, args: dict = None, stdin: str = None) -> (int, str):
    """
    Wrapper for popup rofi/wofi
    """
    cmd = "{runner} "
    prefix = "-"

    if runner == "wofi":
        prefix = "--"

    if mode:
        cmd += f"{prefix}{mode}"
    if prompt:
        cmd += f"-p \"{prompt}\" "
    if options:
        cmd += " ".join([f"{prefix}{opt}" for opt in options]) + " "
    if keybindings:
        if runner == "rofi":
            cmd += " ".join([f"-kb-custom-{kb.exit_code} {kb.mapping}" for kb in keybindings]) + " "
    if args:
        cmd += " ".join([f"{prefix}{key} \"{val}\"" for key, val in args.items()]) + " "

    return srun(cmd, stdin) if stdin else srun(cmd)
