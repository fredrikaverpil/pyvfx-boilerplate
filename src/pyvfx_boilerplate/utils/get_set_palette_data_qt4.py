"""Set and get QPalette data from Maya

# Example: fetch palette data from Maya
data = getPaletteInfo()
print data
write_json(data)

# Example: read palette JSON file and set palette
data = read_json()
print data
setPaletteFromDict(data)
setStylePlastique()
setMayaTweaks()
"""

import json

from PySide import QtGui


STYLE = "plastique"
GROUPS = ["Disabled", "Active", "Inactive", "Normal"]
ROLES = [
    "AlternateBase",
    "Background",
    "Base",
    "Button",
    "ButtonText",
    "BrightText",
    "Dark",
    "Foreground",
    "Highlight",
    "HighlightedText",
    "Light",
    "Link",
    "LinkVisited",
    "Mid",
    "Midlight",
    "Shadow",
    "ToolTipBase",
    "ToolTipText",
    "Text",
    "Window",
    "WindowText",
]


def getPaletteInfo():
    palette = QtGui.QApplication.palette()

    # ColorGroups
    groups = []
    for name in dir(QtGui.QPalette):
        curr_pallet = getattr(QtGui.QPalette, name)
        if isinstance(curr_pallet, QtGui.QPalette.ColorGroup):
            if name != "All" and name != "NColorGroups" and name != "Current":
                print("ColorGroup: {}".format(name))
                groups.append(name)
    # ColorRoles
    roles = []
    for name in dir(QtGui.QPalette):
        if isinstance(getattr(QtGui.QPalette, name), QtGui.QPalette.ColorRole):
            if name != "NColorRoles" and name != "NoRole":
                print("ColorGroup: {}".format(name))
                roles.append(name)

    # build a dict with all the colors
    result = {}
    for role in ROLES:

        for group in GROUPS:
            qGrp = getattr(QtGui.QPalette, group)
            qRl = getattr(QtGui.QPalette, role)
            result["%s:%s" % (role, group)] = palette.color(qGrp, qRl).rgba()
    return result


def setPaletteFromDict(dct):
    palette = QtGui.QPalette()
    for role in ROLES:
        for group in GROUPS:
            color = QtGui.QColor(dct["%s:%s" % (role, group)])
            qGrp = getattr(QtGui.QPalette, group)
            qRl = getattr(QtGui.QPalette, role)
            palette.setColor(qGrp, qRl, color)
    QtGui.QApplication.setPalette(palette)


def setStylePlastique():
    QtGui.QApplication.setStyle(STYLE)


def setMayaTweaks():
    base_palette = QtGui.QApplication.palette()

    # Set custom colors
    LIGHT_COLOR = QtGui.QColor(100, 100, 100)
    MID_COLOR = QtGui.QColor(68, 68, 68)

    # Create a new palette
    tab_palette = QtGui.QPalette(base_palette)
    tab_palette.setBrush(QtGui.QPalette.Window, QtGui.QBrush(LIGHT_COLOR))
    tab_palette.setBrush(QtGui.QPalette.Button, QtGui.QBrush(MID_COLOR))

    # Define the widgets that needs tweaking
    widget_palettes = {}
    widget_palettes["QTabBar"] = tab_palette
    widget_palettes["QTabWidget"] = tab_palette

    # Set the new tweaked palette
    for name, palette in widget_palettes.items():
        QtGui.QApplication.setPalette(palette, name)


def write_json(data):
    with open("/Users/fredrik/Desktop/qpalette.json", "w") as outfile:
        json.dump(data, outfile)


def read_json():
    # read
    with open("/Users/fredrik/Desktop/qpalette.json", "r") as handle:
        data = json.load(handle)
    return data
