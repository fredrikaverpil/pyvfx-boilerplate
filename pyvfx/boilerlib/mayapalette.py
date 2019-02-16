import json

from Qt import QtGui
from Qt import QtWidgets


def set_palette_from_dict(dct):
    """Set palette to current QApplication based on given dictionary"""
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
    palette = QtGui.QPalette()
    for role in roles:
        try:
            for group in groups:
                color = QtGui.QColor(dct['%s:%s' % (role, group)])
                qGrp = getattr(QtGui.QPalette, group)
                qRl = getattr(QtGui.QPalette, role)
                palette.setColor(qGrp, qRl, color)
        except:
            print('Could not use: ' + str(palette))
    try:
        QtWidgets.QApplication.setPalette(palette)
    except:
        print('Could not set palette: ' + str(palette))


def set_style():
    """Set style"""
    available_styles = QtWidgets.QStyleFactory.keys()
    if 'Fusion' in available_styles:
        QtWidgets.QApplication.setStyle("Fusion")
    elif 'Plastique' in available_styles:
        QtWidgets.QApplication.setStyle("Plastique")


def set_maya_tweaks():
    """Apply Maya-specific styling"""
    base_palette = QtWidgets.QApplication.palette()

    # Set custom colors
    LIGHT_COLOR = QtGui.QColor(100, 100, 100)
    MID_COLOR = QtGui.QColor(68, 68, 68)

    # Create a new palette
    tab_palette = QtGui.QPalette(base_palette)
    tab_palette.setBrush(QtGui.QPalette.Window,
                         QtGui.QBrush(LIGHT_COLOR))
    tab_palette.setBrush(QtGui.QPalette.Button,
                         QtGui.QBrush(MID_COLOR))

    # Define the widgets that needs tweaking
    widget_palettes = {}
    widget_palettes["QTabBar"] = tab_palette
    widget_palettes["QTabWidget"] = tab_palette

    # Set the new tweaked palette
    for name, palette in widget_palettes.items():
        QtWidgets.QApplication.setPalette(palette, name)


def read_json(filepath):
    """Read given JSON filepath into dictionary"""
    with open(filepath, 'r') as data_file:
        data = json.load(data_file)
    return data


def set_maya_palette_with_tweaks(palette_filepath):
    """Apply styling to current QApplication"""
    data = read_json(palette_filepath)
    set_palette_from_dict(data)
    set_style()
    set_maya_tweaks()
