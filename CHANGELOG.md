# Changelog

### Version 3.3.0

- adding Blender, 3DS Max, Houdini, and Unreal Engine support
- see below for installing PySide2 into Blender

Ultra Easy Guide To install PySide2 into Blender on macOS:

1) install blender
2) open blender at least once, and then close blender
3) open terminal and run the commands below
```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
/Applications/Blender.app/Contents/Resources/2.81/python/bin/python3.7m get-pip.py
/Applications/Blender.app/Contents/Resources/2.81/python/bin/pip install PySide2, pyvfx-boilerplate
```

Ultra Easy Guide To install PySide into Unreal on Windows:

this currently fails: (testing on 4.24.2)
1) install Unreal
2) open a windows cmd or powershell and run the commands below
```bash
cd C:/Program Files/Unreal/UE_4.24/Engine/Binaries/ThirdParty/Python/Win64/
python.exe -m pip install --upgrade pip
python.exe -m pip install --no-warn-script-location PySide pyvfx-boilerplate
```

### Version 3.2.1

- rearrangement of namespace package location
- updated to setuptools_scm to handle version numbering

### Version 3.2.0

- uses kwargs to pass more arguments to the gui show
- auto docks into attribute editor panel in maya if dockable=True in kwargs

### Version 3.1.0

#### Changes from 2.0 (nzanepro fork)

- Updated to work with latest Qt.py (1.2.0b2)
- Tested with maya (2018.4), nuke (11.2v4), and PySide2 (5.11.2)
- Install via pip and you will get Qt.py installed as a dependency (see below)
- Now includes MayaQWidgetDockableMixin in maya
- Better Maya menuing via python instead of pymel, pyvfx now has a root menu, and other modules can be added to the menu.

- Example new app via inheritance of Boilerplate (includes extension of MayaQWidgetDockableMixin):

https://github.com/nzanepro/pyvfx.boilerplateinherited

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
