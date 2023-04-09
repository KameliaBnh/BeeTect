import os

from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QMainWindow
from PySide2 import QtCore
from PySide2.QtGui import QFont, QIcon

class HelpWindow(QMainWindow):

    def __init__(self):
        """
        User Guide Window class constructor.
        Opens the user guide window with the 'userGuide.ui' file.
        """

        super().__init__()

        # Load the .ui file
        ui_file = QFile(os.path.join(os.getcwd(), "userGuide.ui"), self)
        ui_file.open(QFile.ReadOnly)

        # Load the .ui file as a widget
        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()
        self.setCentralWidget(self.ui)

        # Set the window as modal
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        # Set the font
        font = QFont()
        font.setPointSize(8)
        self.ui.setFont(font)

        # Set the title and size of the form
        self.setWindowTitle('User Guide')
        self.resize(800, 600)

        # Set icon
        #<a href="https://www.flaticon.com/free-icons/question" title="question icons">Question icons created by Freepik - Flaticon</a>
        self.setWindowIcon(QIcon(os.path.join(os.getcwd(), 'resources', 'help_icon.png')))