import os
import sys

try:
    import maya.cmds as cmds
    import pymel.core as pm
    MAYA = True
except ImportError:
    MAYA = False

try:
    import nuke
    import nukescripts
    NUKE = True
except ImportError:
    NUKE = False


def activate(dockable=False):
    import pyvfx.boilerlib.boilerplateUI
    bpr = pyvfx.boilerlib.boilerplateUI.BoilerplateRunner(pyvfx.boilerlib.boilerplateUI.Boilerplate)
    bpr.run_main(dockable)


if NUKE:
    m = nuke.menu("Nuke")
    m.addCommand("pyvfx/boilerlib UI",
                 "import pyvfx.boilerlib.menu\npyvfx.boilerlib.menu.activate()")
    m.addCommand("pyvfx/boilerlib UI dockable",
                 "import pyvfx.boilerlib.menu\npyvfx.boilerlib.menu.activate(True)")

if MAYA:
    MainMayaWindow = pm.language.melGlobals['gMainWindow']
    customMenu = pm.menu('pyvfx', parent=MainMayaWindow)
    pm.menuItem(label="boilerlib UI",
                command="import pyvfx.boilerlib.menu\npyvfx.boilerlib.menu.activate()",
                parent=customMenu)
    pm.menuItem(label="boilerlib UI dockable",
                command="import pyvfx.boilerlib.menu\npyvfx.boilerlib.menu.activate(True)",
                parent=customMenu)
