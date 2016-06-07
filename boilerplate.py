"""This uses a Qt binding of "any" kind, thanks to the Qt.py module,
to produce an UI. First, one .ui file is loaded and then attaches
another .ui file onto the first. Think of it as creating a modular UI.

More on Qt.py:
https://github.com/mottosso/Qt.py
"""

import sys
import os
import site


# ----------------------------------------------------------------------
# Environment
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
    NUKE_VERSION = nuke.NUKE_VERSION_STRING
    NUKE_VERSION_MAJOR = nuke.NUKE_VERSION_MAJOR
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

# Standalone-specific
PALETTE_FILEPATH = '/Users/fredrik/code/repos/pyvfx-boilerplate/data/qpalette_maya2015.json'

# Full path to where .ui files are stored
UI_PATH = '/Users/fredrik/code/repos/pyvfx-boilerplate/data'

# Find Qt.py module and setup site-packages accordingly
SITE_SEARCH_PATHS = [
    'C:/Python27/Lib/site-packages',  # Windows
    '/usr/lib/python2.7/site-packages',  # Linux
    '/Library/Python/2.7/site-packages',  # OS X

    '/usr/local/Cellar/python/2.7.11/Frameworks/Python.framework/Versions/' +
    'Current/lib/python2.7/site-packages'  # Homebrew location, Python 2.7.11
]

# Qt.py option: Set up preffered binding
# os.environ['QT_PREFERRED_BINDING'] = 'PyQt4'
# os.environ['QT_PREFERRED_BINDING'] = 'PySide'
# os.environ['QT_PREFERRED_BINDING'] = 'PyQt5'
# os.environ['QT_PREFERRED_BINDING'] = 'PySide2'
if NUKE:
    # AvoidPri loading site-wide PyQt4/PyQt5 inside of Nuke
    os.environ['QT_PREFERRED_BINDING'] = 'PySide'


# ----------------------------------------------------------------------
# Python site packages helper functions
# ----------------------------------------------------------------------

def _find_qtpy(search_paths, register=False):
    """Searches for Qt.py and register the site path if register is True"""
    for search_path in search_paths:
        if os.path.exists(search_path):
            for item in os.listdir(search_path):
                if item == 'Qt.py':
                    if register:
                        site.addsitedir(search_path)  # Add site path
                    return True


def _sitepackages_setup(additional_search_paths):
    # Make non-standalone DCC application find Qt.py module
    site_paths = site.getsitepackages()
    if not _find_qtpy(site_paths):
        if not _find_qtpy(additional_search_paths, register=True):
            raise ImportError('Could not find Qt.py module.')


def _ui_dir(folderpath):
    """Attempt to auto-detect path to ui files"""

    if os.path.exists(folderpath):
        return folderpath
    else:
        try:
            boilerplate_dir = os.path.dirname(__file__)
            ui_dir = os.path.join(boilerplate_dir, 'data')
            return ui_dir
        except NameError:
            raise IOError('Could not locate .ui directory.')


# ----------------------------------------------------------------------
# Set up Python modules access
# ----------------------------------------------------------------------

# Set up filepath in order to find .ui files (required for Maya and Nuke)
ui_dir = _ui_dir(UI_PATH)

# Find Qt.py module and setup site-packages accordingly
_sitepackages_setup(SITE_SEARCH_PATHS)


# ----------------------------------------------------------------------
# Main script
# ----------------------------------------------------------------------

# Qt setup
from Qt import QtCore
# from Qt import QtGui
from Qt import QtWidgets
from Qt import __binding__
from Qt import load_ui

from utils import palette

# Debug
print 'Using', __binding__


class Boilerplate(QtWidgets.QWidget):
    """Example showing how UI files can be loaded using the same script
    when taking advantage of the Qt.py module and build-in methods
    from PySide/PySide2/PyQt4/PyQt5."""
    def __init__(self, parent=None):
        super(Boilerplate, self).__init__()
        # Filepaths
        main_window_file = os.path.join(ui_dir, 'main_window.ui')
        module_file = os.path.join(ui_dir, 'module.ui')

        # Load UIs
        self.ui = load_ui(main_window_file)  # Main window
        self.ui.module = load_ui(module_file)  # Module

        # Set object name and window title
        self.ui.setObjectName(WINDOW_OBJECT)
        self.ui.setWindowTitle(WINDOW_TITLE)

        if NUKE and DOCK_WITH_NUKE_UI:
            # Set layout to vertical layout
            self.setLayout(QtWidgets.QVBoxLayout())
            # Attach main UI to layout
            self.layout().addWidget(self.ui)

        # Attach module to main window
        self.ui.verticalLayout.addWidget(self.ui.module)

        # Edit widget which resides in module
        self.ui.module.label.setText('Push the button!')

        # Edit widget which resides in main window
        self.ui.pushButton.setText('Push me!')

        # Signals
        # The "pushButton" widget resides in main window
        self.ui.pushButton.clicked.connect(self.say_hello)

    def say_hello(self):
        """Set the label text.
        The "label" widget resides in the module
        """
        self.ui.module.label.setText('Hello world!')


# ----------------------------------------------------------------------
# DCC application helper functions
# ----------------------------------------------------------------------

def _delete_existing_ui():
    """Delete existing UI"""
    if MAYA:
        if cmds.window(WINDOW_OBJECT, q=True, exists=True):
            cmds.deleteUI(WINDOW_OBJECT)  # Delete window
        if cmds.dockControl('MayaWindow|'+WINDOW_TITLE, q=True, ex=True):
            cmds.deleteUI('MayaWindow|'+WINDOW_TITLE)  # Delete docked window
    elif NUKE:
        pass


# ----------------------------------------------------------------------
# Run functions
# ----------------------------------------------------------------------

def run_maya():
    """Run in Maya"""
    _delete_existing_ui()  # Delete any existing existing UI
    global boil
    boil = Boilerplate(parent=QtWidgets.QApplication.activeWindow())
    if not DOCK_WITH_MAYA_UI:
        boil.ui.setWindowFlags(QtCore.Qt.Tool)  # Stay on top of Maya
        # boil.ui.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # Stay on top
        # boil.ui.setWindowModality(QtCore.Qt.WindowModal)  # Modality
        boil.ui.show()  # Show the UI
    elif DOCK_WITH_MAYA_UI:
        # Dock window with Maya UI
        allowedAreas = ['right', 'left']
        cmds.dockControl(WINDOW_TITLE, label=WINDOW_TITLE, area='left',
                         content=WINDOW_OBJECT, allowedArea=allowedAreas)


def run_nuke():
    """Run in Nuke"""
    _delete_existing_ui()  # Delete any alrady existing UI
    global boil
    if not DOCK_WITH_NUKE_UI:
        boil = Boilerplate(parent=QtWidgets.QApplication.activeWindow())
        boil.ui.setWindowFlags(QtCore.Qt.Tool)  # # Stay on top of Nuke
        # boil.ui.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # Stay on top
        # boil.ui.setWindowModality(QtCore.Qt.WindowModal)  # Modality
        boil.ui.show()  # Show the UI

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


def run_standalone():
    """Run standalone"""
    app = QtWidgets.QApplication(sys.argv)
    global boil
    boil = Boilerplate()
    palette.set_maya_palette_with_tweaks(PALETTE_FILEPATH)
    boil.ui.show()  # Show the UI
    sys.exit(app.exec_())


if __name__ == "__main__":
    if MAYA:
        run_maya()
    elif NUKE:
        run_nuke()
    else:
        run_standalone()
