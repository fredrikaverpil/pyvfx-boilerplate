''' Run mode '''
''' ------------- '''
runMode = 'standalone'
try:
	import maya.cmds as cmds
	import maya.OpenMayaUI as omui
	import shiboken
	runMode = 'maya'
except:
	pass
try:
	import nuke
	from nukescripts import panels
	#import site		# Fix for pysideuic which is not included in Nuke - python 2.7 only
	runMode = 'nuke'	
except:
	pass


''' Imports regardless of Qt type '''
''' ------------------------------ '''
import os, sys
import xml.etree.ElementTree as xml
from cStringIO import StringIO	



''' PySide or PyQt - that is the question... '''
''' ---------------------------------------- '''
QtType = 'PySide'	# Edit this to switch between PySide and PyQt
if QtType == 'PySide':
	from PySide import QtCore, QtGui, QtUiTools
	if (runMode == 'nuke'):
		#sys.path.append( site.getsitepackages() ) 		# Fix for pysideuic which is not included in Nuke - python 2.7 only
		sys.path.append(r'C:\Python26\Lib\site-packages')	# Fix for pysideuic which is not included in Nuke - Windows only
	import pysideuic	
elif QtType == 'PyQt':
	from PyQt4 import QtCore, QtGui, uic
	import sip



''' Variables '''
print 'This app is now using ' + QtType
uiFile = os.path.join(os.path.dirname(__file__), "mainWindow.ui")
windowTitle = 'Hello World'
windowObject = 'helloWorld'



class PyQtPySideFixer(QtGui.QMainWindow):
	def __init__(self, parent=None):
		"""Super, loadUi, signal connections"""
		super(PyQtPySideFixer, self).__init__(parent)
		print 'Making a detour (hack), necessary for when using PyQt'


def loadUiType(uiFile):
	"""
	Pyside lacks the "loadUiType" command, so we have to convert the ui file to py code in-memory first
	and then execute it in a special frame to retrieve the form_class.
	"""
	parsed = xml.parse(uiFile)
	widget_class = parsed.find('widget').get('class')
	form_class = parsed.find('class').text

	with open(uiFile, 'r') as f:
		o = StringIO()
		frame = {}

		if QtType == 'PySide':
			pysideuic.compileUi(f, o, indent=0)
			pyc = compile(o.getvalue(), '<string>', 'exec')
			exec pyc in frame

			#Fetch the base_class and form class based on their type in the xml from designer
			form_class = frame['Ui_%s'%form_class]
			base_class = eval('QtGui.%s'%widget_class)
		elif QtType == 'PyQt':
			form_class = PyQtPySideFixer
			base_class = QtGui.QMainWindow
	return form_class, base_class
form, base = loadUiType(uiFile)



def wrapinstance(ptr, base=None):
	"""
	Utility to convert a pointer to a Qt class instance (PySide/PyQt compatible)

	:param ptr: Pointer to QObject in memory
	:type ptr: long or Swig instance
	:param base: (Optional) Base class to wrap with (Defaults to QObject, which should handle anything)
	:type base: QtGui.QWidget
	:return: QWidget or subclass instance
	:rtype: QtGui.QWidget
	"""
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
	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapinstance( long( main_window_ptr ), QtGui.QWidget )	# Works with both PyQt and PySide



class HelloWorld(form, base):
	def __init__(self, parent=None):
		"""Super, loadUi, signal connections"""
		super(HelloWorld, self).__init__(parent)

		if QtType == 'PySide':
			print 'Loading UI using PySide'
			self.setupUi(self)


		elif QtType == 'PyQt':
			print 'Loading UI using PyQt'
			uic.loadUi(uiFile, self)

		self.setObjectName(windowObject)
		self.setWindowTitle(windowTitle)

		# I can now access the UI from self directly, regardless of having used PySide or PyQt
		# Example:
		self.listWidget.addItem('Hello ... world?')



def runStandalone():
	app = QtGui.QApplication(sys.argv)
	gui = HelloWorld()
	gui.show()
	sys.exit(app.exec_())

def runMaya():
	if cmds.window(windowObject, q=True, exists=True):
		cmds.deleteUI(windowObject)
	global gui
	gui = HelloWorld( maya_main_window() )
	gui.show()

def runNuke():
	#pane = nuke.getPaneFor('Properties.1')
	#panels.registerWidgetAsPanel('helloWorld', 'Hello World', 'uk.co.thefoundry.NukeTestWindow', True).addToPane(pane) # View pane and add it to panes menu
	global gui
	gui = HelloWorld()
	gui.show




if runMode == 'standalone':
	runStandalone()
elif runMode == 'maya':
	runMaya()
elif runMode == 'nuke':
	runNuke()
