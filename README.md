pyvfx-boilerplate
==================

A boilerplate for creating PyQt4/PySide and PyQt5/PySide2 applications running in Maya, Nuke or completely standalone.

## Documentation

### Version 2.x

#### Changes from 1.0

- Complete rewrite of the boilerplate.
- Requires (and bundles) the [`Qt.py`](https://github.com/mottosso/Qt.py)
- Tested with Python 2.7.11 and 3.5.1.
- Uses `PySide.QUiTools` instead of `pysideuic`, which was used in v1.0.
- No longer uses the complex "wrap instance" approach in favor for simpler code. Because of this, UIs are no longer loaded into `self`.
- Maya palette styling in standalone mode.
- Git repo name change: all lowercase.
- Pretty much PEP8 compliant.
- Properly parented window in Maya
- Writing of .pyc (bytecode) files disabled to prevent issues between Python 2 and 3.
- Can be run in multiple ways (see examples).

<br>

#### Noteworthy known issues

- Does not work with Nuke 10.0v1 on OS X: [#7](https://github.com/fredrikaverpil/pyvfx-boilerplate/issues/7)
- Maya palette glitchy in standalone mode with PySide/PyQt4 on OS X (disabled by default): [#9](https://github.com/fredrikaverpil/pyvfx-boilerplate/issues/9)
- Window will not stay on top of Nuke (OS X) without Qt.Tool or Qt.WindowStaysOnTopHint: [#12](https://github.com/fredrikaverpil/pyvfx-boilerplate/issues/12)

<br>

#### Installation

Clone the git repository:

```bash
git clone https://github.com/fredrikaverpil/pyvfx-boilerplate.git
```

Edit `boilerplate.py` to make the `REPO_PATH` point to the location where you cloned the repository.

<br>

#### Example usage

Run as standalone:

```python
python boilerplate.py
```

Run in script editor of Maya or Nuke:

```python
import sys
sys.path.append('/path/to/pyvfx-boilerplate')
import boilerplate

boilerplate.run_maya()  # or boilerplate.run_nuke()
```

You can also copy-paste the boilerplate.py contents into the script editor of Maya or Nuke and just execute it. Make sure you set the paths first in the `boilerplate.py` config.

<br>

#### Modifying the boilerplate

- Open up `boilerplate.py` and scroll down to the `# Configuration` section and review the settings.
- Rename every occurance of `boil` in the code to reflect a unique name for your application.
- Change the class `Boilerplate` to your heart's content!

<br>

#### Development guidelines

Since the boilerplate relies on [`Qt.py`](https://github.com/mottosso/Qt.py), you should design your application as if you were designing it for PyQt5/PySide2. This means creating widgets using `QtWidgets` rather than `QtGui`. The `Qt.py` module takes care of the remapping and makes for compatibility with PyQt4/PySide. Read more over at the [`Qt.py` repository](https://github.com/mottosso/Qt.py).

Tip: when you cannot rely on `Qt.py`, create an issue (probably over at [`Qt.py`](https://github.com/mottosso/Qt.py)) and/or detect which binding is being used and write some custom code:

```python
from Qt import QtCompat

if QtCompat.__binding__ in ('PyQt4', 'PySide'):
    # Do something if PyQt4 or PySide is used

if QtCompat__binding.startswith('PySide'):
    # Do something if PySide or PySide2 is used

if QtCompat__binding == 'PySide2':
    # Do something if PySide2 is used

```

#### Issues

Something wrong, have a question or wish to file a feature request?

Open up an issue [here](https://github.com/fredrikaverpil/pyvfx-boilerplate/issues)!

#### Contribute

If you wish to contribute, pull requests are more than welcome!
