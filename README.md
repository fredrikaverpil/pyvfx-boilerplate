pyVFX-boilerplate
==================

A boilerplate for creating PyQt/PySide applications running in Maya, Nuke or completely standalone.

Edit boilerplate.py and edit the "QT_BINDINGS" variable to say either "Auto", "PySide" or "PyQt".
Then just execute boilerplate.py either inside of Nuke, Maya or as standalone. Please note that Maya 2013 and above as well as Nuke 6.3 and above has native support for PySide.

The script is setup in such a way that .ui files are loaded the same way whether you use PySide or PyQt, which is the main reason for why I created this boilerplate.

I've dumped the Maya 2015 QPalette, which can be used if you run your app in Standalone mode, outside of your DCC app. The first step of making a "Pro" app ;)

More information on usage and customization over at the project's wiki: https://github.com/fredrikaverpil/pyVFX-boilerplate/wiki
