import shutil
from pathlib import Path


def which(cmd: str) -> Path:
    if path := shutil.which(cmd):
        return Path(path)
    raise RuntimeError(f"{cmd} not found in current environment")
