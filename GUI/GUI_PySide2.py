import shutil
import sys
import os
import cv2
import torch

from PySide2 import QtGui, QtWidgets
from PySide2.QtCore import QFile, Qt, QCoreApplication
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog


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
        self.imagePath = None
        self.folderPath = None

        # Global flag to check if a file or folder has been selected
        self.folderSelected = False
        self.fileSelected = False

        # Create dictionary to store the results for each image
        self.resultsImage = {}


    def open_image(self):
        # Open a file dialog to select an image file
        filepath, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.jpg *.jpeg *.png *.bmp)")
        self.imagePath = filepath
        # If the image is of the wrong format, open a message box
        if filepath.endswith((".jpg", ".jpeg", ".png", ".bmp", ".JPG", ".JPEG", ".PNG", ".BMP")) == False:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText("Please select an image file of accepted format.")
            msg.setWindowTitle("Error")
            msg.exec_()
            return
        
        # Set the infoText label to display explanation 
        self.ui.infoText.setText("Running detection on the selected image...")
        self.ui.infoText.repaint()

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
        self.folderPath = folder_path

        if folder_path:
            self.folderSelected = True
            # Loop through the files in the folder and display the first image found
            for file_name in os.listdir(folder_path):
                if file_name.endswith((".jpg", ".JPG", "*.jpeg", "*.JPEG", "*.png", "*.PNG", "*.bmp", "*.BMP")):
                    self.imagePath = os.path.join(folder_path, file_name)

                    # Load the image and add it to the scene
                    pixmap = QtGui.QPixmap(self.imagePath)
                    pixmap = pixmap.scaledToWidth(self.ui.image_label.width())
                    self.ui.image_label.setFixedSize(pixmap.size())
                    self.ui.image_label.setPixmap(pixmap)
                    break

                
        # Use of the previous and next buttons to navigate through the images
        self.ui.next.clicked.connect(self.next_image)
        self.ui.previous.clicked.connect(self.previous_image)

        # Set the infoText label to display explanation 
        self.ui.infoText.setText("Running detection on all the images in the selected folder...")
        self.ui.infoText.repaint()

    def next_image(self):
        # Get the list of files in the folder
        files = os.listdir(self.folderPath)
        # If the file is not an image, remove from the list
        for file in files:
            if file.endswith((".jpg", ".JPG", "*.jpeg", "*.JPEG", "*.png", "*.PNG", "*.bmp", "*.BMP")) == False:
                files.remove(file)
        # Get the index of the current image in the list
        index = files.index(os.path.basename(self.imagePath))
        # If the current image is the last one, set the index to 0
        if index == len(files) - 1:
            index = 0
        else:
            index += 1
        # Get the next image in the list
        self.imagePath = os.path.join(self.folderPath, files[index])

        # Load the image and add it to the scene
        pixmap = QtGui.QPixmap(self.imagePath)
        pixmap = pixmap.scaledToWidth(self.ui.image_label.width())
        self.ui.image_label.setFixedSize(pixmap.size())
        self.ui.image_label.setPixmap(pixmap)

    def previous_image(self):
        # Get the list of image files in the folder
        files = os.listdir(self.folderPath)
        # If the file is not an image, remove from the list
        for file in files:
            if file.endswith((".jpg", ".JPG", "*.jpeg", "*.JPEG", "*.png", "*.PNG", "*.bmp", "*.BMP")) == False:
                files.remove(file)
        # Get the index of the current image in the list
        index = files.index(os.path.basename(self.imagePath))
        # If the current image is the first one, set the index to the last one
        if index == 0:
            index = len(files) - 1
        else:
            index -= 1
        # Get the previous image in the list
        self.imagePath = os.path.join(self.folderPath, files[index])

        # Load the image and add it to the scene
        pixmap = QtGui.QPixmap(self.imagePath)
        pixmap = pixmap.scaledToWidth(self.ui.image_label.width())
        self.ui.image_label.setFixedSize(pixmap.size())
        self.ui.image_label.setPixmap(pixmap)
     


    def run_detection(self):
        model_weights = os.path.join(cwd, "yolov5\\weights\\best.pt")

        # Create a folder to save the results
        
        # Display a message box asking the user if they want the folder to be the default one or if they want to select a different one
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setText("Save Results")
        msg.setInformativeText("Do you want to save the results in the default folder or do you want to select a different one?")
        msg.setWindowTitle("Save Results")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        msg.button(QtWidgets.QMessageBox.Ok).setText('Default Folder')
        msg.button(QtWidgets.QMessageBox.Cancel).setText('Select Folder')

        if msg.exec_() == QtWidgets.QMessageBox.Cancel:
            # Ask the user to select a folder to save the results
            save_dir = QFileDialog.getExistingDirectory(self, "Save Results", "", QFileDialog.ShowDirsOnly)
            # If the folder already exists, delete it and create a new one
            if os.path.exists(save_dir):
                shutil.rmtree(os.path.join(cwd, save_dir))
            # If the folder does not exist, create it
            os.makedirs(save_dir)
        
        elif msg.exec_() == QtWidgets.QMessageBox.Ok:
            # Save the results in the default folder
            save_dir = os.path.join(cwd, "runs\\detect\\exp")
            # If the folder already exists, delete it and create a new one
            if os.path.exists(save_dir):
                shutil.rmtree(save_dir)
       


        ## Check if a file or folder has been selected

        if self.fileSelected == True and self.folderSelected == False:
        # If a file has been selected, run detection on the selected image

            # Clear the results dictionary
            self.resultsImage.clear()

            # Run detection on the selected image
            image = cv2.imread(self.imagePath)[:, :, ::-1] # BGR to RGB for detection (OpenCV uses BGR) 
            model = torch.hub.load('ultralytics/yolov5', 'custom', model_weights) 
            model.conf = 0.5 #increase confidence threshold 0.5
            results = model(image)

            # Save the results to a directory
            results.save(save_dir=save_dir, exist_ok=True) 
            results.print()

            # Save results to a text file
            save_results_file = open(os.path.join(save_dir, 'results.txt'), 'w')
            save_results_file.write(str(results))
            
            # Save results

            # get class names
            class_names = model.module.names if hasattr(model, 'module') else model.names
            class_labels = results.pred[0][:, -1].numpy().astype(int)
            class_names = [class_names[i] for i in class_labels]


            # get filename from input image path
            image_name = os.path.basename(self.imagePath).split('.')[0]
            
            # Save results to a JSON file
            results.pandas().xyxy[0].to_json(orient="records", path_or_buf=os.path.join(save_dir, image_name + ".json"))
            
            # Add the name of the image and the corresponding classes to the resultsImage dictionary
            self.resultsImage[image_name] = class_names

            # get extension from input image path
            image_extension = os.path.splitext(self.imagePath)[1]

            # get output path of detected image
            output_path = os.path.join(save_dir, image_name + '_detected' + image_extension)

            # rename output image according to the name of the input image
            os.replace(os.path.join(save_dir, "image0.jpg"), output_path)

            self.fileSelected = False


        elif self.fileSelected == False and self.folderSelected == True:
        # If a folder has been selected, run detection on all the images in the folder

            # Clear the results dictionary
            self.resultsImage.clear()

            # Load the YOLOv5 model
            model = torch.hub.load('ultralytics/yolov5', 'custom', model_weights)
            model.conf = 0.5 #increase confidence threshold 0.5

            # Get a list of image file names in the selected folder
            list_images = os.listdir(self.folderPath)

            # Create an empty list to hold the images
            image_list = []

            # Loop through the list of image file names
            for image_name in list_images:
                # Load the image using OpenCV and append it to the list
                image = cv2.imread(os.path.join(self.folderPath, image_name))[:, :, ::-1] # BGR to RGB for detection (OpenCV uses BGR)
                image_list.append(image)

            # Pass the list of images to the YOLOv5 model
            results = model(image_list)

            # Save the results to a directory
            results.save(save_dir=save_dir, exist_ok=True) 
            # Print results
            results.print()

            # Save results to a text file
            save_results_file = open(os.path.join(save_dir, 'results.txt'), 'w')
            save_results_file.write('Saved ' + str(len(os.listdir(save_dir)) - 1) + ' images to ' + save_dir + '\n')
            save_results_file.write('\n')
            save_results_file.write(str(results))

            # Save pandas datafrale results to a JSON file
            results.pandas().xyxy[0].to_json(orient="records", path_or_buf=os.path.join(save_dir, "results.json"))

            for number, filename in enumerate(os.listdir(self.folderPath)): # Get the filename in the input folder and the corresponding index
                    if filename.endswith(".jpg") or filename.endswith(".JPG") or filename.endswith(".jpeg") or filename.endswith(".JPEG"):
                        image_path = os.path.join(self.folderPath, filename)

                        # Save results

                        # get class names
                        class_names = model.module.names if hasattr(model, 'module') else model.names
                        class_labels = results.pred[0][:, -1].numpy().astype(int)
                        class_names = [class_names[i] for i in class_labels]

                        # get filename from input image path
                        image_name = os.path.basename(image_path).split('.')[0]
                        
                        # Add the name of the image and the corresponding classes to the resultsImage dictionary
                        self.resultsImage[image_name] = class_names

                        # get extension from input image path
                        image_extension = os.path.splitext(image_path)[1]

                        # get output path of detected image
                        output_path = os.path.join(save_dir, image_name + '_detected' + image_extension)

                        # rename output image according to the name of the input image
                        os.replace(os.path.join(save_dir, "image" + str(number) + ".jpg"), output_path)

            self.folderSelected = False
        
        # Display output image
        pixmap = QtGui.QPixmap(output_path)
        pixmap = pixmap.scaledToWidth(self.ui.image_label.width())
        self.ui.image_label.setFixedSize(pixmap.size())
        self.ui.image_label.setPixmap(pixmap)

        self.folderPath = save_dir
        self.imagePath = output_path

        # Use of the previous and next buttons to navigate through the images
        self.ui.next.clicked.connect(self.next_image)
        self.ui.previous.clicked.connect(self.previous_image)

        
        # Display the results in the results dictionary
        print(self.resultsImage)


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
