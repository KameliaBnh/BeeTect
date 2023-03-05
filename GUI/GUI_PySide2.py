import sys
import os
from PySide2 import QtGui, QtWidgets
from PySide2.QtCore import QFile, Qt, QCoreApplication
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QSizePolicy

import cv2
import torch

# Get the path to the directory containing the PySide2 modules
pyside2_dir = os.path.dirname(QtWidgets.__file__)

# Add the PySide2 plugins directory to the Qt plugin search path
os.environ["QT_PLUGIN_PATH"] = os.path.join(pyside2_dir, "plugins") #qt5_applications\Qt\plugins
#os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(pyside2_dir, "plugins", "platforms")


#Get name of the current working directory
cwd = os.getcwd()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_file = QFile(os.path.join(cwd, "interface.ui"), self)
        ui_file.open(QFile.ReadOnly)
        # Load the .ui file as a widget
        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()
        self.setCentralWidget(self.ui)
        self.setWindowTitle("Automated Pollinator Monitoring")
        self.setWindowIcon(QtGui.QIcon(os.path.join(cwd, "bee.png")))
        
        # Connect the button to the function open_image
        self.ui.OpenFile.triggered.connect(self.open_image)
        # Connect the button to the function open_folder
        self.ui.OpenFolder.triggered.connect(self.open_folder)

        # Connect the button to the function on_click
        self.ui.Start.clicked.connect(self.run_detection)

        # Global variable to store the image or folder path
        self.image_path = None
        self.folder_path = None

        # Global flag to check if a file or folder has been selected
        self.folderSelected = False
        self.fileSelected = False



    def open_image(self):
        # Open a file dialog to select an image file
        filepath, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
        self.image_path = filepath

        if filepath:
            self.fileSelected = True
            # Load the image and add it to the scene
            pixmap = QtGui.QPixmap(filepath)
            pixmap = pixmap.scaledToWidth(self.ui.image_label.width())
            self.ui.image_label.setFixedSize(pixmap.size())
            self.ui.image_label.setPixmap(pixmap)
    
    def open_folder(self):
        # Open a file dialog to select a folder
        folder_path = QFileDialog.getExistingDirectory(self, "Open Folder", "", QFileDialog.ShowDirsOnly)
        self.folder_path = folder_path

        if folder_path:
            self.folderSelected = True
            # Loop through the files in the folder and display the first image found
            for file_name in os.listdir(folder_path):
                if file_name.endswith((".jpg", ".JPG")):
                    self.image_path = os.path.join(folder_path, file_name)
                    # Load the image and add it to the scene
                    pixmap = QtGui.QPixmap(self.image_path)
                    pixmap = pixmap.scaledToWidth(self.ui.image_label.width())
                    self.ui.image_label.setFixedSize(pixmap.size())
                    self.ui.image_label.setPixmap(pixmap)
                    break
            


    def run_detection(self):
        model_weights = os.path.join(cwd, "yolov5\\weights\\best.pt")
        save_dir = os.path.join(cwd, "runs\\detect\\exp\\")

        # Check if a file or folder has been selected
        if self.fileSelected == True and self.folderSelected == False:
            # Run detection on the selected image
            image = cv2.imread(self.image_path)
            model = torch.hub.load('ultralytics/yolov5', 'custom', model_weights)
            results = model(image)
            results.save(save_dir, exist_ok=True)
            
            # Save results

            # get class names
            class_names = model.module.names if hasattr(model, 'module') else model.names
            class_labels = results.pred[0][:, -1].numpy().astype(int)
            class_names = [class_names[i] for i in class_labels]
            # get filename from input image path
            image_name = os.path.basename(self.image_path).split('.')[0]
            # get extension from input image path
            image_extension = os.path.splitext(os.path.join(save_dir, self.image_path))[1]
            # get output path of detected image
            output_path = os.path.join(save_dir, image_name + '_detected' + image_extension)
            # rename output image according to the name of the input image
            os.rename(os.path.join(save_dir, "image0.jpg"), output_path)

            self.fileSelected = False

        elif self.fileSelected == False and self.folderSelected == True:
            # Run detection on all images in the selected folder
            model = torch.hub.load('ultralytics/yolov5', 'custom', model_weights)
            for filename in os.listdir(self.folder_path):
                if filename.endswith(".jpg") or filename.endswith(".JPG"):
                    image_path = os.path.join(self.folder_path, filename)
                    print(image_path)
                    image = cv2.imread(image_path)
                    results = model(image)
                    results.save(save_dir, exist_ok=True)

                    # Save results
                    # get class names
                    class_names = model.module.names if hasattr(model, 'module') else model.names
                    class_labels = results.pred[0][:, -1].numpy().astype(int)
                    class_names = [class_names[i] for i in class_labels]
                    # get filename from input image path
                    image_name = os.path.basename(image_path).split('.')[0]
                    # get extension from input image path
                    image_extension = os.path.splitext(os.path.join(save_dir, image_path))[1]
                    # get output path of detected image
                    output_path = os.path.join(save_dir, image_name + '_detected' + image_extension)
                    # rename output image according to the name of the input image
                    os.rename(os.path.join(save_dir, "image0.jpg"), output_path)

            self.folderSelected = False
        
        # Display output image
        pixmap = QtGui.QPixmap(output_path)
        pixmap = pixmap.scaledToWidth(self.ui.image_label.width())
        self.ui.image_label.setFixedSize(pixmap.size())
        self.ui.image_label.setPixmap(pixmap)


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
