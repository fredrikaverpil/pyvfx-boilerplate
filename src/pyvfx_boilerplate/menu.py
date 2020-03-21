import pyvfx_boilerplate.boilerplate_ui as bpui

try:
    import maya.cmds as cmds
    import maya.mel as mel

    MAYA = True
except ImportError:
    MAYA = False

try:
    import nuke

    NUKE = True
except ImportError:
    NUKE = False

try:
    import hou  # noqa

    HOUDINI = True
except ImportError:
    HOUDINI = False

try:
    import MaxPlus

    THREEDSMAX = True
except ImportError:
    THREEDSMAX = False

try:
    import bpy

    BLENDER = True
except ImportError:
    BLENDER = False

try:
    import unreal  # noqa

    UNREAL = True
except ImportError:
    UNREAL = False


rootMenuName = "pyvfx"


def activate(dockable=False):
    bpr = bpui.BoilerplateRunner(bpui.Boilerplate)
    kwargs = {}
    kwargs["dockable"] = dockable
    bpr.run_main(**kwargs)


mcmd = "import pyvfx_boilerplate.menu\npyvfx_boilerplate.menu.activate({})"
if NUKE:
    m = nuke.menu("Nuke")
    menuname = "{}/boilerplate UI".format(rootMenuName)
    m.addCommand("{}/boilerplate UI".format(rootMenuName), mcmd.format(""))
    m.addCommand("{} dockable".format(menuname), mcmd.format("True"))

elif MAYA:
    MainMayaWindow = mel.eval("$temp = $gMainWindow")
    if not cmds.menu("pyvfxMenuItemRoot", exists=True):
        cmds.menu(
            "pyvfxMenuItemRoot",
            label=rootMenuName,
            parent=MainMayaWindow,
            tearOff=True,
            allowOptionBoxes=True,
        )

    cmds.menuItem(
        label="boilerplate UI",
        parent="pyvfxMenuItemRoot",
        ec=True,
        command=mcmd.format(""),
    )

    cmds.menuItem(
        label="boilerplate UI dockable",
        parent="pyvfxMenuItemRoot",
        ec=True,
        command=mcmd.format("True"),
    )

elif HOUDINI:
    print("add menu code here for Houdini")
    activate()

elif UNREAL:
    # http://golaem.com/content/doc/golaem-crowd-documentation/rendering-unreal-engine
    # https://github.com/AlexQuevillon/UnrealPythonLibrary/tree/master/UnrealProject/UnrealPythonLibrary
    print("add menu code here for Unreal")
    activate()

elif THREEDSMAX:

    def activate_dockable():
        activate(True)

    MaxPlus.MenuManager.UnregisterMenu(rootMenuName)
    mb = MaxPlus.MenuBuilder(rootMenuName)
    menuitem = "boilerplate UI"
    menuitemD = "{} dockable".format(menuitem)
    menulist = [
        (menuitem, menuitem, activate),
        (menuitemD, menuitemD, activate_dockable),
    ]
    for item in menulist:
        action = MaxPlus.ActionFactory.Create(item[0], item[1], item[2])
        mb.AddItem(action)
    menu = mb.Create(MaxPlus.MenuManager.GetMainMenu())

elif BLENDER:
    # a little of This
    # https://blender.stackexchange.com/questions/156652/topbar-ht-upper-bar-append-add-menus-in-two-places
    # and a little of this
    # https://blenderartists.org/t/creating-a-custom-menu-option/627316/4

    class PyvfxBoilerplateActivateOperator(bpy.types.Operator):
        """ start the pyvfx_boilerplate ui"""

        bl_idname = "pyvfx_boilerplate_activate"
        bl_label = "boilerplate UI"

        def execute(self, context):
            activate()
            return {"FINISHED"}

    class TOPBAR_MT_pyvfx_menu(bpy.types.Menu):
        """ create the pyvfx top menu and pyvfx menu item"""

        bl_label = rootMenuName

        def draw(self, context):
            """ create the pyvfx menu item"""
            layout = self.layout
            layout.operator("pyvfx_boilerplate_activate")

        def menu_draw(self, context):
            """ create the pyvfx top menu"""
            self.layout.menu("TOPBAR_MT_pyvfx_menu")

    def register():
        bpy.utils.register_class(PyvfxBoilerplateActivateOperator)
        bpy.utils.register_class(TOPBAR_MT_pyvfx_menu)
        bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_pyvfx_menu.menu_draw)

    def unregister():
        bpy.utils.unregister_class(PyvfxBoilerplateActivateOperator)
        bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_pyvfx_menu.menu_draw)
        bpy.utils.unregister_class(TOPBAR_MT_pyvfx_menu)

    register()

else:
    activate()
