import glob
import os
from os.path import dirname, isfile, join


def __list_all_modules():
    work_dir = dirname(__file__)
    mod_paths = glob.glob(join(work_dir, "*", "*.py"))

    all_modules = []
    for f in mod_paths:
        if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py"):
            rel_path = os.path.relpath(f, work_dir)
            mod_name = "." + os.path.splitext(rel_path)[0].replace("/", ".").replace("\\", ".")
            all_modules.append(mod_name)

    return all_modules


ALL_MODULES = sorted(__list_all_modules())
__all__ = ALL_MODULES + ["ALL_MODULES"]
