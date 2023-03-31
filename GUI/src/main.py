import sys
import os

from PySide2 import QtWidgets
from PySide2.QtCore import Qt, QCoreApplication
from PySide2.QtWidgets import QApplication

import MainWindow

# Get the path to the directory containing the PySide2 modules
pyside2_dir = os.path.dirname(QtWidgets.__file__)

# Add the PySide2 plugins directory to the Qt plugin search path
os.environ["QT_PLUGIN_PATH"] = os.path.join(pyside2_dir, "plugins") #qt5_applications\Qt\plugins

if __name__ == "__main__":
    
    # Set the Qt::AA_ShareOpenGLContexts attribute
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

    # Create the Qt application
    app = QApplication(sys.argv)

    # Create the main window
    window = MainWindow.MainWindow()

    # Show the main window
    window.show()

    # Run the Qt event loop
    sys.exit(app.exec_())

