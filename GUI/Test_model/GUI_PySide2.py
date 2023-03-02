import sys
import os
from PySide2 import QtGui, QtWidgets
from PySide2.QtCore import QFile, Qt, QCoreApplication
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog

import cv2
from yolov5.detect import run

# Get the path to the directory containing the PySide2 modules
pyside2_dir = os.path.dirname(QtWidgets.__file__)

# Add the PySide2 plugins directory to the Qt plugin search path
os.environ["QT_PLUGIN_PATH"] = os.path.join(pyside2_dir, "plugins") #qt5_applications\Qt\plugins
#os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(pyside2_dir, "plugins", "platforms")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_file = QFile("C:/Users/benha/OneDrive - Cranfield University/Documents/Cranfield/Group_Project/BPT_Cranfield/GUI/interface.ui", self)
        ui_file.open(QFile.ReadOnly)
        # Load the .ui file as a widget
        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()
        self.setCentralWidget(self.ui)
        self.setWindowTitle("Automated Pollinator Monitoring")
        self.setWindowIcon(QtGui.QIcon("C:/Users/benha/OneDrive - Cranfield University/Documents/Cranfield/Group_Project/BPT_Cranfield/GUI/bee.png"))
        self.ui.Open.triggered.connect(self.open_image)

        # Connect the button to the function on_click
        self.ui.Start.clicked.connect(self.run_detection_and_display)

        # Global variable to store the image path
        self.image_path = None

    def open_image(self):
        # Open a file dialog to select an image file
        filename, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
        self.image_path = filename

        if filename:
            # Load the image and add it to the scene
            self.ui.image_label.setPixmap(QtGui.QPixmap(filename).scaledToWidth(self.ui.image_label.width()))

    def run_detection(self, filename):
        model_weights = "C:/Users/benha/OneDrive - Cranfield University/Documents/Cranfield/Group_Project/BPT_Cranfield/GUI/Test_model/yolov5/weights/best.pt"
        image = cv2.imread(filename)
        results = run(image, model_weights, conf_thres=0.4)
        return results
    
    def run_detection_and_display(self):
        # get path to selected image
        image_path = self.image_path

        # run detection on image
        results = self.run_detection(image_path)

        # display detection results on raw image
        image = cv2.imread(image_path)
        for result in results:
            label = result['label']
            bbox = result['bbox']
            cv2.rectangle(image, bbox[0], bbox[1], (0, 255, 0), 2)
            cv2.putText(image, label, bbox[0], cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        # get filename from image path
        image_name = os.path.basename(image_path)
        
        # create path for detected image
        output_image = "C:/Users/benha/OneDrive - Cranfield University/Documents/Cranfield/Group_Project/BPT_Cranfield/GUI/Test_model/yolov5/runs/detect/exp/" + image_name

        # display image
        self.ui.image_label.setPixmap(QtGui.QPixmap(output_image).scaledToWidth(self.ui.image_label.width()))


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
