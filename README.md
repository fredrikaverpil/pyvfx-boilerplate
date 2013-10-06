pyVFX-boilerplate
==================

A boilerplate for creating PyQt/PySide applications running in Maya, Nuke or completely standalone.

Edit boiler.pyw and edit the "QtType" variable to say either "PySide" or "PyQt".
Then just execute boiler.pyw either inside of Nuke, Maya or as standalone. Please note that Maya 2013 and above as well as Nuke 6.3 and above has native support for PySide.

The script is setup in such a way that .ui files are loaded the same way whether you use PySide or PyQt which makes it easy to switch back and forth while developing, if necessary.

More information on usage and customization: http://fredrikaverpil.tumblr.com/post/63276257075