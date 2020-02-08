import pyvfx.boilerplate.boilerplateUI
try:
    import maya.cmds as cmds
    import pymel.core as pm
    MAYA = True
except ImportError:
    MAYA = False

try:
    import nuke
    NUKE = True
except ImportError:
    NUKE = False


def activate(dockable=False):
    bpr = pyvfx.boilerplate.boilerplateUI.BoilerplateRunner(pyvfx.boilerplate.boilerplateUI.Boilerplate)
    kwargs = {}
    kwargs["dockable"] = dockable
    bpr.run_main(**kwargs)


if NUKE:
    m = nuke.menu("Nuke")
    m.addCommand("pyvfx/boilerplate UI",
                 "import pyvfx.boilerplate.menu\npyvfx.boilerplate.menu.activate()")
    m.addCommand("pyvfx/boilerplate UI dockable",
                 "import pyvfx.boilerplate.menu\npyvfx.boilerplate.menu.activate(True)")

elif MAYA:
    MainMayaWindow = pm.language.melGlobals['gMainWindow']
    if not cmds.menu('pyvfxMenuItemRoot', exists=True):
        cmds.menu("pyvfxMenuItemRoot", label="pyvfx", parent=MainMayaWindow,
                  tearOff=True, allowOptionBoxes=True)

    cmds.menuItem(label="boilerplate UI",
                  parent="pyvfxMenuItemRoot", ec=True,
                  command="import pyvfx.boilerplate.menu\npyvfx.boilerplate.menu.activate()")

    cmds.menuItem(label="boilerplate UI dockable",
                  parent="pyvfxMenuItemRoot", ec=True,
                  command="import pyvfx.boilerplate.menu\npyvfx.boilerplate.menu.activate(True)")

else:
    activate()
