pyvfx-boilerplate
==================

A boilerplate for creating PyQt4/PySide and PyQt5/PySide2 applications running in Maya, Nuke or completely standalone.

## Documentation

### Version 2.x

#### Changes from 1.0

- Complete rewrite of the boilerplate.
- Requires the [`Qt.py`](https://github.com/mottosso/Qt.py) module (v0.2.5) to detect Qt bindings.
- Uses `PySide.QUiTools` instead of `pysideuic`.
- No longer uses the complex "wrap instance" approach in favor for simpler code. Because of this, UIs are no longer loaded into `self`.
- Maya palette removed (will be back soon).
- Git repo name change: all lowercase.
- Pretty much PEP8 compliant.
- Now comes with `Qt.WindowStaysOnTopHint` out of the box.
- Can be run in multiple ways (see examples).

<br>

#### Example usage

```python
# Download, install and run standalone
git clone https://github.com/pyvfx-boilerplate.git
cd pyvfx-boilerplate
pip install -U Qt.py
python
>>> import boilerplate
>>> boilerplate.run_standalone()
```

```python
# Just run as standalone
pip install Qt.py
python boilerplate.py
```

```python
# Run in script editor of Maya or Nuke (requires having installed Qt.py)
import sys
sys.path.append('/path/to/pyvfx-boilerplate')
import boilerplate

boilerplate.run_maya()  # or boilerplate.run_nuke()
```

You can also copy-paste the boilerplate.py contents into the script editor of Maya or Nuke and just execute it. Make sure you set the path to your .ui files prior to executing the code.

<br>

#### Modifying the boilerplate

Open up `boilerplate.py` and scroll down to the `# Configuration` section and review the settings.

Rename every occurance of `boil` in the code to reflect a unique name for your application.

Change the class `Boilerplate` to your heart's content!

<br>

#### Development guidelines

Since the boilerplate relies on [`Qt.py`](https://github.com/mottosso/Qt.py), you should design your application as if you were designing it for PyQt5/PySide2. This means creating widgets using `QtWidgets` rather than `QtGui`. The `Qt.py` module takes care of the remapping and makes for compatibility with PyQt4/PySide. Read more over at the [`Qt.py` repository](https://github.com/mottosso/Qt.py).

Tip: when you cannot rely on `Qt.py`, create an issue (probably over at [`Qt.py`](https://github.com/mottosso/Qt.py)) and/or detect which binding is being used and write some custom code:

```python
from Qt import __binding__

if __binding__.startswith('PyQt'):
    ...
elif __binding.startswith('PySide'):
    ...
```

<br>


## Version 1.0

Edit boilerplate.py and edit the "QT_BINDINGS" variable to say either "Auto", "PySide" or "PyQt". 
Then just execute boilerplate.py either inside of Nuke, Maya or as standalone. Please note that Maya 2013 and above as well as Nuke 6.3 and above has native support for PySide.

The script is setup in such a way that .ui files are loaded the same way whether you use PySide or PyQt, which is the main reason for why I created this boilerplate.

I've dumped the Maya 2015 QPalette, which can be used if you run your app in Standalone mode, outside of your DCC app. The first step of making a "Pro" app ;)

More information on usage and customization over at the project's wiki: https://github.com/fredrikaverpil/pyvfx-boilerplate/wiki
