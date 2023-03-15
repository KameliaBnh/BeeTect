import datetime
import shutil
import sys
import os
import cv2
import torch

from PySide2 import QtGui, QtWidgets
from PySide2.QtCore import QFile, Qt, QCoreApplication, QTimer
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog, QMessageBox, QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout


# Get the path to the directory containing the PySide2 modules
pyside2_dir = os.path.dirname(QtWidgets.__file__)

# Add the PySide2 plugins directory to the Qt plugin search path
os.environ["QT_PLUGIN_PATH"] = os.path.join(pyside2_dir, "plugins") #qt5_applications\Qt\plugins
#os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(pyside2_dir, "plugins", "platforms")

# Get current working directory
cwd = os.getcwd()

# Path of the text file storing the preferences of the user
preferences_path = os.path.join(cwd, 'preferences.txt')



class UserInfoForm(QWidget):

    def __init__(self):
        super().__init__()

        # Set the title and size of the form
        self.setWindowTitle('User information')
        self.resize(300, 200)

        # Create labels and line edits for user information
        user_label = QLabel('User Information:')
        name_label = QLabel('Name:')
        self.name_edit = QLineEdit()
        surname_label = QLabel('Surname:')
        self.surname_edit = QLineEdit()
        email_label = QLabel('Email:')
        self.email_edit = QLineEdit()

        # Make all line edits required except email
        self.name_edit.setPlaceholderText('Required')
        self.surname_edit.setPlaceholderText('Required')
        self.email_edit.setPlaceholderText('Optional')

        # If the user does not enter a value in the line edit that is required, display a message box

        # Create a submit button
        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.submit)

        # Create a layout for the form
        layout = QVBoxLayout()

        # User information label bold and as a separator
        user_label.setStyleSheet("font-weight: bold")
        layout.addWidget(user_label)
        layout.addWidget(name_label)
        layout.addWidget(self.name_edit)
        layout.addWidget(surname_label)
        layout.addWidget(self.surname_edit)
        layout.addWidget(email_label)
        layout.addWidget(self.email_edit)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def submit(self):
        # Retrieve user information
        name = self.name_edit.text()
        surname = self.surname_edit.text()
        email = self.email_edit.text()

        if not name:
            QMessageBox.warning(self, 'Error', 'Please enter your name.')
            return

        if not surname:
            QMessageBox.warning(self, 'Error', 'Please enter your surname.')
            return

        # Print the user information
        print(f'Name: {name}')
        print(f'Surname: {surname}')
        print(f'Email: {email}')

        # Close the form
        self.close()


class NewModel(QWidget):

    def __init__(self):
        super().__init__()

        # Set the title and size of the form
        self.setWindowTitle('New Detection Model')
        self.resize(300, 200)

        # Create labels and line edits for new model
        model_label = QLabel('Model name:')
        self.model_edit = QLineEdit()
        self.model_edit.setPlaceholderText('Required')

        # Create a model weight label that open a file dialog to select the model weight file
        model_weight_label = QLabel('Model weight:')
        self.model_weight_edit = QLineEdit()
        self.model_weight_edit.setReadOnly(True)
        self.model_weight_button = QPushButton('Browse')
        self.model_weight_button.clicked.connect(self.open_model_weight)

        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.submit)

        # Create a layout for the form
        layout = QVBoxLayout()
        layout.addWidget(model_label)
        layout.addWidget(self.model_edit)
        layout.addWidget(model_weight_label)
        layout.addWidget(self.model_weight_edit)
        layout.addWidget(self.model_weight_button)
        layout.addWidget(self.submit_button)

        # Retrieve the model name
        model_name = self.model_edit.text()

        # Create a folder for the model inside the user project folder
        model_path = os.path.join(cwd, 'models')
        # if it already exists, set the model path to the existing folder
        if os.path.exists(model_path):
            print('Folder already exists')
        else:
            os.mkdir(model_path)

        # Save the model weight file in the user project folder with the name of the model
        self.model_weight_path = os.path.join(model_path, model_name + '.pt')


        self.setLayout(layout)

    
    def open_model_weight(self):
        # Open a file dialog to select the model weight file
        model_weight_file, _ = QFileDialog.getOpenFileName(self, 'Select model weight file', cwd, 'Model weight (*.pt)')
        self.model_weight_edit.setText(model_weight_file)

    def submit(self):
        # Retrieve the model information
        model_name = self.model_edit.text()
        model_weight = self.model_weight_edit.text()

        # Validate required fields
        if not model_name:
            QMessageBox.warning(self, 'Error', 'Please enter a model name.')
            return

        if not model_weight:
            QMessageBox.warning(self, 'Error', 'Please select a model weight file.')
            return

        # Validate that the model weight file exists
        if not os.path.isfile(model_weight):
            QMessageBox.warning(self, 'Error', 'The selected model weight file does not exist.')
            return

        # Create a folder for the model inside the user project folder
        model_path = os.path.join(os.getcwd(), 'models')

        # Save the model weight file in the user project folder with the name of the model
        model_weight_path = os.path.join(model_path, model_name + '.pt')

        # Validate that the destination directory exists
        if not os.path.isdir(os.path.dirname(model_weight_path)):
            QMessageBox.warning(self, 'Error', 'The destination directory for the model weight file does not exist.')
            return

        # Copy the model weight file to the user project folder 
        try:
            print(f'Copying model weight file to {model_weight_path}')
            shutil.copy(model_weight, model_weight_path)
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Error copying model weight file: {str(e)}')
            return

        # Close the form
        self.close()



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
        
        # Close the application when the user clicks the close button
        self.ui.Exit.triggered.connect(self.close)

        # Connect the button to the function open_image
        self.ui.OpenFile.triggered.connect(self.open_image)
        # Connect the button to the function open_image_folder
        self.ui.OpenFolder.triggered.connect(self.open_image_folder)

        # Connect the button to the function open_project
        self.ui.OpenProject.triggered.connect(self.open_project)
        # Connect the button to the function new_project
        self.ui.NewProject.triggered.connect(self.new_project)

        # Connect the button to the function on_click
        self.ui.Start.clicked.connect(self.run_detection)

        # Connect the addModel button to the function add_model
        self.ui.addModel.clicked.connect(self.add_model)


        ##GLOBAL VARIABLES##

        # User information
        self.userName = None
        self.userSurname = None
        self.userEmail = None

        # Project information
        self.projectName = None

        # Global variable to store the image or folder path
        self.imagePath = None
        self.folderPath = None

        # Global flag to check if a file or folder has been selected
        self.folderSelected = False
        self.fileSelected = False

        # Create dictionary to store the results for each image
        self.resultsImage = {}



        # If the preferences.txt file does not exist, open the user information form to ask for user information
        # and save the information in the preferences.txt file

        if not os.path.isfile(os.path.join(cwd, 'preferences.txt')):     
            # If the preferences.txt file does not exist
            # Wait for 5 seconds before opening a message box to ask for user information when the program is launched
            self.timer = QTimer()
            self.timer.timeout.connect(self.user_info_form)
            self.timer.start(1500)

        else: 
            # If the preferences.txt file exists, read the user information from the file
            with open(os.path.join(cwd, 'preferences.txt'), 'r') as f:
                # Skip the first line
                f.readline()
                # Read the user information
                self.userName = f.readline().strip()
                self.userSurname = f.readline().strip()
                self.userEmail = f.readline().strip()



    def user_info_form(self):
        # Stop the timer
        self.timer.stop()

        # Open the user information form
        self.user_info_dialog = UserInfoForm()
        self.user_info_dialog.show()

        # Connect the submit button to the function submit_user_info
        self.user_info_dialog.submit_button.clicked.connect(self.submit_user_info)

    
    def submit_user_info(self):
        # Retrieve the user information
        self.userName = self.user_info_dialog.name_edit.text()
        self.userSurname = self.user_info_dialog.surname_edit.text()
        self.userEmail = self.user_info_dialog.email_edit.text()
        
        # Save the user information in the preferences.txt file
        with open(os.path.join(cwd, 'preferences.txt'), 'w') as f:
            f.write('User information:\n')
            f.write(f'Name: {self.userName}\n')
            f.write(f'Surname: {self.userSurname}\n')
            f.write(f'Email: {self.userEmail}\n')
            # Write the date and time when the user information was saved
            now = datetime.datetime.now()
            date_str = now.strftime("%d/%m/%Y")
            time_str = now.strftime("%H:%M:%S")
            f.write(f'Date: {date_str} Time: {time_str}\n')



    def open_project(self):
        # If the user wants to open an existing project, open a file dialog to select the project folder
        self.folderPath = QFileDialog.getExistingDirectory(self, "Open Project", os.getcwd())
        self.folderSelected = True
        self.fileSelected = False
        # If the user doesn't select a folder, open a message box
        if self.folderPath == '':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("No folder selected")
            msg.setWindowTitle("Warning")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

        # Set the project name to the selected folder name
        self.projectName = os.path.basename(self.folderPath)

        new_line = f'Project Name: {self.projectName}'

        self.save_to_text_file(new_line)


        # Set the project folder path as the current working directory
        os.chdir(self.folderPath)


    def new_project(self):
        # Create a dialog box for selecting project name and folder path
        dialog = QDialog()
        dialog.setWindowTitle("New Project")
        dialog.setModal(True)
        layout = QVBoxLayout(dialog)

        # Add label and line edit for project name
        name_label = QLabel("Project Name:")
        name_edit = QLineEdit()
        layout.addWidget(name_label)
        layout.addWidget(name_edit)

        # Add button for selecting folder path
        path_button = QPushButton("Select Folder")
        path_label = QLabel()
        layout.addWidget(path_button)
        layout.addWidget(path_label)

        # Define function for handling folder path selection
        def select_folder():
            folder_path = QFileDialog.getExistingDirectory(
                dialog,
                "Select Folder",
                "."
            )
            path_label.setText(folder_path)

        # Connect folder path selection button to function
        path_button.clicked.connect(select_folder)

        # Add button for saving project
        save_button = QPushButton("Save")
        layout.addWidget(save_button)

        # Define function for handling project saving
        def save_project():
            project_name = name_edit.text()
            folder_path = path_label.text()
            project_path = f"{folder_path}/{project_name}"
            # Create project folder if it does not exist
            if not os.path.exists(project_path):
                os.makedirs(project_path)
            # If the project folder already exists, open a message box
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Project already exists")
                msg.setWindowTitle("Warning")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return
            
            # Set the project name to the selected folder name
            self.projectName = os.path.basename(project_path)

            new_line = f'Project Name: {self.projectName}'

            self.save_to_text_file(new_line)

            # Set the project folder path as the current working directory
            os.chdir(project_path)

            # Close the dialog box
            dialog.close()

        # Connect save button to function
        save_button.clicked.connect(save_project)

        # Show dialog box
        dialog.exec_()
        
        
    def save_to_text_file(self, new_line):
        # Save the project name in the preferences.txt file
        with open(preferences_path, 'r') as f:
            lines = f.readlines()

        with open(preferences_path, 'w') as f:
            found = False
            for i, line in enumerate(lines):
                if line.startswith('Project Name'):
                    lines[i] = new_line
                    found = True
                    break
            if not found:
                lines.append(new_line)

            f.writelines(lines)

        with open(preferences_path, 'r') as f:
            lines = f.readlines()



    def add_model(self):
        # Create and show the model form
        self.model_form = NewModel()
        self.model_form.show()

        # Add the model name to the combobox
        if self.model_form.model_edit.text() != '':
            self.ui.comboBox.addItem(self.model_form.model_edit.text())



    def open_image(self):

        # Open a file dialog to select an image file
        filepath, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.jpg *.jpeg *.png *.bmp)")
        self.imagePath = filepath
        # If the image is of the wrong format, open a message box
        if filepath.endswith((".jpg", ".jpeg", ".png", ".bmp", ".JPG", ".JPEG", ".PNG", ".BMP")) == False:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
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
    
    def open_image_folder(self):
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

    def get_image_files(self):
        image_files = [f for f in os.listdir(self.folderPath) 
                       if os.path.isfile(os.path.join(self.folderPath, f)) and
                       f.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.JPG', '.JPEG', '.PNG', '.BMP'))]
        return image_files

    def next_image(self):
        image_files = self.get_image_files()
        if len(image_files) == 0:
            return
        
        current_index = image_files.index(os.path.basename(self.imagePath))
        next_index = (current_index + 1) % len(image_files)
        next_image_path = os.path.join(self.folderPath, image_files[next_index])

        self.load_image(next_image_path)

    def previous_image(self):
        image_files = self.get_image_files()
        if len(image_files) == 0:
            return
        
        current_index = image_files.index(os.path.basename(self.imagePath))
        previous_index = (current_index - 1) % len(image_files)
        previous_image_path = os.path.join(self.folderPath, image_files[previous_index])

        self.load_image(previous_image_path)

    def load_image(self, image_path):
        pixmap = QtGui.QPixmap(image_path)
        pixmap = pixmap.scaledToWidth(self.ui.image_label.width())
        self.ui.image_label.setFixedSize(pixmap.size())
        self.ui.image_label.setPixmap(pixmap)
        self.imagePath = image_path
     


    def run_detection(self):
        model_weights = os.path.join(cwd, "models\\yolov5\\weights_2021\\best.pt")

        # Create a folder to save the results
        
        # Display a message box asking the user if they want the folder to be the default one or if they want to select a different one
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Save Results")
        msg.setInformativeText("Do you want to save the results in the default folder or do you want to select a different one? Default folder: runs\\detect\\exp")
        msg.setWindowTitle("Save Results")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.button(QMessageBox.Ok).setText('Default Folder')
        msg.button(QMessageBox.Cancel).setText('Select Folder')

        if msg.exec_() == QMessageBox.Cancel:
            # Ask the user to select a folder to save the results
            save_dir = QFileDialog.getExistingDirectory(self, "Save Results", "", QFileDialog.ShowDirsOnly)
            # If the folder already exists, delete it and create a new one
            if os.path.exists(save_dir):
                shutil.rmtree(os.path.join(os.getcwd(), save_dir))
            # If the folder does not exist, create it
            os.makedirs(save_dir)
        
        elif msg.exec_() == QMessageBox.Ok:
            # Save the results in the default folder
            save_dir = os.path.join(os.getcwd(), "runs\\detect\\exp")
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
