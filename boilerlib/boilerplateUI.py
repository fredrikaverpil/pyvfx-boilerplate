"""This uses a Qt binding of "any" kind, thanks to the Qt.py module,
to produce an UI. First, one .ui file is loaded and then attaches
another .ui file onto the first. Think of it as creating a modular UI.

More on Qt.py:
https://github.com/mottosso/Qt.py
"""

import sys
import os
import platform
import Qt
from Qt import QtWidgets  # pylint: disable=E0611
from Qt import QtCore  # pylint: disable=E0611
from Qt import QtCompat

import mayapalette

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

sys.dont_write_bytecode = True  # Avoid writing .pyc files

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------

# Full path to where .ui files are stored
UI_PATH = os.path.join(os.path.dirname(__file__), 'resources')

# Palette filepath
PALETTE_FILEPATH = os.path.join(
    UI_PATH, 'qpalette_maya2016.json')

# ----------------------------------------------------------------------
# Main script
# ----------------------------------------------------------------------


class Boilerplate(QtWidgets.QMainWindow):
    """Example showing how UI files can be loaded using the same script
    when taking advantage of the Qt.py module and build-in methods
    from PySide/PySide2/PyQt4/PyQt5."""

    def __init__(self, parent=None, win_title='Boilerplate', win_object='boilerPlate'):
        super(Boilerplate, self).__init__(parent)

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
        main_window_file = os.path.join(UI_PATH, 'main_window.ui')
        module_file = os.path.join(UI_PATH, 'module.ui')

        # Load UIs
        self.main_widget = QtCompat.load_ui(main_window_file)  # Main window UI
        self.module_widget = QtCompat.load_ui(module_file)  # Module UI

        # Attach module to main window UI's boilerVerticalLayout layout
        self.main_widget.boilerVerticalLayout.addWidget(self.module_widget)

        # Edit widget which resides in module UI
        self.module_widget.boilerLabel.setText('Push the button!')

        # Edit widget which reside in main window UI
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
        self.module_widget.boilerLabel.update()




# ----------------------------------------------------------------------
# DCC application helper functions
# ----------------------------------------------------------------------
def _maya_delete_ui(window_title, window_object):
    """Delete existing UI in Maya"""
    if cmds.window(window_object, q=True, exists=True):
        cmds.deleteUI(window_object)  # Delete window
    if cmds.dockControl('MayaWindow|' + window_title, q=True, ex=True):
        cmds.deleteUI('MayaWindow|' + window_title)  # Delete docked window


def _nuke_delete_ui(window_object):
    """Delete existing UI in Nuke"""
    for obj in QtWidgets.QApplication.allWidgets():
        if obj.objectName() == window_object:
            obj.deleteLater()


def _maya_main_window():
    """Return Maya's main window"""
    for obj in QtWidgets.QApplication.instance().topLevelWidgets():
        if obj.objectName() == 'MayaWindow':
            return obj
    raise RuntimeError('Could not find MayaWindow instance')


def _nuke_main_window():
    """Returns Nuke's main window"""
    for obj in QtWidgets.QApplication.instance().topLevelWidgets():
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

class BoilerplateRunner():

    def __init__(self, guiClass=Boilerplate,win_title='Boilerplate', win_object='boilerPlate'):

        self.guiClass = guiClass
        self.window_title = win_title
        self.window_object = win_object

    def run_maya(self, dockable=False):
        """Run in Maya"""
        _maya_delete_ui(self.window_title, self.window_object)  # Delete any existing existing UI
        boil = self.guiClass(_maya_main_window(),self.window_title, self.window_object)

        # Makes Maya perform magic which makes the window stay
        # on top in OS X and Linux. As an added bonus, it'll
        # make Maya remember the window position
        boil.setProperty("saveWindowPref", True)

        if dockable:
            allowed_areas = ['right', 'left']
            cmds.dockControl(self.window_title, label=self.window_title, area='left',
                             content=self.window_object, allowedArea=allowed_areas)
        else:
            boil.show()  # Show the UI


    def run_nuke(self, dockable=False):
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
        if dockable:
            basename = os.path.basename(__file__)
            module_name = os.path.splitext(basename)[0]
            widget = module_name + '.' + self.guiClass.__name__
            panel = nukescripts.panels.registerWidgetAsPanel(
                widget=widget ,  # module_name.Class_name
                name=self.window_title,
                id='uk.co.thefoundry.' + self.window_title,
                create=True)
            pane = nuke.getPaneFor('Properties.1')
            panel.addToPane(pane)
            boil = panel.customKnob.getObject().widget
            _nuke_set_zero_margins(boil)
        else:
            boil = self.guiClass(_nuke_main_window(),self.window_title, self.window_object)
            boil.setWindowFlags(QtCore.Qt.Tool)
            boil.show()  # Show the UI


    def run_standalone(self):
        """Run standalone

        Note:
            Styling the UI with the Maya palette on OS X when using the
            PySide/PyQt4 bindings result in various issues, which is why
            it is disabled by default when you're running this combo.

        .. _Issue #9:
           https://github.com/fredrikaverpil/pyvfx-boilerplate/issues/9
        """
        app = QtWidgets.QApplication(sys.argv)
        boil = self.guiClass(win_title=self.window_title, win_object=self.window_object)
        if not (platform.system() == 'Darwin' and
                (Qt.IsPySide or Qt.IsPyQt4)):
            mayapalette.set_maya_palette_with_tweaks(PALETTE_FILEPATH)
        boil.show()  # Show the UI
        sys.exit(app.exec_())


    def run_main(self, dockable=False):
        """Run appropriate gui"""
        if MAYA:
            self.run_maya(dockable)
        elif NUKE:
            self.run_nuke(dockable)
        else:
            self.run_standalone()
