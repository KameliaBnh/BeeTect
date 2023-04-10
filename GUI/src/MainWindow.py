import os
import shutil
import subprocess
import webbrowser
import pandas
import torch

from PySide2.QtGui import QIcon, QFont, QPixmap
from PySide2.QtCore import QFile, Qt
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QMainWindow, QMainWindow, QMenu, QFileDialog, QMessageBox, QInputDialog, QPushButton, QDialog, QLineEdit, QVBoxLayout, QLabel, QTableWidget, QHeaderView, QTableWidgetItem, QAction, QAbstractItemView, QListView, QTreeView

import Project
import User
import Models
import Image
import Batch
from HelpWindow import HelpWindow

class MainWindow(QMainWindow):

    def __init__(self):
        """
        Constructor of the MainWindow class.
        It creates the main window of the application using the 'interface.ui' file.
        It also creates the User, Models, Images, Projects and Batches objects.
        """

        # Class attributes
    
        self.User = User.User()
        self.Models = Models.Models()

        # Create an empty list to store the images
        self.Images = []

        self.cpt_image = 0
        self.cpt_image_result = 0

        results_path = os.path.join(os.getcwd(), "projects")
        
        # If the projects folder doesn't exist, create it
        if not os.path.exists(results_path):
            os.makedirs(results_path)

        # Create a list of Project objects
        self.Projects = [Project.Project(os.path.join(results_path, dir)) for dir in os.listdir(results_path) if os.path.isdir(os.path.join(results_path, dir))]

        # Create a list of Batch objects
        if len(self.Projects) > 0:
            if os.path.exists(os.path.join(self.Projects[0].path, "batches.txt")):
                # Fill the self.Batches list with the batches written in the batches.txt file
                with open(os.path.join(self.Projects[0].path, "batches.txt"), "r") as batches_file:
                    self.Batches = [Batch.Batch(batch) for batch in batches_file.read().splitlines()]

        else:
            self.Batches = []

        self.batch_results = []

        # If the selected_batches.txt file exists, fill the self.batches_results list
        if os.path.exists(os.path.join(os.getcwd(), "selected_batches.txt")):
            with open(os.path.join(os.getcwd(), "selected_batches.txt"), "r") as save_results_file:
                self.batch_results = save_results_file.read().splitlines()

        # Call the parent class constructor
        super().__init__()

        # Load the .ui file
        ui_file = QFile(os.path.join(os.getcwd(), "interface.ui"), self)
        ui_file.open(QFile.ReadOnly)

        # Load the .ui file as a widget
        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()
        self.setCentralWidget(self.ui)

        # Set the title of the application
        self.setWindowTitle("BeeTect")

        # Set the icon of the application
        self.setWindowIcon(QIcon(os.path.join(os.getcwd(), "resources/bee.png")))
        
        # Check if the user_info.txt file exists when the application starts
        self.check_flag = False
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

        # Connect the editModels button to the function edit_models
        self.ui.editModels.clicked.connect(self.edit_models)

        # Connect the button to the function close_model_form
        self.Models.submit_button.clicked.connect(self.close_model_form)

        # Deactivate the OpenFile and OpenFolder buttons until the user selects a project
        if self.ui.ProjectNameDisplay.text() == "":
            self.ui.OpenFile.setEnabled(False)
            self.ui.OpenFolder.setEnabled(False)

        # Connect the button to the function open_image
        self.ui.OpenFile.triggered.connect(self.show_image)
        # Connect the button to the function open_image_folder
        self.ui.OpenFolder.triggered.connect(self.show_image_from_folder)

        # Connect the button to the function export_batch_report
        self.ui.ExportBatchRep.triggered.connect(self.export_batch_report)

        # Connect the button to the function select_project_results_folder
        self.ui.SelectFolder.clicked.connect(self.select_project_results_folder)
        # Connect the button to the function on_click
        self.ui.Start.clicked.connect(self.run_detection)
        # Deactivate the 'Start detection' button until the user selects an image or folder
        self.ui.Start.setEnabled(False)

        # Connect the button to the function open_app_help
        self.ui.OpenAppHelp.triggered.connect(self.open_app_help)

        # Disable the next and previous buttons until the user selects a folder
        self.ui.next.setEnabled(False)
        self.ui.previous.setEnabled(False)

        # Add two buttons to the center of the 'image_frame' QFrame: openImage and openFolder
        self.ui.openImage.clicked.connect(self.show_image)
        self.ui.openFolder.clicked.connect(self.show_image_from_folder)

        # Retrieve the 5 most recent projects from the self.Projects list
        recent_projects_dict = {}

        # Create a menu for the recent projects
        self.ui.RecentProjects.setMenu(QMenu(self.ui.File))

        # If there are less than 5 projects, add all the projects to the menu
        if len(self.Projects) < 5:
            for project in self.Projects:
                recent_projects_dict[project.name] = project.path
        
        else:
            # Add the 5 most recent projects to the dictionary
            for i in range(5):
                recent_projects_dict[self.Projects[i].name] = self.Projects[i].path

        # Add recent projects to the menu
        for project_name, project_path in recent_projects_dict.items():

            action = QAction(project_name, self)
            self.ui.RecentProjects.menu().addAction(action)

        # Get the name of the item that was clicked in the menu
        self.ui.RecentProjects.menu().triggered.connect(lambda triggered_action: self.open_selected_project(triggered_action.text()))

    def check_preferences(self):
        """
        Check if the user_info.txt file exists.
        If it doesn't, open the user form. If it does, retrieve the user information.
        """

        if not self.check_flag:
            # Check if the user_info.txt file exists
            if not os.path.isfile(os.path.join(os.getcwd(), 'user_info.txt')):
                self.User.open_user_form()
                print("Getting user information...")

            else:

                print("Retrieving user information...")
                with open(os.path.join(os.getcwd(), 'user_info.txt'), 'r') as file:

                    # Create an empty dictionary to store the user information
                    info_dict = {}

                    for line in file.readlines()[:10]:
                        if ': ' in line:
                            x = line.split(': ')
                            info_dict[x[0].strip()] = x[1].strip()

                    # Assign values to the class attributes
                    self.User.name = info_dict['Name']
                    self.User.surname = info_dict['Surname']
                    self.User.email = info_dict['Email']
                    self.User.date = info_dict['Date']
                    self.User.time = info_dict['Time']

                    # Check if the user has selected a project
                    if 'Project Folder' in info_dict.keys():
                        # Insert the current Project in the self.Projects list
                        if info_dict['Project Folder'] not in [project.path for project in self.Projects]:
                            # Add the project to the top of the list
                            self.Projects.insert(0, Project.Project(info_dict['Project Folder']))
                        else:
                            # Move the project to the top of the list
                            self.Projects.insert(0, self.Projects[[project.path for project in self.Projects].index(info_dict['Project Folder'])])

            # Set the flag to True
            self.check_flag = True

        if len(self.Projects) != 0:
            # Display project information
            self.ui.ProjectNameDisplay.setText(self.Projects[0].name)
            self.ui.ProjectPathDisplay.setText(self.Projects[0].path)

            print("Current Project: " + self.Projects[0].name)

    # Save the project to text file
    def write_project_to_text_file(self, name, path):
        """
        Save the current project information to the 'user_info.txt' file.
        """

        print("Saving project information to user_info.txt file...")

        # Open 'user_info.txt' file
        with open(os.path.join(os.getcwd(), 'user_info.txt'), 'r') as file:
            # Read the file
            lines = file.readlines()

        # Copy the 6 first lines of the file
        new_lines = lines[:6]

        ## Write lines back to the file, updating the project name and path if necessary

        # Save current project to a tuple
        current_project = (name, path)

        # Create an empty list to store tuples of recent projects
        recent_projects = [current_project]

        for i, line in enumerate(lines):
            if line.startswith('Project Name:'):
                recent_project = (lines[i].strip().split(': ')[1],
                                  lines[i+1].strip().split(': ')[1])
                if recent_project not in recent_projects:
                    recent_projects.append(recent_project)
        
        # Write the project name and path to the file
        with open(os.path.join(os.getcwd(), 'user_info.txt'), 'w') as file:
            new_lines.append('\nCurrent Project:\n')
            new_lines.append(f'Project Name: {name}\n')
            new_lines.append(f'Project Folder: {path}\n')
            new_lines.append('\nRecently Opened Projects:\n')
            for cpt, project in enumerate(recent_projects[1:]):
                if cpt == 5:
                    break
                new_lines.append(f'\nProject Name: {project[0]}\n')
                new_lines.append(f'Project Folder: {project[1]}\n')
            
            file.writelines(new_lines)

    def open_selected_project(self, project_name):
        """
        Open the selected project.
        Move the project to the top of the list of projects. Save the project to the 'user_info.txt' file.    
        """

        # Get the project from the list of projects
        project = next((p for p in self.Projects if p.name == project_name), None)
        if project is None:
            QMessageBox.warning(self, 'Error', f"Project '{project_name}' not found in list of projects.")
            return
        
        # Move the project to the top of the list
        self.Projects.insert(0, self.Projects.pop(self.Projects.index(project)))

        print("Opening project: " + self.Projects[0].name)

        # Save project to text file
        self.write_project_to_text_file(self.Projects[0].name, self.Projects[0].path)

        self.Batches.clear()
        self.Batches = [Batch.Batch(os.path.join(self.Projects[0].path, dir)) for dir in os.listdir(self.Projects[0].path) if os.path.isdir(os.path.join(self.Projects[0].path, dir))]

        # Write the Batches to a text file
        with open(os.path.join(self.Projects[0].path, 'batches.txt'), 'w') as file:
            for batch in self.Batches:
                file.write(batch.path + '\n')

        # Display project information
        self.ui.ProjectNameDisplay.setText(self.Projects[0].name)
        self.ui.ProjectPathDisplay.setText(self.Projects[0].path)

        # Enable the OpenFile and OpenFolder buttons
        self.ui.OpenFile.setEnabled(True)
        self.ui.OpenFolder.setEnabled(True)

    def open_project(self):
        """
        Open a project. Add the project to the top of the list of projects. Save the project to the 'user_info.txt' file.
        """

        # Set the window as modal
        self.setWindowModality(Qt.ApplicationModal)

        try:
            # Open the project
            project_path = QFileDialog.getExistingDirectory(self, "Open Project", os.path.join(os.getcwd(), 'projects'))
            if project_path not in [project.path for project in self.Projects]:
                # Add the project to the top of the list
                self.Projects.insert(0, Project.Project(project_path))
            else:
                # Move the project to the top of the list
                self.Projects.insert(0, self.Projects[[project.path for project in self.Projects].index(project_path)])

            print("Opening project: " + self.Projects[0].name)

        except Exception as e:
            # Open message box
            QMessageBox.warning(self, 'Error', f'Error opening project: {str(e)}', QMessageBox.Ok)
            return
        
        else:
            print("Project opened successfully!")

            # Update the project last modification date
            self.Projects[0].update_last_modification_date()

            # Save project to text file
            self.write_project_to_text_file(self.Projects[0].name, project_path)

            if self.Batches:
                self.Batches.clear()
                
            self.Batches = [Batch.Batch(os.path.join(self.Projects[0].path, dir)) for dir in os.listdir(self.Projects[0].path) if os.path.isdir(os.path.join(self.Projects[0].path, dir))]

            # Write the Batches to a text file
            with open(os.path.join(self.Projects[0].path, 'batches.txt'), 'w') as file:
                for batch in self.Batches:
                    file.write(batch.path + '\n')

        # Display project information
        self.ui.ProjectNameDisplay.setText(self.Projects[0].name)
        self.ui.ProjectPathDisplay.setText(self.Projects[0].path)

        # Enable the OpenFile and OpenFolder buttons
        self.ui.OpenFile.setEnabled(True)
        self.ui.OpenFolder.setEnabled(True)

        # Disable start button
        self.ui.Start.setEnabled(False)

    # Open a file dialog to select the project directory
    def open_project_directory(self, project_directory_edit):
        """
        Open a file dialog to select the project directory.
        """

        # Set the window as modal
        self.setWindowModality(Qt.ApplicationModal)

        try:
            # Open the project directory
            project_directory = QFileDialog.getExistingDirectory(self, "Select Project Directory", os.getcwd())

            print("Selecting project directory...")

        except Exception as e:
            # Open message box
            QMessageBox.warning(self, 'Error', f'Error opening project directory: {str(e)}', QMessageBox.Ok)
            return
        
        else:
            # Set the project directory
            project_directory_edit.setText(project_directory)

            print(project_directory + " selected successfully!")

    # Save the new project
    def save_new_project(self, project_name_edit, project_directory_edit):
        """
        Save the new project. Add the project to the top of the list of projects. Save the project to the 'user_info.txt' file.
        """
            
        try:

            print("Creating project: " + project_name_edit.text())

            # Add the project to the list of projects
            new_project_path = os.path.join(project_directory_edit.text(), project_name_edit.text())
            if new_project_path not in [project.path for project in self.Projects]:
                # Create the project directory
                os.mkdir(new_project_path)
                # Add the project to the top of the list
                self.Projects.insert(0, Project.Project(new_project_path))
            else:
                # Move the project to the top of the list
                self.Projects.insert(0, self.Projects[[project.path for project in self.Projects].index(new_project_path)])

                self.Batches.clear()
                self.Batches = [Batch.Batch(os.path.join(self.Projects[0].path, dir)) for dir in os.listdir(self.Projects[0].path) if os.path.isdir(os.path.join(self.Projects[0].path, dir))]

        except Exception as e:
            # Open message box
            QMessageBox.warning(self, 'Error', f'Error saving project: {str(e)}', QMessageBox.Ok)
            return
        
        else:
            # Open message box
            QMessageBox.information(self, 'Success', 'Project successfully created', QMessageBox.Ok)

            print("Project successfully created!")

    def new_project(self):
        """
        Create a new project.
        """
        
        # Open a file dialog to select the project name and directory
        dialog = QDialog()
        dialog.setWindowTitle('Create New Project')
        dialog.setModal(True)
        dialog.setFixedSize(500, 300)
        layout = QVBoxLayout(dialog)

        # Set the font
        font = QFont()
        font.setPointSize(8)

        # Add window icon
        dialog.setWindowIcon(QIcon(QPixmap(os.path.join(os.getcwd(), 'resources', 'newProject.png'))))

        # Create a label and line edit for the project name
        project_name_label = QLabel('Project name:')
        project_name_label.setFont(font)
        project_name_edit = QLineEdit()
        project_name_edit.setFont(font)
        project_name_edit.setPlaceholderText('Required')
        project_name_edit.setFont(font)

        # Create a label and line edit for the project directory
        project_directory_label = QLabel('Project directory:')
        project_directory_label.setFont(font)
        project_directory_edit = QLineEdit()
        project_directory_edit.setFont(font)
        project_directory_edit.setReadOnly(True)
        project_directory_button = QPushButton('Browse')
        project_directory_button.setFont(font)
        project_directory_button.clicked.connect(lambda: self.open_project_directory(project_directory_edit))

        # Create a submit button
        submit_button = QPushButton('Submit')
        submit_button.setFont(font)
        submit_button.clicked.connect(lambda: self.save_new_project(project_name_edit, project_directory_edit))

        # Add the widgets to the layout
        layout.addWidget(project_name_label)
        layout.addWidget(project_name_edit)
        layout.addWidget(project_directory_label)
        layout.addWidget(project_directory_edit)
        layout.addWidget(project_directory_button)
        layout.addWidget(submit_button)

        # Show the dialog
        dialog.exec_()

        print("Creating new project...")

        # Save project to text file
        self.write_project_to_text_file(self.Projects[0].name, self.Projects[0].path)

        # Close the dialog when the submit button is clicked
        dialog.close()

        # Display project information
        self.ui.ProjectNameDisplay.setText(self.Projects[0].name)
        self.ui.ProjectPathDisplay.setText(self.Projects[0].path)

        # Enable the OpenFile and OpenFolder buttons
        self.ui.OpenFile.setEnabled(True)
        self.ui.OpenFolder.setEnabled(True)

        # Disable start button
        self.ui.Start.setEnabled(False)

    def add_new_model(self):
        """
        Add a new model to the list of models.
        Open a window to add a new model.
        """

        self.Models.open_models_form()

        print("Adding new model...")

    def load_models(self):
        """
        Load the models in the combobox.
        """

        # Clear the combobox
        self.ui.comboBox.clear()
        for model in self.Models.list:
            self.ui.comboBox.addItem(model)

    def close_model_form(self):
        """
        Close the model form. Refresh the combobox.
        """

        self.Models.close_models_form()
        # Refresh the combobox
        self.load_models()

    def edit_models(self):
        """
        Open a window to edit the models. Allow the user to add, remove, and edit models.
        """

        print("Editing models...")

        # Open a window displaying the models in a table
        window = QDialog()
        window.setWindowTitle('Edit Models')
        window.setModal(True)
        window.setFixedSize(500, 300)
        layout = QVBoxLayout(window)
        
        # Add window icon
        window.setWindowIcon(QIcon(QPixmap(os.path.join(os.getcwd(), 'resources', 'editModel.png'))))

        # Set the font
        font = QFont()
        font.setPointSize(8)

        # Create a table widget
        table = QTableWidget()
        table.setRowCount(len(self.Models.list))
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(['Model', 'Path'])
        # Set the resize mode of the header to allow for resizing of columns
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        table.verticalHeader().setVisible(False)
        table.setFont(font)

        # Add the models to the table
        for i, model in enumerate(self.Models.list):
            table.setItem(i, 0, QTableWidgetItem(model))
            table.setItem(i, 1, QTableWidgetItem(os.path.join(self.Models.path, self.Models.list[i], self.Models.list[i] + '.pt')))

        # Create a button to add a new model
        add_model_button = QPushButton('Add Model')
        add_model_button.setFont(font)
        add_model_button.clicked.connect(self.add_new_model)

        # Create a button to remove a model
        remove_model_button = QPushButton('Remove Model')
        remove_model_button.setFont(font)
        remove_model_button.clicked.connect(lambda: self.remove_model(table))

        # Create a button to close the window
        close_button = QPushButton('Close')
        close_button.setFont(font)
        close_button.clicked.connect(window.close)

        # Add the widgets to the layout
        layout.addWidget(table)
        layout.addWidget(add_model_button)
        layout.addWidget(remove_model_button)
        layout.addWidget(close_button)

        # Show the window
        window.exec_()

        # Refresh the combobox
        self.load_models()

    def remove_model(self, table):
        """
        Remove a model from the list of models.
        """

        # Get the selected row
        selected_row = table.currentRow()

        # Check that the selected row is a valid index
        if selected_row < 0 or selected_row >= len(self.Models.list):
            return
        
        # Ask the user to confirm the deletion
        confirmation = QMessageBox.question(
            self, 'Confirm Deletion', 'Are you sure you want to delete the selected model?', 
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if confirmation == QMessageBox.Yes:

            print("Deleting " + self.Models.list[selected_row] + " model...")

            # Remove the model from the list
            model_name = self.Models.list[selected_row]
            self.Models.list.pop(selected_row)

            # Remove the model from the table
            table.removeRow(selected_row)
            
            # Delete the model and the model folder from the models folder
            model_path = os.path.join(self.Models.path, model_name, model_name)
            if os.path.exists(model_path):
                shutil.rmtree(model_path)
            model_file = os.path.join(self.Models.path, model_name, model_name + '.pt')
            if os.path.exists(model_file):
                os.remove(model_file)

            # Refresh the combobox
            self.load_models()

    def get_image(self):
        """
        Open a dialog to select an image. Add the image to the list of images.
        """

        print("Loading image...")

        # Disable the next and previous buttons until the user selects a folder
        self.ui.next.setEnabled(False)
        self.ui.previous.setEnabled(False)
        
        # Set the window as modal
        self.setWindowModality(Qt.ApplicationModal)

        self.Images.clear()
        image_path = QFileDialog.getOpenFileName(self, 'Open Image', os.getcwd(), 'Image Files (*.jpg *.jpeg *.png *.bmp)')[0]
        self.Images.append(Image.Image(image_path))
    
    def get_images_from_folder(self):
        """
        Open a dialog to select a folder of images. Add the images in the folder to the list of images.
        """

        print("Loading images from folder...")

        self.Images.clear()

        # Set the window as modal
        self.setWindowModality(Qt.ApplicationModal)

        folder_path = QFileDialog.getExistingDirectory(self, 'Open Folder', os.getcwd(), QFileDialog.ShowDirsOnly)
        for root, dirs, file in os.walk(folder_path):
            for image in file:
                if image.lower().endswith('.jpg') or image.lower().endswith('.jpeg') or image.lower().endswith('.png') or image.lower().endswith('.bmp'):
                    self.Images.append(Image.Image(os.path.join(root, image)))
        
    def load_image(self, image):
        """
        Load an image into the image label.
        """

        image.pixmap.scaledToHeight(self.ui.image_label.height())
        self.ui.image_label.setPixmap(image.pixmap)

    def show_next_image(self):
        """
        Show the next image in the list of images.
        """
        
        self.cpt_image += 1
        self.load_image(self.Images[self.cpt_image % len(self.Images)])

    def show_previous_image(self):
        """
        Show the previous image in the list of images.
        """

        self.cpt_image -= 1
        self.load_image(self.Images[self.cpt_image % len(self.Images)])

    def show_image(self):
        """ 
        Show the image selected by the user.
        """

        self.get_image()
        self.load_image(self.Images[0])
        
        # Delete the two buttons when the user selects an image or folder
        self.ui.openImage.hide()
        self.ui.openFolder.hide()

    def show_image_from_folder(self):
        """
        Show the images in the folder selected by the user.
        """

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
        """
        Load an image after detection into the image label.
        """

        image.pixmap_result.scaledToHeight(self.ui.image_label.height())
        self.ui.image_label.setPixmap(image.pixmap_result)

        self.ui.Start.setEnabled(True)

    def show_next_result(self):
        """
        Show the next image in the list of imagesafter detection.
        """

        self.cpt_image_result += 1
        self.load_image_result(self.Images[self.cpt_image % len(self.Images)])

    def show_previous_result(self):
        """
        Show the previous image in the list of images after detection.
        """

        self.cpt_image_result -= 1
        self.load_image_result(self.Images[self.cpt_image % len(self.Images)])

    def create_subdirectories(self, folder_path, image):
        """
        Create subdirectories for the images after detection. 
        One subdirectory for images with pollinators and one subdirectory for images without pollinators.
        One subdirectory for each detected class and one subdirectory for images containing multiple pollinators.
        """

        # Create two 'Pollinator' and 'Non-Pollinator' folders
        os.makedirs(os.path.join(folder_path, "Pollinator"), exist_ok=True)
        os.makedirs(os.path.join(folder_path, "Non-Pollinator"), exist_ok=True)

        # Create subfolders in the 'Pollinator' folder for each detected class
        for detected_class in image.class_name:
            if detected_class != 'flower':
                os.makedirs(os.path.join(folder_path, "Pollinator", detected_class), exist_ok=True)

        # Create one subfolder for images containing multiple pollinators
        os.makedirs(os.path.join(folder_path, "Pollinator", "Multiple-Pollinators"), exist_ok=True)

    def select_project_results_folder(self):
        """
        Open a dialog to select the folder where the results will be saved.
        The folder is created if it does not exist. It can be either the default subfolder of the current project or a renamed subfolder.
        """

        # Set the window as modal
        self.setWindowModality(Qt.ApplicationModal)

        # Let the user choose whether to save the results in the default subfolder of the current project or in a renamed subfolder
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Save Results")
        msg.setInformativeText("Do you want to save the results in the default folder or do you want to select a different one?")
        msg.setWindowTitle("Save Results")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.button(QMessageBox.Ok).setText('Default Folder')
        msg.button(QMessageBox.Cancel).setText('Select Folder')
        msg.setWindowIcon(QIcon(QPixmap(os.path.join(os.getcwd(), 'resources', 'select.png'))))

        # If the user selects the custom folder option, let him write the name of the folder
        if msg.exec_() == QMessageBox.Cancel:

            print("Saving results in a custom folder...")

            # Set the window as modal
            self.setWindowModality(Qt.ApplicationModal)

            folder_name = QInputDialog.getText(self, 'Folder Name', 'Enter the name of the folder')[0]
            folder_path = os.path.join(self.Projects[0].path, folder_name)                

            if folder_path not in [batch.path for batch in self.Batches]:
                os.makedirs(folder_path)
                # Add the batch to the top of the list
                self.Batches.insert(0, Batch.Batch(folder_path))

                # Write the Batches to a text file
                with open(os.path.join(self.Projects[0].path, 'batches.txt'), 'w') as file:
                    for batch in self.Batches:
                        file.write(batch.path + '\n')
                
            else:
                shutil.rmtree(folder_path)
                # Move the batch to the top of the list
                self.Batches.insert(0, self.Batches[[batch.path for batch in self.Batches].index(folder_path)])

                # Write the Batches to a text file
                with open(os.path.join(self.Projects[0].path, 'batches.txt'), 'w') as file:
                    for batch in self.Batches:
                        file.write(batch.path + '\n')

        # If the user selects the default folder option, create the folder if it doesn't exist
        else:

            print("Saving results in the default folder...")

            folder_number = 1
            folder_path = os.path.join(self.Projects[0].path, os.path.join('exp'))
            while os.path.exists(folder_path + str(folder_number)):
                folder_number += 1
            folder_path = folder_path + str(folder_number)

            if folder_path not in [batch.path for batch in self.Batches]:
                os.makedirs(folder_path)
                # Add the batch to the top of the list
                self.Batches.insert(0, Batch.Batch(folder_path))
                
                # Write the Batches to a text file
                with open(os.path.join(self.Projects[0].path, 'batches.txt'), 'w') as file:
                    for batch in self.Batches:
                        file.write(batch.path + '\n')

            else:
                shutil.rmtree(folder_path)
                # Move the batch to the top of the list
                self.Batches.insert(0, self.Batches[[batch.path for batch in self.Batches].index(folder_path)])

                # Write the Batches to a text file
                with open(os.path.join(self.Projects[0].path, 'batches.txt'), 'w') as file:
                    for batch in self.Batches:
                        file.write(batch.path + '\n')

        print(self.Batches[0].path)
        # Display the folder path in the BatchFolder label
        self.ui.BatchFolder.setText("Batch Folder: " + self.Batches[0].name)

        # Enable the Start button
        self.ui.Start.setEnabled(True)

    def run_detection(self):
        """
        Run the detection on the images in the current batch.
        Results are saved in the folder selected by the user.
        Results are displayed in the image label and also saved in the Images list.
        The images are renamed after their original name.
        """

        model_path = os.path.join(self.Models.path, self.ui.comboBox.currentText(), self.ui.comboBox.currentText() + '.pt')

        print("Yolo Model selected: " + os.path.basename(model_path))

        # Select the folder where the results will be saved
        batch_folder = self.Batches[0].path

        # Run the detection
        model = torch.hub.load('ultralytics/yolov5', 'custom', model_path) # load model
        model.conf = 0.5 # confidence threshold

        results = model([im.image_cv for im in self.Images]) # inference

        # Save the results
        results.save(save_dir=batch_folder, exist_ok=True)
        
        # Display the results
        results.print()

        # Rename the images in the folder
        print("Renaming images...")
        for i in range(len(self.Images)):
            # Set the new path of the image
            self.Images[i].new_path_result(batch_folder)
            file = os.path.join(batch_folder, "image" + str(i) + ".jpg")
            if file.lower().endswith('.jpg') or file.lower().endswith('.jpeg') or file.lower().endswith('.png') or file.lower().endswith('.bmp'):
                os.replace(os.path.join(batch_folder, file), self.Images[i].path_result)

        # Save results to text file
        print("Saving results to text file...")
        with open(os.path.join(batch_folder, 'results.txt'), 'w') as save_results_file:
            save_results_file.write('Saved ' + str(len(self.Images)) + ' images to ' + batch_folder + '\n')
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
            self.create_subdirectories(batch_folder, image)

            # Move images to subfolders according to their classes
            try:
                shutil.move(image.path_result, os.path.join(batch_folder, image.class_folder_name, image.name_result))
                # Also move the corresponding JSON file
                shutil.move(image.json_result_path, os.path.join(batch_folder, image.class_folder_name, os.path.basename(image.json_result_path)))
            except Exception as e:
                # Message box to inform the user of the error
                QMessageBox.warning(self, 'Error', f'Error moving the images to their subfolders: {str(e)}', QMessageBox.Ok)

        print("Subdirectories created!")

        print("Images moved to subfolders!")

        # Display results images
        self.load_image_result(self.Images[0])

        # Add the current batch to the list of batches

        # Store the paths of the selected folders in a text file
        with open(os.path.join(os.getcwd(), 'selected_batches.txt'), 'w') as save_results_file:
            save_results_file.write(os.path.join(self.Batches[0].path, 'results.txt'))

        self.batch_results.clear()
        self.batch_results.append(os.path.join(self.Batches[0].path, 'results.txt'))

        # Export the report
        self.export_report()

        # Enable the previous and next buttons
        self.ui.next.setEnabled(True)
        self.ui.previous.setEnabled(True)

        # Set next and previous buttons to navigate through the results
        self.ui.next.clicked.connect(self.show_next_result)
        self.ui.previous.clicked.connect(self.show_previous_result)

        # Disable the Start button
        self.ui.Start.setEnabled(False)

    def export_report(self):
        """
        Export the report in HTML format.
        Rename the HTML file to the name of the batch. Save it in the same folder as the batch.
        """

        print("Exporting report...")
        
        # Call nbconvert to convert the notebook to HTML
        subprocess.call(["python", "src/layout.py"])

        shutil.move(os.path.join(os.getcwd(), 'stats.html'), self.Batches[0].path)

        report_name = self.Batches[0].name + '_report.html'

        os.rename(os.path.join(self.Batches[0].path, 'stats.html'), os.path.join(self.Batches[0].path, report_name))
        webbrowser.open(f'file://{self.Batches[0].path}/{report_name}')

        # Add the graphs to the visualisation pane, in the graph1 and graph2 labels
        self.ui.graph1.setPixmap(QPixmap(os.path.join(self.Batches[0].path, 'Output_Graphs', 'Bar_plot.png')).scaledToHeight(self.ui.stats_graphs_frame.height()))
        self.ui.graph2.setPixmap(QPixmap(os.path.join(self.Batches[0].path, 'Output_Graphs', 'bee_species_counts.png')).scaledToHeight(self.ui.stats_graphs_frame.height()))

        # Fill the table with the results
        self.fill_table()

    # def fill_table(self):
    #     """
    #     Fill the table with the results of the batch.
    #     """


    def export_batch_report(self):
        """
        Export the report in HTML format.
        The report is a comparison of the results of the selected batches.
        """

        # Clear the text file containing the paths of the selected folders
        with open(os.path.join(os.getcwd(), 'selected_batches.txt'), 'w') as save_results_file:
            save_results_file.write('')

        try:
            # Set font
            font = QFont()
            font.setPointSize(8)

            # Open a file dialog to select one or more folders to compare different batches
            file_dialog = QFileDialog()
            file_dialog.setFileMode(QFileDialog.DirectoryOnly)
            file_dialog.setOption(QFileDialog.DontUseNativeDialog, True)
            # Open the file dialog in the current project folder
            file_dialog.setDirectory(self.Projects[0].path)
            file_dialog.setFont(font)
            file_view = file_dialog.findChild(QListView, 'listView')

            # Make it possible to select multiple folders
            if file_view:
                file_view.setSelectionMode(QAbstractItemView.MultiSelection)
            f_tree_view = file_dialog.findChild(QTreeView)
            if f_tree_view:
                f_tree_view.setSelectionMode(QAbstractItemView.MultiSelection)

            # Open the file dialog
            if file_dialog.exec():
                paths = file_dialog.selectedFiles()

                # Store the paths of the selected folders in a text file
                with open(os.path.join(os.getcwd(), 'selected_batches.txt'), 'w') as save_results_file:
                    for path in paths:
                        save_results_file.write(os.path.join(path, 'results.txt') + '\n')

            # Print a text saying that the batches are being compared with their respective names (the names of the folders before the results.txt file)
            print("Comparing batches: " + ", ".join([os.path.basename(os.path.dirname(path)) for path in self.batch_results]))

        except Exception as e:
            # Message box to inform the user of the error
            QMessageBox.warning(self, 'Error', f'Error selecting the folders to compare: {str(e)}', QMessageBox.Ok)
        
        else:
            print("Exporting batch report...")
            
            # Call nbconvert to convert the notebook to HTML
            subprocess.call(["python", "src/layout.py"])

            webbrowser.open(f'file://{os.getcwd()}/Batch_Comparison.html')

    def open_app_help(self):
        """
        Open the help window. Gives information about the application (User Guide).
        """

        # Create a window to display the help
        self.help_window = HelpWindow()
        self.help_window.show()