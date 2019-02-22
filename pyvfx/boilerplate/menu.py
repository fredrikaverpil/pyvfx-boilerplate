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
    import pyvfx.boilerplate.boilerplateUI
    bpr = pyvfx.boilerplate.boilerplateUI.BoilerplateRunner(pyvfx.boilerplate.boilerplateUI.Boilerplate)
    bpr.run_main(dockable)


if NUKE:
    m = nuke.menu("Nuke")
    m.addCommand("pyvfx/boilerplate UI",
                 "import pyvfx.boilerplate.menu\npyvfx.boilerplate.menu.activate()")
    m.addCommand("pyvfx/boilerplate UI dockable",
                 "import pyvfx.boilerplate.menu\npyvfx.boilerplate.menu.activate(True)")

if MAYA:
    MainMayaWindow = pm.language.melGlobals['gMainWindow']
    customMenu = pm.menu('pyvfx', parent=MainMayaWindow)
    pm.menuItem(label="boilerplate UI",
                command="import pyvfx.boilerplate.menu\npyvfx.boilerplate.menu.activate()",
                parent=customMenu)
    pm.menuItem(label="boilerplate UI dockable",
                command="import pyvfx.boilerplate.menu\npyvfx.boilerplate.menu.activate(True)",
                parent=customMenu)
