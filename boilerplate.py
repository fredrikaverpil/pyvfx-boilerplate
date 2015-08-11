# Author: fredrik.averpil@gmail.com, http://fredrikaverpil.tumblr.com
# Github: https://github.com/fredrikaverpil/pyVFX-boilerplate

''' Imports regardless of Qt type
--------------------------------------------------------------------------------
'''
import os, sys, json
import xml.etree.ElementTree as xml
from cStringIO import StringIO



''' Configuration: Global settings
--------------------------------------------------------------------------------
QT_BINDINGS: Edit this to force Qt Bindnings: PySide|PyQt|Auto
QT_BINDINGS_PATH: Possibility to specify external site-packages location (a neat
trick is to customize this further to make the boilerplate load different
site package locations based on e.g. operating system)
UI_FILE: Full path to .ui file to load, created by Qt Designer
WINDOW_TITLE: The visible title of the window
WINDOW_OBJECT: The name of the window object
sys.dont_write_bytecode: Skips .pyc file creation, if set to True '''

QT_BINDINGS = 'Auto'
QT_BINDINGS_PATH = None
UI_FILE = os.path.join(os.path.dirname(__file__), 'main_window.ui')
WINDOW_TITLE = 'Hello World'
WINDOW_OBJECT = 'helloWorld'
sys.dont_write_bytecode = False



''' Configuration: Standalone mode
--------------------------------------------------------------------------------
MAYA_PALETTE: Uses approximately the same stylesheet as seen in Maya 2015 '''

MAYA_PALETTE = False



''' Configuration: Maya
--------------------------------------------------------------------------------
MAYA_LAUNCH_AS_DOCKED_WINDOW:
False = opens as free floating window
True = docks window to Maya UI '''

MAYA_LAUNCH_AS_DOCKED_WINDOW = False



''' Configuration: Nuke
--------------------------------------------------------------------------------
NUKE_LAUNCH_AS_PANEL: Opens a regular window or a panel
NUKE_PARENT_TO_NUKE_MAIN_WINDOW: If True, makes window stay on top of Nuke '''

NUKE_LAUNCH_AS_PANEL = False
NUKE_PARENT_TO_NUKE_MAIN_WINDOW = True



''' Run mode
--------------------------------------------------------------------------------
'''

RUN_MODE = 'standalone'
try:
	import maya.cmds as cmds
	import maya.OpenMayaUI as omui
	import shiboken
	RUN_MODE = 'maya'
except ImportError:
	pass

try:
	import nuke
	import nukescripts
	RUN_MODE = 'nuke'
except ImportError:
	pass



''' Qt Bindnings
--------------------------------------------------------------------------------
'''

if type(QT_BINDINGS_PATH) != type(None):
	print 'Loading external site-packages from', QT_BINDINGS_PATH
	sys.path.append( QT_BINDINGS_PATH ) # Load external site-packages

if QT_BINDINGS == 'Auto':
	try:
		from PySide import QtGui, QtGui, QtUiTools
		import pysideuic
		QT_BINDINGS = 'PySide'
	except ImportError:
		from PyQt4 import QtGui, QtCore, uic
		import sip
		QT_BINDINGS = 'PyQt'
elif QT_BINDINGS == 'PySide':
	from PySide import QtGui, QtGui, QtUiTools
	import pysideuic
elif QT_BINDINGS == 'PyQt':
	from PyQt4 import QtGui, QtCore, uic
	import sip

print	('This app is now running in ' + RUN_MODE + ' mode,'
		' using ' + QT_BINDINGS + ' Qt bindings')



''' Auto-setup classes and functions
--------------------------------------------------------------------------------
'''

class PyQtFixer(QtGui.QMainWindow):
	def __init__(self, parent=None):
		'''Super, loadUi, signal connections'''
		super(PyQtFixer, self).__init__(parent)
		print 'Making a detour (hack), necessary for when using PyQt'


def load_ui_type(UI_FILE):
	'''
	Pyside lacks the "load_ui_type" command, so we have to convert the ui file
	to py code in-memory first and then execute it in a special frame to
	retrieve the form_class.
	'''
	parsed = xml.parse(UI_FILE)
	widget_class = parsed.find('widget').get('class')
	form_class = parsed.find('class').text

	with open(UI_FILE, 'r') as f:
		o = StringIO()
		frame = {}

		if QT_BINDINGS == 'PySide':
			pysideuic.compileUi(f, o, indent=0)
			pyc = compile(o.getvalue(), '<string>', 'exec')
			exec pyc in frame

			# Fetch the base_class and form class based on their type in the xml
			# from designer
			form_class = frame['Ui_%s'%form_class]
			base_class = eval('QtGui.%s'%widget_class)
		elif QT_BINDINGS == 'PyQt':
			form_class = PyQtFixer
			base_class = QtGui.QMainWindow
	return form_class, base_class
form, base = load_ui_type(UI_FILE)



def wrap_instance(ptr, base=None):
	'''
	Utility to convert a pointer to a Qt class instance (PySide/PyQt compatible)

	:param ptr: Pointer to QObject in memory
	:type ptr: long or Swig instance
	:param base: (Optional) Base class to wrap with (Defaults to QObject,
	             which should handle anything)
	:type base: QtGui.QWidget
	:return: QWidget or subclass instance
	:rtype: QtGui.QWidget
	'''
	if ptr is None:
		return None
	ptr = long(ptr) #Ensure type
	if globals().has_key('shiboken'):
		if base is None:
			qObj = shiboken.wrapInstance(long(ptr), QtCore.QObject)
			metaObj = qObj.metaObject()
			cls = metaObj.className()
			superCls = metaObj.superClass().className()
			if hasattr(QtGui, cls):
				base = getattr(QtGui, cls)
			elif hasattr(QtGui, superCls):
				base = getattr(QtGui, superCls)
			else:
				base = QtGui.QWidget
		return shiboken.wrapInstance(long(ptr), base)
	elif globals().has_key('sip'):
		base = QtCore.QObject
		return sip.wrapinstance(long(ptr), base)
	else:
		return None


def maya_main_window():
	''' Returns the main Maya window. This works for both PySide and PyQt. '''
	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrap_instance( long( main_window_ptr ), QtGui.QWidget )



''' Main class
--------------------------------------------------------------------------------
'''

class HelloWorld(form, base):
	def __init__(self, parent=None):
		"""Super, loadUi, signal connections"""
		super(HelloWorld, self).__init__(parent)

		if QT_BINDINGS == 'PySide':
			self.setupUi(self)
		elif QT_BINDINGS == 'PyQt':
			uic.loadUi(UI_FILE, self)

		self.setObjectName(WINDOW_OBJECT)
		self.setWindowTitle(WINDOW_TITLE)

		# Access the UI, regardless of having used PySide or PyQt
		# Example:
		self.listWidget.addItem('Hello world')

	def closeEvent(self, event):
		''' Delete this object when closed.'''
		self.deleteLater()

	def set_maya_palette_with_tweaks(self):
		palette_json_file = os.path.join(os.path.dirname(__file__),
					   'qpalette_maya2015.json')
		groups = ['Disabled', 'Active', 'Inactive', 'Normal']
		roles = [
				'AlternateBase',
				'Background',
				'Base',
				'Button',
				'ButtonText',
				'BrightText',
				'Dark',
				'Foreground',
				'Highlight',
				'HighlightedText',
				'Light',
				'Link',
				'LinkVisited',
				'Mid',
				'Midlight',
				'Shadow',
				'ToolTipBase',
				'ToolTipText',
				'Text',
				'Window',
				'WindowText'
				]

		def set_palette_from_dict(dct):
			palette = QtGui.QPalette()
			for role in roles:
				try:
					for group in groups:
						color = QtGui.QColor(dct['%s:%s' % (role, group)])
						qGrp = getattr(QtGui.QPalette, group)
						qRl = getattr(QtGui.QPalette, role)
						palette.setColor(qGrp, qRl, color)
				except:
					print 'Could not use: ' + str(palette)
			try:
				QtGui.QApplication.setPalette(palette)
			except:
				print 'Could not set palette: ' + str(palette)

		def set_style_plastique():
			QtGui.QApplication.setStyle("plastique")

		def set_maya_tweaks():
			base_palette = QtGui.QApplication.palette()

			# Set custom colors
			LIGHT_COLOR = QtGui.QColor(100, 100, 100)
			MID_COLOR = QtGui.QColor(68, 68, 68)

			# Create a new palette
			tab_palette = QtGui.QPalette(base_palette)
			tab_palette.setBrush(   QtGui.QPalette.Window,
									QtGui.QBrush(LIGHT_COLOR))
			tab_palette.setBrush(	QtGui.QPalette.Button,
									QtGui.QBrush(MID_COLOR))

			# Define the widgets that needs tweaking
			widget_palettes = {}
			widget_palettes["QTabBar"] = tab_palette
			widget_palettes["QTabWidget"] = tab_palette

			# Set the new tweaked palette
			for name, palette in widget_palettes.items():
				QtGui.QApplication.setPalette(palette, name)

		def read_json():
			# read
			with open(palette_json_file, 'rb') as data_file:
				data = json.load(data_file)
			return data

		# Read the JSON theme data and set the palette
		data = read_json()
		set_palette_from_dict(data)
		set_style_plastique()
		set_maya_tweaks()






''' Run functions
--------------------------------------------------------------------------------
'''

def run_standalone():
	app = QtGui.QApplication(sys.argv)
	global gui
	gui = HelloWorld()
	if MAYA_PALETTE:
		gui.set_maya_palette_with_tweaks()
	gui.show()
	sys.exit(app.exec_())

def run_maya():
	if cmds.window(WINDOW_OBJECT, q=True, exists=True):
		cmds.deleteUI(WINDOW_OBJECT)

	if cmds.dockControl( 'MayaWindow|'+WINDOW_TITLE, q=True, ex=True):
		cmds.deleteUI( 'MayaWindow|'+WINDOW_TITLE )

	global gui
	gui = HelloWorld( parent=maya_main_window() )
	# Alternative way of setting parent window below:
	#gui = HelloWorld( parent=QtGui.QApplication.activeWindow() )

	if MAYA_LAUNCH_AS_DOCKED_WINDOW:
		allowedAreas = ['right', 'left']
		cmds.dockControl( WINDOW_TITLE, label=WINDOW_TITLE, area='left',
						  content=WINDOW_OBJECT, allowedArea=allowedAreas )
	else:
		#gui.setWindowModality(QtCore.Qt.WindowModal) # Set modality
		gui.show()

def run_nuke():
	module_name = __name__
	if module_name == '__main__':
		module_name = ''
	else:
		module_name = module_name + '.'
	global gui
	if NUKE_LAUNCH_AS_PANEL:
		panel = nukescripts.panels.registerWidgetAsPanel(
					widget = module_name + '.' + WINDOW_TITLE,
					name = WINDOW_TITLE,
					id='uk.co.thefoundry.' + WINDOW_TITLE,
					create=True)
		pane = nuke.getPaneFor('Properties.1')
		panel.addToPane( pane )
		gui = panel.customKnob.getObject().widget

	else:
		if NUKE_PARENT_TO_NUKE_MAIN_WINDOW:
			gui = HelloWorld( parent=QtGui.QApplication.activeWindow() )
		else:
			gui = HelloWorld()
		#gui.setWindowModality(QtCore.Qt.WindowModal) # Set modality
		gui.show()





if RUN_MODE == 'standalone':
	run_standalone()
'''
elif RUN_MODE == 'maya':
	run_maya()
elif RUN_MODE == 'nuke':
	run_nuke()
'''
