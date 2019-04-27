#!/usr/bin/env python
import os
import sys

# this is required to keep pyside2 seperate from maya and nuke's pyside2
# make sure this is added to any inherited program to work from cli
if "QT_PREFERRED_PATH" in os.environ:
    sys.path.append(os.environ["QT_PREFERRED_PATH"])

import pyvfx.boilerplate.boilerplateUI as bpUI

sys.dont_write_bytecode = True  # Avoid writing .pyc files

if __name__ == "__main__":
    bpr = bpUI.BoilerplateRunner(bpUI.Boilerplate)
    bpr.run_main()
