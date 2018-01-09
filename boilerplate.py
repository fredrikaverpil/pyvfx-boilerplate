"""This uses a Qt binding of "any" kind, thanks to the Qt.py module,
to produce an UI. First, one .ui file is loaded and then attaches
another .ui file onto the first. Think of it as creating a modular UI.

More on Qt.py:
https://github.com/mottosso/Qt.py
"""

import sys
import os
import platform

sys.dont_write_bytecode = True  # Avoid writing .pyc files

# ----------------------------------------------------------------------
# Environment detection
# ----------------------------------------------------------------------

try:
    import maya.cmds as cmds
    MAYA = True
except ImportError:
    MAYA = False

try:
    import nuke
    import nukescripts
    NUKE = True
except ImportError:
    NUKE = False

STANDALONE = False
if not MAYA and not NUKE:
    STANDALONE = True


# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------

# Window title and object names
WINDOW_TITLE = 'Boilerplate'
WINDOW_OBJECT = 'boilerPlate'

# Maya-specific
DOCK_WITH_MAYA_UI = False

# Nuke-specific
DOCK_WITH_NUKE_UI = False

# Repository path, e.g. REPO_PATH = '/Users/fredrik/code/repos/pyvfx-boilerplate/'
REPO_PATH = os.path.dirname(__file__)

# Palette filepath
PALETTE_FILEPATH = os.path.join(
    REPO_PATH, 'boilerdata', 'qpalette_maya2016.json')

# Full path to where .ui files are stored
UI_PATH = os.path.join(REPO_PATH, 'boilerdata')

# Qt.py option: Set up preffered binding
# os.environ['QT_PREFERRED_BINDING'] = 'PyQt4'
# os.environ['QT_PREFERRED_BINDING'] = 'PySide'
# os.environ['QT_PREFERRED_BINDING'] = 'PyQt5'
# os.environ['QT_PREFERRED_BINDING'] = 'PySide2'
if NUKE:
    # Avoid loading site-wide PyQt4/PyQt5 inside of Nuke
    os.environ['QT_PREFERRED_BINDING'] = 'PySide'


# ----------------------------------------------------------------------
# Set up Python modules access
# ----------------------------------------------------------------------

# Enable access to boilerlib (Qt.py, mayapalette)
if REPO_PATH not in sys.path:
    sys.path.append(REPO_PATH)

# ----------------------------------------------------------------------
# Main script
# ----------------------------------------------------------------------

from boilerlib.Qt import QtWidgets  # pylint: disable=E0611
from boilerlib.Qt import QtCore  # pylint: disable=E0611
from boilerlib.Qt import QtCompat

from boilerlib import mayapalette


# Debug
# print('Using' + QtCompat.__binding__)


class Boilerplate(QtWidgets.QMainWindow):
    """Example showing how UI files can be loaded using the same script
    when taking advantage of the Qt.py module and build-in methods
    from PySide/PySide2/PyQt4/PyQt5."""

    def __init__(self, parent=None):
        super(Boilerplate, self).__init__(parent)

        # Set object name and window title
        self.setObjectName(WINDOW_OBJECT)
        self.setWindowTitle(WINDOW_TITLE)

        # Window type
        self.setWindowFlags(QtCore.Qt.Window)

        if MAYA:
            # Makes Maya perform magic which makes the window stay
            # on top in OS X and Linux. As an added bonus, it'll
            # make Maya remember the window position
            self.setProperty("saveWindowPref", True)

        # Filepaths
        main_window_file = os.path.join(UI_PATH, 'main_window.ui')
        module_file = os.path.join(UI_PATH, 'module.ui')

        # Load UIs
        self.main_widget = QtCompat.load_ui(main_window_file)  # Main window UI
        self.module_widget = QtCompat.load_ui(module_file)  # Module UI

        # Attach module to main window UI's boilerVerticalLayout layout
        self.main_widget.boilerVerticalLayout.addWidget(self.module_widget)

        # Edit widget which resides in module UI
        self.module_widget.boilerLabel.setText('Push the button!')

        # Edit widget which resides in main window UI
        self.main_widget.boilerPushButton.setText('Push me!')

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
        self.module_widget.boilerLabel.setText('Hello world!')


# ----------------------------------------------------------------------
# DCC application helper functions
# ----------------------------------------------------------------------

def _maya_delete_ui():
    """Delete existing UI in Maya"""
    if cmds.window(WINDOW_OBJECT, q=True, exists=True):
        cmds.deleteUI(WINDOW_OBJECT)  # Delete window
    if cmds.dockControl('MayaWindow|' + WINDOW_TITLE, q=True, ex=True):
        cmds.deleteUI('MayaWindow|' + WINDOW_TITLE)  # Delete docked window


def _nuke_delete_ui():
    """Delete existing UI in Nuke"""
    for obj in QtWidgets.QApplication.allWidgets():
        if obj.objectName() == WINDOW_OBJECT:
            obj.deleteLater()


def _maya_main_window():
    """Return Maya's main window"""
    for obj in QtWidgets.qApp.topLevelWidgets():
        if obj.objectName() == 'MayaWindow':
            return obj
    raise RuntimeError('Could not find MayaWindow instance')


def _nuke_main_window():
    """Returns Nuke's main window"""
    for obj in QtWidgets.qApp.topLevelWidgets():
        if (obj.inherits('QMainWindow') and
                obj.metaObject().className() == 'Foundry::UI::DockMainWindow'):
            return obj
    else:
        raise RuntimeError('Could not find DockMainWindow instance')


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
                parentWidgetList.append(
                    parent.parentWidget())
                parentWidgetList.append(
                    parent.parentWidget().parentWidget())
                parentWidgetList.append(
                    parent.parentWidget().parentWidget().parentWidget())

                for sub in parentWidgetList:
                    for tinychild in sub.children():
                        try:
                            tinychild.setContentsMargins(0, 0, 0, 0)
                        except:
                            pass


# ----------------------------------------------------------------------
# Run functions
# ----------------------------------------------------------------------

def run_maya():
    """Run in Maya"""
    _maya_delete_ui()  # Delete any existing existing UI
    boil = Boilerplate(parent=_maya_main_window())

    # Makes Maya perform magic which makes the window stay
    # on top in OS X and Linux. As an added bonus, it'll
    # make Maya remember the window position
    boil.setProperty("saveWindowPref", True)

    if not DOCK_WITH_MAYA_UI:
        boil.show()  # Show the UI
    elif DOCK_WITH_MAYA_UI:
        allowed_areas = ['right', 'left']
        cmds.dockControl(WINDOW_TITLE, label=WINDOW_TITLE, area='left',
                         content=WINDOW_OBJECT, allowedArea=allowed_areas)


def run_nuke():
    """Run in Nuke

    Note:
        If you want the UI to always stay on top, replace:
        `boil.ui.setWindowFlags(QtCore.Qt.Tool)`
        with:
        `boil.ui.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)`

        If you want the UI to be modal:
        `boil.ui.setWindowModality(QtCore.Qt.WindowModal)`
    """
    _nuke_delete_ui()  # Delete any alrady existing UI
    if not DOCK_WITH_NUKE_UI:
        boil = Boilerplate(parent=_nuke_main_window())
        boil.setWindowFlags(QtCore.Qt.Tool)
        boil.show()  # Show the UI
    elif DOCK_WITH_NUKE_UI:
        prefix = ''
        basename = os.path.basename(__file__)
        module_name = basename[: basename.rfind('.')]
        if __name__ == module_name:
            prefix = module_name + '.'
        panel = nukescripts.panels.registerWidgetAsPanel(
            widget=prefix + 'Boilerplate',  # module_name.Class_name
            name=WINDOW_TITLE,
            id='uk.co.thefoundry.' + WINDOW_TITLE,
            create=True)
        pane = nuke.getPaneFor('Properties.1')
        panel.addToPane(pane)
        boil = panel.customKnob.getObject().widget
        _nuke_set_zero_margins(boil)


def run_standalone():
    """Run standalone

    Note:
        Styling the UI with the Maya palette on OS X when using the
        PySide/PyQt4 bindings result in various issues, which is why
        it is disabled by default when you're running this combo.

    .. _Issue #9:
       https://github.com/fredrikaverpil/pyvfx-boilerplate/issues/9
    """
    app = QtWidgets.QApplication(sys.argv)
    boil = Boilerplate()
    if not (platform.system() == 'Darwin' and
            (QtCompat.__binding__ == 'PySide' or QtCompat.__binding__ == 'PyQt4')):
        mayapalette.set_maya_palette_with_tweaks(PALETTE_FILEPATH)
    boil.show()  # Show the UI
    sys.exit(app.exec_())


if __name__ == "__main__":
    if MAYA:
        run_maya()
    elif NUKE:
        run_nuke()
    else:
        run_standalone()
