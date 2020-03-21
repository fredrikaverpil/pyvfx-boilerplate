# pyvfx-boilerplate

![Tests](https://github.com/fredrikaverpil/pyvfx-boilerplate/workflows/Tests/badge.svg) ![PyPI](https://github.com/fredrikaverpil/pyvfx-boilerplate/workflows/PyPI/badge.svg)

A boilerplate for creating PyQt4/PySide and PyQt5/PySide2 applications running in Maya, Nuke, Blender, 3DS Max, Houdini, Unreal Engine or completely standalone.

## Documentation

### Version 3.x

- The entire boilerplate was re-written so it could be packaged and distributed with PyPi.
- Adding Blender, 3DS Max, Houdini, and Unreal Engine support.

For details, see [CHANGELOG.md](CHANGELOG.md).

### Noteworthy known issues

- Does not work with Nuke 10.0v1 on OS X: [#7](https://github.com/fredrikaverpil/pyvfx-boilerplate/issues/7)
- Maya palette glitchy in standalone mode with PySide/PyQt4 on OS X (disabled by default): [#9](https://github.com/fredrikaverpil/pyvfx-boilerplate/issues/9)
- Window will not stay on top of Nuke (OS X) without Qt.Tool or Qt.WindowStaysOnTopHint: [#12](https://github.com/fredrikaverpil/pyvfx-boilerplate/issues/12)
### Installation

Easy way:

```bash
pip install pyvfx-boilerplate
```

Long way:

```bash
git clone https://github.com/fredrikaverpil/pyvfx-boilerplate.git
cd pyvfx-boilerplate
python setup.py sdist bdist_wheel
pip install dist/*
```

### Example usage

Pip installs a program named `pyvfx-boilerplate` as an example Run as standalone:
(you may need to additionally install PyQt4, PyQt5, PySide or PySide2 for standalone to work depending on your system configuration)

```bash
pyvfx-boilerplate
```

Run in script editor of Maya or Nuke:

```python
import sys
sys.path.append('/path/to/pyvfx-boilerplate')
from pyvfx_boilerplate import boilerplate_ui
bpr = boilerplate_ui.BoilerplateRunner()
bpr.run_main()
```

### Modifying the boilerplate

- See inheritance example above

### Development guidelines

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

### Issues

Something wrong, have a question or wish to file a feature request?

Open up an issue [here](https://github.com/fredrikaverpil/pyvfx-boilerplate/issues)!

### Contribute

If you wish to contribute, pull requests are more than welcome!
