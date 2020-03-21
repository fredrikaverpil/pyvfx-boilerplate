#!/usr/bin/env python
import os
import sys

# this is required to keep pyside2 seperate from maya and nuke's pyside2
# make sure this is added to any inherited program to work from cli
if "QT_PREFERRED_PATH" in os.environ:
    sys.path.append(os.environ["QT_PREFERRED_PATH"])

from pyvfx_boilerplate import menu  # noqa


def main():
    menu.activate()


if __name__ == "__main__":
    main()
