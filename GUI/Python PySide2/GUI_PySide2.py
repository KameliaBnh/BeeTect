import sys
import os
from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtCore import QFile, Qt, QCoreApplication
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog, QMessageBox, QAction, QMenu

# Get the path to the directory containing the PySide2 modules
pyside2_dir = os.path.dirname(QtWidgets.__file__)

# Add the PySide2 plugins directory to the Qt plugin search path
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(pyside2_dir, "plugins", "platforms")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_file = QFile("C:/Users/benha/Documents/Cranfield/Group Project/BPT_Cranfield/GUI/interface.ui", self)
        ui_file.open(QFile.ReadOnly)
        # Load the .ui file as a widget
        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()
        self.setCentralWidget(self.ui)
        self.setWindowTitle("Automated Pollinator Monitoring")
        self.setWindowIcon(QtGui.QIcon("C:/Users/benha/Documents/Cranfield/Group Project/BPT_Cranfield/GUI/bee.png"))
        self.ui.Open.triggered.connect(self.open_image)

    def open_image(self):
        # Display a file dialog to select a file
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.xpm *.jpg *.bmp *.JPEG *.JPG *.PNG *.BMP *.XPM *.jpeg)")
        file_dialog.setViewMode(QFileDialog.Detail)
        file_dialog.setFileMode(QFileDialog.ExistingFile)

        if file_dialog.exec_() == QDialog.Accepted:
            # Get the path to the selected file
            image_path = file_dialog.selectedFiles()[0]

            # Load the image and display it in the QLabel widget
            image = QtGui.QImage(image_path)
            if image.isNull():
                QMessageBox.information(self, "Image Viewer", "Unable to load image.")
            else:
                self.ui.image_label.setPixmap(QtGui.QPixmap.fromImage(image).scaled(self.ui.image_label.size(), QtCore.Qt.KeepAspectRatio))

if __name__ == "__main__":
    # Set the Qt::AA_ShareOpenGLContexts attribute
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

    # Create the Qt application
    app = QApplication(sys.argv)

    # Create the main window
    window = MainWindow()

    # Show the main window
    window.show()

    # Run the Qt event loop
    sys.exit(app.exec_())
