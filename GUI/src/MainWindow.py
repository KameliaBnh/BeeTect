# Attributes:
#   - User: User.User()
#   - Project: Project.Project()
#   - Models: Models.Models()
#   - Images: list
#   - cpt_image: int
#   - cpt_image_result: int

# Functions:
#   - __init__(self)
#   - check_preferences(self)
#   - open_selected_project(self, project_name, project_path)
#   - open_project(self)
#   - new_project(self)
#   - add_new_model(self)
#   - load_models(self)
#   - close_model_form(self)
#   - get_image(self)
#   - get_images_from_folder(self, path)
#   - load_image(self)
#   - show_next_image(self)
#   - show_previous_image(self)
#   - show_image(self, image)
#   - show_image_from_folder(self)
#   - load_image_result(self)
#   - show_next_result(self)
#   - show_previous_result(self)
#   - run_detection(self)
#   - export_report(self)


import os
import shutil
import subprocess
import webbrowser
import pandas
import torch

from PySide2.QtGui import QIcon
from PySide2.QtCore import QFile, Qt
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QMainWindow, QMainWindow, QMenu, QFileDialog, QMessageBox, QInputDialog, QPushButton

import Project
import User
import Models
import Image

class MainWindow(QMainWindow):

    def __init__(self):

        # Class attributes
    
        self.User = User.User()
        self.Project = Project.Project()
        self.Models = Models.Models()
        self.Images = []

        self.cpt_image = 0
        self.cpt_image_result = 0

        self.project_results_path = None

        # Call the parent class constructor
        super().__init__()

        # Load the .ui file
        ui_file = QFile(os.path.join(os.getcwd(), "src\\interface.ui"), self)
        ui_file.open(QFile.ReadOnly)

        # Load the .ui file as a widget
        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()
        self.setCentralWidget(self.ui)

        # Set the title of the application
        self.setWindowTitle("Automated Pollinator Monitoring")

        # Set the icon of the application
        self.setWindowIcon(QIcon(os.path.join(os.getcwd(), "resources\\bee.png")))
        
        # Check if the user_info.txt file exists when the application starts
        self.check_preferences()

        # Load models from the models folder in the combobox
        self.load_models()

        # Close the application when the user clicks the close button
        self.ui.Exit.triggered.connect(self.close)
        
        # Connect the button to the function open_project
        self.ui.OpenProject.triggered.connect(self.open_project)
        # Connect the button to the function new_project
        self.ui.NewProject.triggered.connect(self.new_project)

        # Connect the addModel button to the function new_model
        self.ui.addModel.clicked.connect(self.add_new_model)

        # Connect the button to the function close_model_form
        self.Models.submit_button.clicked.connect(self.close_model_form)

        # Connect the button to the function open_image
        self.ui.OpenFile.triggered.connect(self.show_image)
        # Connect the button to the function open_image_folder
        self.ui.OpenFolder.triggered.connect(self.show_image_from_folder)

        # Connect the button to the function on_click
        self.ui.Start.clicked.connect(self.run_detection)
        # Deactivate the 'Start detection' button until the user selects an image or folder
        self.ui.Start.setEnabled(False)

        # Press the button to export the html report 
        self.ui.ExportReport.aboutToShow.connect(self.export_report)

        # Disable the next and previous buttons until the user selects a folder
        self.ui.next.setEnabled(False)
        self.ui.previous.setEnabled(False)

        # Add two buttons to the center of the 'image_frame' QFrame: openImage and openFolder
        self.ui.openImage.clicked.connect(self.show_image)
        self.ui.openFolder.clicked.connect(self.show_image_from_folder)



    def check_preferences(self):
        # Check if the user_info.txt file exists
        if not os.path.isfile(os.path.join(os.getcwd(), 'user_info.txt')):
            self.User.open_user_form()

        else:

            with open(os.path.join(os.getcwd(), 'user_info.txt'), 'r') as file:

                # Create an empty dictionary to store the user information
                info_dict = {}

                for line in file.readlines()[:9]:
                    if ': ' in line:
                        x = line.split(': ')
                        info_dict[x[0].strip()] = x[1].strip()

                # Assign values to the class attributes
                self.User.name = info_dict['Name']
                self.User.surname = info_dict['Surname']
                self.User.email = info_dict['Email']
                self.User.date = info_dict['Date']
                self.Project.name = info_dict['Project Name']
                self.Project.path = info_dict['Project Folder']

            with open(os.path.join(os.getcwd(), 'user_info.txt'), 'r') as file:
                # Create an empty dictionary to store the recent projects information
                recent_projects_dict = {}

                # Create a menu for the recent projects
                self.ui.RecentProjects.setMenu(QMenu(self.ui.File))
                
                # Retrieve recent projects
                lines_recent_projects = file.readlines()[11:]
                for number, line in enumerate(lines_recent_projects):
                    if 'Project Name: ' in line:
                        x1 = line.split(': ')
                        x2 = lines_recent_projects[number + 1].split(': ')
                        recent_projects_dict[x1[1].strip()] = x2[1].strip()

                # Add recent projects to the menu
                for project_name, project_path in recent_projects_dict.items():
                    self.ui.RecentProjects.menu().addAction(project_name)

                    # Link the recent projects to the open_selected_project function
                    #self.ui.RecentProjects.menu().triggered.connect(self.open_selected_project(project_name, project_path))

        print(f'User: {self.User.name} {self.User.surname} {self.User.email} {self.User.date}')
        print(f'Project: {self.Project.name} {self.Project.path}')

        # Display project information
        self.ui.ProjectNameDisplay.setText(self.Project.name)
        self.ui.ProjectPathDisplay.setText(self.Project.path)

    def open_selected_project(self, project_name, project_path):
        # Save project to text file
        self.Project.save_project(project_name, project_path)

    def open_project(self):
        self.Project.open_project()

        # Display project information
        self.ui.ProjectNameDisplay.setText(self.Project.name)
        self.ui.ProjectPathDisplay.setText(self.Project.path)

    def new_project(self):
        self.Project.create_project()

        # Display project information
        self.ui.ProjectNameDisplay.setText(self.Project.name)
        self.ui.ProjectPathDisplay.setText(self.Project.path)

    def add_new_model(self):
        self.Models.open_models_form()

    def load_models(self):
        # Clear the combobox
        self.ui.comboBox.clear()
        for model in self.Models.list:
            self.ui.comboBox.addItem(model)

    def close_model_form(self):
        self.Models.close_models_form()
        # Refresh the combobox
        self.load_models()

    def get_image(self):
        # Disable the next and previous buttons until the user selects a folder
        self.ui.next.setEnabled(False)
        self.ui.previous.setEnabled(False)
        
        # Set the window as modal
        self.setWindowModality(Qt.ApplicationModal)

        self.Images.clear()
        image_path = QFileDialog.getOpenFileName(self, 'Open Image', os.getcwd(), 'Image Files (*.jpg *.jpeg *.png *.bmp)')[0]
        self.Images.append(Image.Image(image_path))
    
    def get_images_from_folder(self):
        self.Images.clear()

        # Set the window as modal
        self.setWindowModality(Qt.ApplicationModal)

        folder_path = QFileDialog.getExistingDirectory(self, 'Open Folder', os.getcwd(), QFileDialog.ShowDirsOnly)
        for root, dirs, file in os.walk(folder_path):
            for image in file:
                if image.lower().endswith('.jpg') or image.lower().endswith('.jpeg') or image.lower().endswith('.png') or image.lower().endswith('.bmp'):
                    self.Images.append(Image.Image(os.path.join(root, image)))
        
    def load_image(self, image):
        image.pixmap.scaledToHeight(self.ui.image_label.height())
        self.ui.image_label.setPixmap(image.pixmap)

        self.ui.Start.setEnabled(True)

    def show_next_image(self):
        self.cpt_image += 1
        self.load_image(self.Images[self.cpt_image % len(self.Images)])

    def show_previous_image(self):
        self.cpt_image -= 1
        self.load_image(self.Images[self.cpt_image % len(self.Images)])

    def show_image(self):
        self.get_image()
        self.load_image(self.Images[0])
        
        # Delete the two buttons when the user selects an image or folder
        self.ui.openImage.hide()
        self.ui.openFolder.hide()

    def show_image_from_folder(self):
        # Enable the previous and next buttons
        self.ui.next.setEnabled(True)
        self.ui.previous.setEnabled(True)

        self.get_images_from_folder()
        self.load_image(self.Images[0])

        # Set next and previous buttons to navigate through the images
        self.ui.next.clicked.connect(self.show_next_image)
        self.ui.previous.clicked.connect(self.show_previous_image)

        # Delete the two buttons when the user selects an image or folder
        self.ui.openImage.hide()
        self.ui.openFolder.hide()

    def load_image_result(self, image):
        image.pixmap_result.scaledToHeight(self.ui.image_label.height())
        self.ui.image_label.setPixmap(image.pixmap_result)

        self.ui.Start.setEnabled(True)

    def show_next_result(self):
        self.cpt_image_result += 1
        self.load_image_result(self.Images[self.cpt_image % len(self.Images)])

    def show_previous_result(self):
        self.cpt_image_result -= 1
        self.load_image_result(self.Images[self.cpt_image % len(self.Images)])

    def create_subdirectories(self, folder_path, image):
        # Create two 'Pollinator' and 'Non-Pollinator' folders
        os.makedirs(os.path.join(folder_path, "Pollinator"), exist_ok=True)
        os.makedirs(os.path.join(folder_path, "Non-Pollinator"), exist_ok=True)

        # Create subfolders in the 'Pollinator' folder for each detected class
        for detected_class in image.class_name:
            if detected_class != 'flower':
                os.makedirs(os.path.join(folder_path, "Pollinator", detected_class), exist_ok=True)

        # Create one subfolder for images containing multiple pollinators
        os.makedirs(os.path.join(folder_path, "Pollinator", "Multiple-Pollinators"), exist_ok=True)

    def run_detection(self):
        model_path = os.path.join(self.Models.path, self.ui.comboBox.currentText() + '.pt')
        
        # Set the window as modal
        self.setWindowModality(Qt.ApplicationModal)

        # Let the user choose whether to save the results in the default subfolder of the current project or in a renamed subfolder
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Save Results")
        msg.setInformativeText("Do you want to save the results in the default folder or do you want to select a different one? Default folder: runs\\detect\\exp")
        msg.setWindowTitle("Save Results")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.button(QMessageBox.Ok).setText('Default Folder')
        msg.button(QMessageBox.Cancel).setText('Select Folder')

        # If the user selects the custom folder option, let him write the name of the folder
        if msg.exec_() == QMessageBox.Cancel:
            folder_name = QInputDialog.getText(self, 'Folder Name', 'Enter the name of the folder')[0]
            self.project_results_path = os.path.join(self.Project.path, folder_name)
            if os.path.exists(self.project_results_path):
                shutil.rmtree(self.project_results_path)
            os.makedirs(self.project_results_path)

        # If the user selects the default folder option, create the folder if it doesn't exist
        else:
            folder_number = 1
            self.project_results_path = os.path.join(self.Project.path, os.path.join('runs', 'detect', 'exp'))
            while os.path.exists(self.project_results_path + str(folder_number)):
                folder_number += 1
            self.project_results_path = self.project_results_path + str(folder_number)
            os.makedirs(self.project_results_path)

        # Run the detection
        model = torch.hub.load('ultralytics/yolov5', 'custom', model_path) # load model
        model.conf = 0.5 # confidence threshold

        results = model([im.image_cv for im in self.Images]) # inference

        # Save the results
        results.save(save_dir=self.project_results_path, exist_ok=True)
        
        # Display the results
        results.print()

        # Rename the images in the folder
        #for image, file in zip(self.Images, os.listdir(folder_path)):
        for i in range(len(self.Images)):
            # Set the new path of the image
            self.Images[i].new_path_result(self.project_results_path)
            file = os.path.join(self.project_results_path, "image" + str(i) + ".jpg")
            if file.lower().endswith('.jpg') or file.lower().endswith('.jpeg') or file.lower().endswith('.png') or file.lower().endswith('.bmp'):
                os.replace(os.path.join(self.project_results_path, file), self.Images[i].path_result)

        # Save results to text file
        with open(os.path.join(self.project_results_path, 'results.txt'), 'w') as save_results_file:
            save_results_file.write('Saved ' + str(len(self.Images)) + ' images to ' + self.project_results_path + '\n')
            save_results_file.write('\n')
            save_results_file.write(str(results))

        class_names = model.module.names if hasattr(model, 'module') else model.names

        for i, image in enumerate(self.Images):
            # Store class names in image object
            # get class names
            class_labels = results.pred[i][:, -1].numpy().astype(int)
            class_names_i = [class_names[j] for j in class_labels]

            # store in image object
            image.store_class_name(class_names_i)

            # Dataframe to JSON
            # create a pandas dataframe from the tensor
            results_df = pandas.DataFrame(results.pred[i].cpu().numpy(), columns=['x1', 'y1', 'x2', 'y2', 'confidence', 'class'])
            results_df['class'] = results_df['class'].astype(int)

            # save the dataframe to a JSON file
            results_df.to_json(image.json_result_path, orient="records")

            # Create a pixmap from the result image    
            image.new_pixmap_result(image.path_result)

            # Create subdirectories
            self.create_subdirectories(self.project_results_path, image)

            # Move images to subfolders according to their classes
            try:
                shutil.move(image.path_result, os.path.join(self.project_results_path, image.class_folder_name, image.name_result))
                # Also move the corresponding JSON file
                shutil.move(image.json_result_path, os.path.join(self.project_results_path, image.class_folder_name, os.path.basename(image.json_result_path)))
            except Exception as e:
                # Message box to inform the user of the error
                QMessageBox.warning(self, 'Error', f'Error moving the images to their subfolders: {str(e)}', QMessageBox.Ok)

        # Display results images
        self.load_image_result(self.Images[0])

        # Enable the previous and next buttons
        self.ui.next.setEnabled(True)
        self.ui.previous.setEnabled(True)

        # Set next and previous buttons to navigate through the results
        self.ui.next.clicked.connect(self.show_next_result)
        self.ui.previous.clicked.connect(self.show_previous_result)


    def export_report(self):

        # get the path to the directory containing this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        print(script_dir)

        # construct the path to the notebook
        notebook_path = os.path.join(script_dir, 'stats.ipynb')
        print(notebook_path)
        
        # Call nbconvert to convert the notebook to HTML
        subprocess.run(['jupyter', 'nbconvert', '--execute',  "--no-input",'--to', 'html', notebook_path])
        shutil.move(os.path.join(script_dir, 'stats.html'), self.project_results_path)
        webbrowser.open(f'file://{self.project_results_path}/stats.html')