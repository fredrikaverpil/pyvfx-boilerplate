"""This uses a Qt binding of "any" kind, thanks to the Qt.py module,
to produce an UI. First, one .ui file is loaded and then attaches
another .ui file onto the first. Think of it as creating a modular UI.

More on Qt.py:
https://github.com/mottosso/Qt.py
"""

import sys
import os
import platform
import atexit
from . import mayapalette

import Qt
from Qt import QtWidgets, QtCore, QtCompat  # pylint: disable=E0611

try:
    import maya.cmds as cmds
    from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

    MAYA = True
except ImportError:
    MAYA = False

try:
    import nuke
    import nukescripts

    NUKE = True
except ImportError:
    NUKE = False

try:
    import hou

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
    import unreal

    UNREAL = True
except ImportError:
    UNREAL = False

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------

# Full path to where .ui files are stored
UI_PATH = os.path.join(os.path.dirname(__file__), "resources")

# Palette filepath
PALETTE_FILEPATH = os.path.join(UI_PATH, "qpalette_maya2016.json")
WTITLE = "Boilerplate"
WOBJ = "boilerPlate"

# ----------------------------------------------------------------------
# Main script
# ----------------------------------------------------------------------


class _Boilerplate(QtWidgets.QMainWindow):
    """
    Don't subclass this directly, subclass Boilerplate without the '_'
    """

    def __init__(self, parent=None, win_title=WTITLE, win_object=WOBJ):

        super(_Boilerplate, self).__init__(parent)

        # Set object name and window title
        self.setObjectName(win_object)
        self.setWindowTitle(win_title)

        # Window type
        self.setWindowFlags(QtCore.Qt.Window)

        if MAYA:
            # Makes Maya perform magic which makes the window stay
            # on top in OS X and Linux. As an added bonus, it'll
            # make Maya remember the window position
            self.setProperty("saveWindowPref", True)

        self.setupUi()

    def setupUi(self):
        # Filepaths
        main_window_file = os.path.join(UI_PATH, "main_window.ui")
        module_file = os.path.join(UI_PATH, "module.ui")

        # Load UIs
        self.main_widget = QtCompat.load_ui(main_window_file)  # Main window UI
        self.module_widget = QtCompat.load_ui(module_file)  # Module UI

        # Attach module to main window UI's boilerVerticalLayout layout
        self.main_widget.boilerVerticalLayout.addWidget(self.module_widget)

        # Edit widget which resides in module UI
        self.module_widget.boilerLabel.setText("Push the button!")

        # Edit widget which reside in main window UI
        self.main_widget.boilerPushButton.setText("Push me!")

        # Set the main widget
        self.setCentralWidget(self.main_widget)

        # Define minimum size of UI
        self.setMinimumSize(200, 200)

        # Signals
        # The "pushButton" widget resides in the main window UI
        self.main_widget.boilerPushButton.clicked.connect(self.say_hello)

    def say_hello(self):
        """Set the label text.
        The "label" widget resides in the module
        """
        self.module_widget.boilerLabel.setText("Hello world!")
        self.module_widget.boilerLabel.update()


if MAYA:

    class Boilerplate(MayaQWidgetDockableMixin, _Boilerplate):
        """Example showing how UI files can be loaded using the same script
        when taking advantage of the Qt.py module and build-in methods
        from PySide/PySide2/PyQt4/PyQt5."""

        def __init__(self, parent=None, win_title=WTITLE, win_object=WOBJ):
            super(Boilerplate, self).__init__(
                parent, win_title=win_title, win_object=win_object
            )


# elif THREEDSMAX:
#     # https://forums.autodesk.com/t5/3ds-max-programming/3ds-max-2019-qt-dock-widget/td-p/8164550 # noqa
#     # https://help.autodesk.com/view/3DSMAX/2019/ENU/?guid=__py_ref_demo_py_side_tool_bar_q_widget_8py_example_html # noqa
#     pass
else:

    class Boilerplate(_Boilerplate):
        """Example showing how UI files can be loaded using the same script
        when taking advantage of the Qt.py module and build-in methods
        from PySide/PySide2/PyQt4/PyQt5."""

        def __init__(self, parent=None, win_title=WTITLE, win_object=WOBJ):
            super(Boilerplate, self).__init__(
                parent, win_title=win_title, win_object=win_object
            )


# ----------------------------------------------------------------------
# DCC application helper functions
# ----------------------------------------------------------------------
def _maya_delete_ui(window_title, window_object):
    """Delete existing UI in Maya"""
    if cmds.window(window_object, q=True, exists=True):
        cmds.deleteUI(window_object)  # Delete window
    if cmds.dockControl("MayaWindow|" + window_title, q=True, ex=True):
        cmds.deleteUI("MayaWindow|" + window_title)  # Delete docked window


def _maya_delete_workspace(window_object):
    """Delete existing workspace in Maya"""
    control = window_object + "WorkspaceControl"
    if cmds.workspaceControl(control, q=True, exists=True):
        cmds.workspaceControl(control, e=True, close=True)
        cmds.deleteUI(control, control=True)


def _maya_update_workspace(window_object):
    """Updates existing workspace in Maya"""
    control = window_object + "WorkspaceControl"
    # TODO make this argument controllable
    if cmds.workspaceControl(control, q=True, exists=True):
        cmds.workspaceControl(
            control,
            e=True,
            restore=True,
            retain=True,
            # # options below
            # dockToMainWindow=("left", -1),
            # tabToControl=("ChannelBoxLayerEditor", -1),
            # tabToControl=("Outliner", -1),
            tabToControl=("AttributeEditor", -1),
        )


def _maya_main_window():
    """Return Maya's main window"""
    for obj in QtWidgets.QApplication.instance().topLevelWidgets():
        if obj.objectName() == "MayaWindow":
            return obj
    raise RuntimeError("Could not find MayaWindow instance")


def _nuke_delete_ui(window_object):
    """Delete existing UI in Nuke"""
    for obj in QtWidgets.QApplication.allWidgets():
        if obj.objectName() == window_object:
            obj.deleteLater()


def _nuke_main_window():
    """Returns Nuke's main window"""
    for obj in QtWidgets.QApplication.instance().topLevelWidgets():
        if (
            obj.inherits("QMainWindow")
            and obj.metaObject().className() == "Foundry::UI::DockMainWindow"
        ):
            return obj
    else:
        raise RuntimeError("Could not find DockMainWindow instance")


def _nuke_set_zero_margins(widget_object):
    """Remove Nuke margins when docked UI

    .. _More info:
        https://gist.github.com/maty974/4739917
    """
    parentApp = QtWidgets.QApplication.allWidgets()
    parentWidgetList = []
    for parent in parentApp:
        for child in parent.children():
            if widget_object.__class__.__name__ == child.__class__.__name__:
                parentWidgetList.append(parent.parentWidget())
                try:
                    twoup = parent.parentWidget().parentWidget()
                    parentWidgetList.append(twoup)
                    threeup = twoup.parentWidget()
                    parentWidgetList.append(threeup)
                except AttributeError:
                    pass

                for sub in parentWidgetList:
                    if sub is not None:
                        for tinychild in sub.children():
                            try:
                                tinychild.setContentsMargins(0, 0, 0, 0)
                            except AttributeError:
                                pass


def _houdini_main_window():
    """Return Houdini's main window"""
    return hou.ui.mainQtWindow()


def _3dsmax_main_window():
    """Return 3dsmax's main window"""
    return MaxPlus.GetQMaxMainWindow()


# ----------------------------------------------------------------------
# Run functions
# ----------------------------------------------------------------------
class BoilerplateRunner:
    def __init__(self, guiClass=Boilerplate, win_title=WTITLE, win_object=WOBJ):  # noqa

        self.guiClass = guiClass
        self.window_title = win_title
        self.window_object = win_object
        self.boil = None

    def run_maya(self, **kwargs):
        """Run in Maya"""
        # Delete any existing existing UI
        _maya_delete_ui(self.window_title, self.window_object)
        # Delete any existing existing workspace
        _maya_delete_workspace(self.window_object)
        self.boil = self.guiClass(
            _maya_main_window(), self.window_title, self.window_object
        )

        # Makes Maya perform magic which makes the window stay
        # on top in OS X and Linux. As an added bonus, it'll
        # make Maya remember the window position
        self.boil.setProperty("saveWindowPref", True)

        if "dockable" in kwargs and kwargs["dockable"]:
            kwargs["allowed_areas"] = ["right", "left"]
        self.boil.show(**kwargs)
        if "dockable" in kwargs and kwargs["dockable"]:
            _maya_update_workspace(self.window_object)

    def run_nuke(self, **kwargs):
        """Run in Nuke

        Note:
            If you want the UI to always stay on top, replace:
            `boil.ui.setWindowFlags(QtCore.Qt.Tool)`
            with:
            `boil.ui.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)`

            If you want the UI to be modal:
            `boil.ui.setWindowModality(QtCore.Qt.WindowModal)`
        """
        _nuke_delete_ui(self.window_object)  # Delete any alrady existing UI
        if "dockable" in kwargs and kwargs["dockable"]:
            widgetname = ("{}.{}").format(
                self.guiClass.__module__, self.guiClass.__name__
            )
            panel = nukescripts.panels.registerWidgetAsPanel(
                widget=widgetname,  # module_name.Class_name
                name=self.window_title,
                id="uk.co.thefoundry." + self.window_title,
                create=True,
            )
            pane = nuke.getPaneFor("Properties.1")
            panel.addToPane(pane)
            self.boil = panel.customKnob.getObject().widget
            _nuke_set_zero_margins(self.boil)
        else:
            self.boil = self.guiClass(
                _nuke_main_window(), self.window_title, self.window_object
            )
            self.boil.setWindowFlags(QtCore.Qt.Tool)
            self.boil.show()  # Show the UI

    def run_houdini(self, **kwargs):
        """Run in Houdini"""
        self.boil = self.guiClass(
            _houdini_main_window(), self.window_title, self.window_object
        )
        self.boil.show()

    def run_3dsmax(self, **kwargs):
        """Run in 3dsmax"""
        # https://gist.github.com/mrabito/0f9d1f177a3bea94d33d35b476c88731
        # dockable?
        # https://help.autodesk.com/view/3DSMAX/2019/ENU/?guid=__py_ref_demo_py_side_tool_bar_q_widget_8py_example_html
        self.boil = self.guiClass(
            _3dsmax_main_window(), self.window_title, self.window_object
        )
        self.boil.show()

    def on_exit_unreal(self):
        app = QtWidgets.QApplication.instance()
        if app:
            app.store_window_geometry()
            app.quit()

    def run_unreal(self, **kwargs):
        # https://github.com/20tab/UnrealEnginePython
        # https://forums.unrealengine.com/development-discussion/python-scripting/1674204-dock-qtwidget-to-unreal
        # https://github.com/AlexQuevillon/UnrealPythonLibrary/blob/master/UnrealProject/UnrealPythonLibrary/Plugins/UnrealPythonLibraryPlugin/Content/Python/PythonLibraries/QtFunctions.py
        # https://forums.unrealengine.com/unreal-engine/unreal-studio/1526501-how-to-get-the-main-window-of-the-editor-to-parent-qt-or-pyside-application-to-it
        app = QtWidgets.QApplication.instance()

        if not app:
            # create the first instance
            app = QtWidgets.QApplication(sys.argv)
            app.aboutToQuit.connect(self.on_exit_unreal)

        atexit.register(self.on_exit_unreal)

        self.boil = None

        self.event_loop = QtCore.QEventLoop()
        self.boil = self.guiClass(None, self.window_title, self.window_object)
        mayapalette.set_maya_palette_with_tweaks(PALETTE_FILEPATH)
        unreal.parent_external_window_to_slate(self.boil.winId())
        self.boil.show()

    def on_exit_blender(self):
        """
        Close BlenderApplication instance on exit

        Returns: None

        """
        app = QtWidgets.QApplication.instance()
        if app:
            app.store_window_geometry()
            app.quit()

    def on_update_blender(self):
        # https://github.com/techartorg/bqt
        app = QtWidgets.QApplication.instance()
        if app.should_close:
            win = bpy.context.window_manager.windows[0]
            bpy.ops.wm.quit_blender({"window": win}, "INVOKE_DEFAULT")

    def run_blender(self, **kwargs):
        """Run in Blender"""
        # mix of code from
        # https://github.com/friedererdmann/blender_pyside2_example
        # and
        # https://github.com/techartorg/bqt

        # TODO add dockable?
        # https://github.com/cube-creative/guibedos/blob/master/guibedos/blender.py
        app = QtWidgets.QApplication.instance()

        if not app:
            # create the first instance
            app = QtWidgets.QApplication(sys.argv)
            # modal
            bpy.app.timers.register(self.on_update_blender, persistent=True)

        atexit.register(self.on_exit_blender)

        self.event_loop = QtCore.QEventLoop()
        self.boil = self.guiClass(None, self.window_title, self.window_object)
        mayapalette.set_maya_palette_with_tweaks(PALETTE_FILEPATH)
        self.boil.show()
        # non-modal:
        # app.exec_()

    def run_standalone(self, **kwargs):
        """Run standalone

        Note:
            Styling the UI with the Maya palette on OS X when using the
            PySide/PyQt4 bindings result in various issues, which is why
            it is disabled by default when you're running this combo.

        .. _Issue #9:
           https://github.com/fredrikaverpil/pyvfx-boilerplate/issues/9
        """
        extrawin = True
        app = QtWidgets.QApplication.instance()

        if not app:
            app = QtWidgets.QApplication(sys.argv)
            extrawin = False

        self.boil = self.guiClass(
            win_title=self.window_title, win_object=self.window_object
        )
        if not (platform.system() == "Darwin" and (Qt.IsPySide or Qt.IsPyQt4)):
            mayapalette.set_maya_palette_with_tweaks(PALETTE_FILEPATH)
        self.boil.show()  # Show the UI

        if not extrawin:
            sys.exit(app.exec_())

    def run_main(self, **kwargs):
        """Run appropriate gui"""
        if MAYA:
            self.run_maya(**kwargs)
        elif NUKE:
            self.run_nuke(**kwargs)
        elif HOUDINI:
            self.run_houdini(**kwargs)
        elif THREEDSMAX:
            self.run_3dsmax(**kwargs)
        elif BLENDER:
            self.run_blender(**kwargs)
        elif UNREAL:
            self.run_unreal(**kwargs)
        else:
            self.run_standalone(**kwargs)
