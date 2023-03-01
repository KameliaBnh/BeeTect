import sys
import os
from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtCore import QFile, Qt, QCoreApplication
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog, QMessageBox, QAction, QMenu


#Hello

# Obtenir le chemin du répertoire contenant les modules PySide2
pyside2_dir = os.path.dirname(QtWidgets.__file__)

# Ajouter le répertoire des plugins de PySide2 au chemin de recherche des plugins de Qt
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(pyside2_dir, "plugins", "platforms")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_file = QFile("C:/Users/benha/Documents/Cranfield/Group Project/Test Different GUI/interface.ui", self)
        ui_file.open(QFile.ReadOnly)
        # Charger le fichier .ui en tant que widget
        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()
        self.setCentralWidget(self.ui)
        self.setWindowTitle("Automated Pollinator Monitoring")
        self.setWindowIcon(QtGui.QIcon("C:/Users/benha/Documents/Cranfield/Group Project/Test Different GUI/bee.png"))
        self.ui.Open.triggered.connect(self.open_image)

    def open_image(self):
        # Afficher une boîte de dialogue pour sélectionner un fichier
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.xpm *.jpg *.bmp *.JPEG *.JPG *.PNG *.BMP *.XPM *.jpeg)")
        file_dialog.setViewMode(QFileDialog.Detail)
        file_dialog.setFileMode(QFileDialog.ExistingFile)

        if file_dialog.exec_() == QDialog.Accepted:
            # Obtenir le chemin du fichier sélectionné
            image_path = file_dialog.selectedFiles()[0]

            # Charger l'image et l'afficher dans le widget QLabel
            image = QtGui.QImage(image_path)
            if image.isNull():
                QMessageBox.information(self, "Image Viewer", "Impossible de charger l'image.")
            else:
                self.ui.image_label.setPixmap(QtGui.QPixmap.fromImage(image).scaled(self.ui.image_label.size(), QtCore.Qt.KeepAspectRatio))


if __name__ == "__main__":
    # Set the Qt::AA_ShareOpenGLContexts attribute
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

    # Créer l'application Qt
    app = QApplication(sys.argv)

    # Créer la fenêtre principale
    window = MainWindow()

    # Afficher la fenêtre principale
    window.show()

    # Exécuter la boucle d'événements Qt
    sys.exit(app.exec_())
