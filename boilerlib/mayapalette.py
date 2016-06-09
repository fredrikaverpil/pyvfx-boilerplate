import json
from Qt import QtGui
from Qt import QtWidgets


def set_maya_palette_with_tweaks(palette_filepath):

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

    def set_palette_from_dict(dct):
        palette = QtGui.QPalette()
        for role in roles:
            try:
                for group in groups:
                    color = QtGui.QColor(dct['%s:%s' % (role, group)])
                    qGrp = getattr(QtGui.QPalette, group)
                    qRl = getattr(QtGui.QPalette, role)
                    palette.setColor(qGrp, qRl, color)
            except:
                print 'Could not use: ' + str(palette)
        try:
            QtWidgets.QApplication.setPalette(palette)
        except:
            print 'Could not set palette: ' + str(palette)

    def set_style_plastique():
        QtWidgets.QApplication.setStyle("plastique")

    def set_maya_tweaks():
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
        # read
        with open(filepath, 'rb') as data_file:
            data = json.load(data_file)
        return data


    data = read_json(palette_filepath)
    set_palette_from_dict(data)
    set_style_plastique()
    set_maya_tweaks()
