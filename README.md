pyvfx.boilerplate
==================

A boilerplate for creating PyQt4/PySide and PyQt5/PySide2 applications running in Maya, Nuke or completely standalone.

## Documentation



### Version 3.0.0

#### Changes from 2.0 (nzanepro fork)

- Updated to work with latest Qt.py (1.2.0b2)
- Tested with maya (2018.4), nuke (11.2v4), and PySide2 (5.11.2)
- Install via pip and you will get Qt.py installed as a dependency (see below)

- Example new app via inheritance of Boilerplate:
```python
import sys
import os
import platform

from Qt import QtCompat
from pyvfx.boilerplate import boilerplateUI


class myPlate(boilerplateUI.Boilerplate):
    def __init__(self, parent=None, win_title='defaultTitle', win_object='defaultObject'):
        super(myPlate, self).__init__(parent, win_title, win_object)

    def setupUi(self):
        main_window_file = os.path.join('uifile.ui')
        self.main_widget = QtCompat.load_ui(main_window_file)
        self.setCentralWidget(self.main_widget)
        self.main_widget.pushButton.clicked.connect(self.say_hello)

    def say_hello(self):
        print('Hello world!')


if __name__ == "__main__":
    bpr = boilerplateUI.BoilerplateRunner(guiClass=myPlate, win_title='Myplate', win_object='myPlate')
    bpr.run_main()
```

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

easy way:
```bash
pip install git+https://github.com/nzanepro/pyvfx.boilerplate
```
long way:
```bash
git clone https://github.com/nzanepro/pyvfx.boilerplate
cd pyvfx.boilerplate
python setup.py sdist bdist_wheel
pip install dist/*
```

<br>

#### Example usage

Pip installs a program named `pyvfx.boilerplateUI` as an example Run as standalone:
(you may need to additionally install PyQt4, PyQt5, PySide or PySide2 for standalone to work depending on your system configuration)

```bash
pyvfx.boilerplateUI
```

Run in script editor of Maya or Nuke:

```python
import sys
sys.path.append('/path/to/pyvfx.boilerplate')
from pyvfx.boilerplate import boilerplateUI
bpr = boilerplateUI.BoilerplateRunner()
bpr.run_main()
```

<br>

#### Modifying the boilerplate

- see inheritance example above

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

Open up an issue [here](https://github.com/nzanepro/pyvfx.boilerplate/issues)!

#### Contribute

If you wish to contribute, pull requests are more than welcome!
