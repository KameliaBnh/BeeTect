import datetime
import shutil
import sys
import os
import time
import cv2
import pandas
import torch

from PySide2 import QtGui, QtWidgets
from PySide2.QtCore import QFile, Qt, QCoreApplication, QTimer
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog, QMessageBox, QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMenu


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
        self.resize(500, 350)

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

        # Create a folder for the model inside the project folder
        self.model_path = os.path.join(cwd, 'models')

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


        # if it already exists, set the model path to the existing folder
        if os.path.exists(self.model_path):
            print('Folder already exists')
        else:
            os.mkdir(self.model_path)


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

        # Save the model weight file in the user project folder with the name of the model
        model_weight_path = os.path.join(self.model_path, model_name + '.pt')

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
        # Deactivate the start button until the user selects an image or folder
        self.ui.Start.setEnabled(False)

        # Connect the addModel button to the function new_model
        self.ui.addModel.clicked.connect(self.new_model)


        ##GLOBAL VARIABLES##

        # User information
        self.userName = None
        self.userSurname = None
        self.userEmail = None

        # Project information
        self.projectName = None
        self.projectPath = None

        # Global variable to store the image or folder path
        self.imagePath = None
        self.folderPath = None

        # Global flag to check if a file or folder has been selected
        self.folderSelected = False
        self.fileSelected = False

        # Create dictionary to store the results for each image
        self.resultsImage = {}

        # Total number of images
        self.totalImages = 0



        # If the preferences.txt file does not exist, open the user information form to ask for user information
        # and save the information in the preferences.txt file

        if not os.path.isfile(preferences_path):     
            # If the preferences.txt file does not exist
            # Wait for 5 seconds before opening a message box to ask for user information when the program is launched
            self.timer = QTimer()
            self.timer.timeout.connect(self.user_info_form)
            self.timer.start(1500)

        else: 
            # If the preferences.txt file exists, read the user information from the file
            with open(preferences_path, 'r') as f:

                # Create an empty dictionary to store the user and project information
                info_dict = {}

                # Loop through the lines in the file
                for line in f.readlines()[:9]:
                    if ': ' in line:
                        x = line.split(': ')
                        info_dict[x[0].strip()] = x[1].strip()
                                                                   
                # Assign values to keys
                self.projectName = info_dict['Project Name']
                self.projectPath = info_dict['Project Folder']   
                self.userName = info_dict['Name']
                self.userSurname = info_dict['Surname']
                self.userEmail = info_dict['Email']

        print(f'User information: {self.userName} {self.userSurname} {self.userEmail}')
        print(f'Project information: {self.projectName} {self.projectPath}')

        # Display the project name and path in the label as soon as the program is launched
        self.ui.ProjectNameDisplay.setText(self.projectName)
        self.ui.ProjectPathDisplay.setText(self.projectPath)

        # Set the project folder path as the current working directory
        # If the app has never been opened, the project path is set to none
        if self.projectPath != None:
            os.chdir(self.projectPath)


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

        # If the user doesn't select a folder, open a message box
        if self.folderPath == '':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("No folder selected")
            msg.setWindowTitle("Warning")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

        # Use open_selected_project function to open the newly created project
        self.open_selected_project()


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
            # If the project name is empty, open a message box
            if project_name == '':
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Project name cannot be empty")
                msg.setWindowTitle("Warning")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return
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
            
            # Use open_selected_project function to open the newly created project
            self.folderPath = project_path
            self.open_selected_project()

            # Close the dialog box
            dialog.close()

        # Connect save button to function
        save_button.clicked.connect(save_project)

        # Show dialog box
        dialog.exec_()
        
    def open_selected_project(self):
        # Set the project name to the selected folder name
        self.projectName = os.path.basename(self.folderPath)

        self.save_to_text_file(self.projectName, self.folderPath)


        # Set the project folder path as the current working directory
        os.chdir(self.folderPath)

        # Display the project name and path in the label
        self.ui.ProjectNameDisplay.setText(self.projectName)
        self.ui.ProjectPathDisplay.setText(self.folderPath)


        
    def save_to_text_file(self, project_name, project_folder):
        
        # Save the project name and folder in the preferences.txt file
        with open(preferences_path, 'r') as f:
            # Read the lines of the file
            lines = f.readlines()

        # Copy the 5 first lines of the file
        new_lines = lines[:5]

        # Write the lines back to the file, updating the project name and folder if it already exists
        
        # Save project to a tuple
        current_project = (project_name, project_folder)
        
        # Create an empty list to store tuples of recent projects
        recent_projects = [current_project]

        for i, line in enumerate(lines):
            if line.startswith('Project Name:'):
                # We've found an existing project, so update its name and folder
                recent_project = (lines[i].strip().split(': ')[1],
                                  lines[i+1].strip().split(': ')[1])
                if recent_project not in recent_projects:
                    recent_projects.append(recent_project)

        # Add the recent projects in the menuBar
        self.ui.RecentProjects.setMenu(QMenu(self.ui.File))
        for project in recent_projects:
            self.ui.RecentProjects.menu().addAction(project[0])
        # Link the recent projects to the open_selected_project function
        self.ui.RecentProjects.menu().triggered.connect(self.open_selected_project)

        with open(preferences_path, 'w') as f:
            new_lines.append('\nCurrent Project:\n')
            new_lines.append(f'Project Name: {project_name}\n')
            new_lines.append(f'Project Folder: {project_folder}\n')
            new_lines.append('\nRecently Opened Projects:\n')
            for cpt, project in enumerate(recent_projects[1:]):
                if cpt == 5:
                    break
                new_lines.append(f'\nProject Name: {project[0]}\n')
                new_lines.append(f'Project Folder: {project[1]}\n')

            f.writelines(new_lines)



    def new_model(self):
        # Create and show the model form
        self.model_form = NewModel()
        self.model_form.show()

        # If the submit button is clicked, add the model name to the combobox
        self.model_form.submit_button.clicked.connect(self.add_model_to_combobox)

    def add_model_to_combobox(self):
        # Get the model name from the model form
        model_name = self.model_form.model_edit.text()
        # Add the model name to the combobox
        self.ui.comboBox.addItem(model_name)
        # Save the model names to the file
        self.save_model_names()
        # Close the model form
        self.model_form.close()

    def save_model_names(self):
        # Get the model names from the combobox
        model_names = [self.ui.comboBox.itemText(i) for i in range(self.ui.comboBox.count())]

        models_file = os.path.join(cwd, 'models', 'model_names.txt')

        # Read the existing model names from the file, if any
        try:
            with open(models_file, 'r') as f:
                existing_model_names = [line.strip() for line in f]
        except FileNotFoundError:
            existing_model_names = []

        # Append the new model names to the existing list of names
        model_names += [name for name in existing_model_names if name not in model_names]

        # Write the model names to a file
        with open(models_file, 'w') as f:
            for model_name in model_names:
                f.write(model_name + '\n')

    def load_model_names(self):
        # Load models to the combobox from the file

        models_file = os.path.join(cwd, 'models', 'model_names.txt')

        # Read the model names from the file
        try:
            with open(models_file, 'r') as f:
                model_names = [line.strip() for line in f]
        except FileNotFoundError:
            model_names = []

        # Add the model names to the combobox if it doen't already exist
        for model_name in model_names:
            if self.ui.comboBox.findText(model_name) == -1:
                self.ui.comboBox.addItem(model_name)


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

        if filepath:
            self.fileSelected = True
            # Load the image and add it to the scene
            pixmap = QtGui.QPixmap(filepath)
            pixmap = pixmap.scaledToWidth(self.ui.image_label.width())
            self.ui.image_label.setFixedSize(pixmap.size())
            self.ui.image_label.setPixmap(pixmap)

        # Activate the start button
        self.ui.Start.setEnabled(True)
    
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

        # Get total number of images in the folder
        self.total_images = len([file for file in os.listdir(folder_path)
                                 if file.endswith((".jpg", ".JPG", "*.jpeg", "*.JPEG", "*.png", "*.PNG", "*.bmp", "*.BMP"))])
                
        # Use of the previous and next buttons to navigate through the images
        self.ui.next.clicked.connect(self.next_image)
        self.ui.previous.clicked.connect(self.previous_image)

        # Activate the start button
        self.ui.Start.setEnabled(True)


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

            self.folderNumber = 1

            # If the default folder is selected and "runs\\detect\\exp" already exists, increment the number of the folder
            if save_dir == os.path.join(os.getcwd(), "runs\\detect\\exp"):
                while os.path.exists(os.path.join(os.getcwd(), f"runs\\detect\\exp{self.folderNumber}")):
                    self.folderNumber += 1
                save_dir = os.path.join(os.getcwd(), f"runs\\detect\\exp{self.folderNumber}")
                results.save(save_dir=save_dir, exist_ok=True) 
            # If a different folder is selected, save the results in the selected folder
            else:
                results.save(save_dir=save_dir, exist_ok=True)

            results.print()

            # Save results to a text file
            with open(os.path.join(save_dir, 'results.txt'), 'w') as save_results_file:
                save_results_file.write('Saved image to ' + save_dir + '\n')
                save_results_file.write('\n')
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
            
            self.folderNumber = 1

            # If the default folder is selected and "runs\\detect\\exp" already exists, increment the number of the folder
            if save_dir == os.path.join(os.getcwd(), "runs\\detect\\exp"):
                while os.path.exists(os.path.join(os.getcwd(), f"runs\\detect\\exp{self.folderNumber}")):
                    self.folderNumber += 1
                save_dir = os.path.join(os.getcwd(), f"runs\\detect\\exp{self.folderNumber}")
                results.save(save_dir=save_dir, exist_ok=True) 
            # If a different folder is selected, save the results in the selected folder
            else:
                results.save(save_dir=save_dir, exist_ok=True)


            # Update progress bar

            # Number of images that have been processed
            #while self.current_num < self.total_images:
            #    self.current_num += 1
            #    self.ui.progressBar.setValue(self.current_num)
            #    self.ui.progressBar.repaint()
            #    self.ui.progressBar.update()
            #    time.sleep(0.01)


            # Print results
            results.print()

            # Save results to a text file
            with open(os.path.join(save_dir, 'results.txt'), 'w') as save_results_file:
                save_results_file.write('Saved ' + str(len(os.listdir(save_dir)) - 1) + ' images to ' + save_dir + '\n')
                save_results_file.write('\n')
                save_results_file.write(str(results))

            
            for number, filename in enumerate(os.listdir(self.folderPath)): # Get the filename in the input folder and the corresponding index
                    if filename.endswith(".jpg") or filename.endswith(".JPG") or filename.endswith(".jpeg") or filename.endswith(".JPEG"):
                        image_path = os.path.join(self.folderPath, filename)

                        # Save results

                        # get class names
                        class_names = model.module.names if hasattr(model, 'module') else model.names
                        class_labels = results.pred[number][:, -1].numpy().astype(int)
                        class_names = [class_names[i] for i in class_labels]

                        # get filename from input image path
                        image_name = os.path.basename(image_path).split('.')[0]
                        
                        # create a pandas dataframe from the tensor
                        results_df = pandas.DataFrame(results.pred[number].cpu().numpy(), columns=['x1', 'y1', 'x2', 'y2', 'confidence', 'class'])
                        results_df['class'] = results_df['class'].astype(int)

                        # save the dataframe to a JSON file
                        results_df.to_json(os.path.join(save_dir, image_name + ".json"), orient="records")


                        # Add the name of the image and the corresponding classes to the resultsImage dictionary
                        self.resultsImage[image_name] = class_names

                        # get extension from input image path
                        image_extension = os.path.splitext(image_path)[1]

                        # get output path of detected image
                        output_path = os.path.join(save_dir, image_name + '_detected' + image_extension)

                        # rename output image according to the name of the input image
                        os.replace(os.path.join(save_dir, "image" + str(number) + ".jpg"), output_path)

            
            # Create directories and subdirectories for the results
            self.create_subdirectories(save_dir)

            # Move the images to the appropriate subdirectories
            pollinator_dir, non_pollinator_dir = self.move_images(save_dir)
            
            self.folderSelected = False
        
        # Select the first image in the 'Multiple Pollinators' folder
        multiple_pollinators_dir = os.path.join(pollinator_dir, "Multiple Pollinators")
        for image in os.listdir(multiple_pollinators_dir):
            if image.endswith(".jpg") or image.endswith(".JPG") or image.endswith(".jpeg") or image.endswith(".JPEG"):
                output_path = os.path.join(multiple_pollinators_dir, image)
                break

        # Display output image
        pixmap = QtGui.QPixmap(output_path)
        pixmap = pixmap.scaledToWidth(self.ui.image_label.width())
        self.ui.image_label.setFixedSize(pixmap.size())
        self.ui.image_label.setPixmap(pixmap)

        self.folderPath = save_dir
        self.imagePath = output_path
        
        # Display the results in the results dictionary
        print(self.resultsImage)

        # Deactivate Start button
        self.ui.Start.setEnabled(False)


    def create_subdirectories(self, save_dir):
        # Create two subdirectories in the selected folder: one for Pollinator images and one for Non-Pollinator images
        self.pollinator_dir = os.path.join(save_dir, "Pollinator")
        self.nonpollinator_dir = os.path.join(save_dir, "Non-Pollinator")
        os.makedirs(self.pollinator_dir, exist_ok=True)
        os.makedirs(self.nonpollinator_dir, exist_ok=True)

        # Inside the Pollinator directory, create subdirectories for each class
        pollinator_classes = set()
        for class_list in self.resultsImage.values():
            pollinator_classes.update(class_list)
        for class_name in pollinator_classes:
            if class_name != 'flower':
                os.makedirs(os.path.join(self.pollinator_dir, class_name), exist_ok=True)
        os.makedirs(os.path.join(self.pollinator_dir, "Multiple Pollinators"), exist_ok=True)

    def move_images(self, save_dir):
    # Move the images to the corresponding subdirectories

        for image_name, class_list in self.resultsImage.items():
            # If the image contains only a flower or nothing detected
            if class_list == ['flower'] or not class_list:
                shutil.move(os.path.join(save_dir, image_name + "_detected.JPG"), os.path.join(self.nonpollinator_dir, image_name + "_detected.JPG"))
                # Also move the corresponding JSON file
                shutil.move(os.path.join(save_dir, image_name + ".json"), os.path.join(self.nonpollinator_dir, image_name + ".json"))

            # If the image contains a single pollinator or a pollinator and one or multiple flowers detected
            elif len(class_list) >= 1 and ('flower' in class_list or len(set(class_list)) == 1):
                # Get the pollinator class
                pollinator_class = None
                for class_name in class_list:
                    if class_name != 'flower':
                        pollinator_class = class_name
                        break
                if pollinator_class is not None:
                    shutil.move(os.path.join(save_dir, image_name + "_detected.JPG"), os.path.join(self.pollinator_dir, pollinator_class, image_name + "_detected.JPG"))
                    # Also move the corresponding JSON file
                    shutil.move(os.path.join(save_dir, image_name + ".json"), os.path.join(self.pollinator_dir, pollinator_class, image_name + ".json"))
                else:
                    # There is a flower but no pollinator class, move to nonpollinator directory
                    shutil.move(os.path.join(save_dir, image_name + "_detected.JPG"), os.path.join(self.nonpollinator_dir, image_name + "_detected.JPG"))
                    # Also move the corresponding JSON file
                    shutil.move(os.path.join(save_dir, image_name + ".json"), os.path.join(self.nonpollinator_dir, image_name + ".json"))

            # If the image contains multiple pollinators
            elif len(class_list) > 1:
                os.makedirs(os.path.join(self.pollinator_dir, "Multiple Pollinators"), exist_ok=True)
                shutil.move(os.path.join(save_dir, image_name + "_detected.JPG"), os.path.join(self.pollinator_dir, "Multiple Pollinators", image_name + "_detected.JPG"))
                # Also move the corresponding JSON file
                shutil.move(os.path.join(save_dir, image_name + ".json"), os.path.join(self.pollinator_dir, "Multiple Pollinators", image_name + ".json"))

        return self.pollinator_dir, self.nonpollinator_dir


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
