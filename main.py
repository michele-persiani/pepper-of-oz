from poz.gui.widgets import get_main_window
from poz.gui.widgets.xml_factory import load_from_xml
import os.path
import sys
from PySide2 import QtWidgets


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    widgets = load_from_xml('./poz/gui/widgets/poz_config.xml')

    main_window = get_main_window(widgets, 4)

    main_window.show()
    sys.exit(app.exec_())
