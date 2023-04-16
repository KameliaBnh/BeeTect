import datetime
import os
import shutil
import subprocess
import webbrowser
import pandas
import torch
import csv

from PySide2.QtGui import QIcon, QFont, QPixmap
from PySide2.QtCore import QFile, Qt
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QMainWindow, QMainWindow, QMenu, QFileDialog, QMessageBox, QInputDialog, QPushButton, QDialog, QLineEdit, QVBoxLayout, QLabel, QTableWidget, QHeaderView, QTableWidgetItem, QAction, QAbstractItemView, QListView, QTreeView, QGroupBox

import Project
import User
import Model
import Image
import Batch
from HelpWindow import HelpWindow

class MainWindow(QMainWindow):

    def __init__(self):
        """
        Constructor of the MainWindow class.
        It creates the main window of the application using the 'interface.ui' file.
        It also creates the User, Model, Images, Projects and Batches objects.
        """

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
        self.setWindowIcon(QIcon(os.path.join(os.getcwd(), "resources/bee.jpg")))

        
        # Class attributes
    
        # Create an empty list to store the users filled with the users written in the users.txt file if it exists
        self.Users = []
        if os.path.exists(os.path.join(os.getcwd(), "users.txt")):
            with open(os.path.join(os.getcwd(), "users.txt"), "r") as users_file:
                for line in users_file.read().splitlines():
                    self.Users.insert(0, User.User(line.split(" ")[0], line.split(" ")[1]))

            # Update the combobox with the users
            self.ui.userSelection.clear()
            self.ui.userSelection.addItems([user.name + " " + user.surname for user in self.Users])

        self.Models = []
        # Create an empty list to store the models filled with the models written in the models.txt file if it exists
        if os.path.exists(os.path.join(os.getcwd(), 'models', "models.txt")):
            with open(os.path.join(os.getcwd(), 'models', "models.txt"), "r") as models_file:
                for line in models_file.read().splitlines():
                    self.Models.append(Model.Model(line))
        else:
            # Write the models currently available in the models folder in the models.txt file
            with open(os.path.join(os.getcwd(), 'models', "models.txt"), "w") as models_file:
                for root, dirs, files in os.walk(os.path.join(os.getcwd(), "models")):
                    for file in files:
                        if file.endswith('.pt'):
                            model_path = os.path.join(root, file)
                            models_file.write(model_path + "\n")
                            self.Models.append(Model.Model(model_path))

        # Update the combobox with the models
        self.ui.modelSelection.clear()
        self.ui.modelSelection.addItems([model.name for model in self.Models])

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

        else:
            self.Batches = []

        self.batch_results = []

        # If the selected_batches.txt file exists, fill the self.batches_results list
        if os.path.exists(os.path.join(os.getcwd(), "selected_batches.txt")):
            with open(os.path.join(os.getcwd(), "selected_batches.txt"), "r") as save_results_file:
                self.batch_results = save_results_file.read().splitlines()
        
        # Check if the user_info.txt file exists when the application starts
        self.check_flag = False
        self.check_preferences()

        # Load models from the models folder in the combobox
        self.load_models()

        # Close the application when the user clicks the close button
        self.ui.Exit.triggered.connect(self.close)

        # Connect the button to the function add_new_user
        self.ui.addUser.clicked.connect(self.add_user)

        # Connect the userSelection combo box to the function update_user_info
        self.ui.userSelection.currentIndexChanged.connect(self.update_user_info)
        
        # Connect the button to the function open_project
        self.ui.OpenProject.triggered.connect(self.open_project)
        # Connect the button to the function new_project
        self.ui.NewProject.triggered.connect(self.new_project)

        # Connect the addModel button to the function new_model
        self.ui.addModel.clicked.connect(self.add_new_model)

        # Connect the editModels button to the function edit_models
        self.ui.editModels.clicked.connect(self.edit_models)

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
                self.open_user_form()
                print("Getting user information...")
                # Add message to the status bar
                self.ui.status_bar.setText("Getting user information...")

            else:

                print("Retrieving user information...")
                # Add message to the status bar
                self.ui.status_bar.setText("Retrieving user information...")
                with open(os.path.join(os.getcwd(), 'user_info.txt'), 'r') as file:

                    # Create an empty dictionary to store the user information
                    info_dict = {}

                    for line in file.readlines()[:10]:
                        if ': ' in line:
                            x = line.split(': ')
                            info_dict[x[0].strip()] = x[1].strip()

                    # Assign values to the class attributes
                    self.Users.insert(0, User.User(info_dict['Name'], info_dict['Surname']))
                    self.Users[0].set_email(info_dict['Email'])
                    self.Users[0].set_date(info_dict['Date'])
                    self.Users[0].set_time(info_dict['Time'])

                    # Set the user name in the userSelection combo box and in the userDisplay label
                    self.ui.userSelection.setCurrentText(self.Users[0].name + ' ' + self.Users[0].surname)
                    self.ui.currentUser.setText(self.Users[0].name + ' ' + self.Users[0].surname)

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
            # Add message to the status bar
            self.ui.status_bar.setText("Current Project: " + self.Projects[0].name)

    # Open user information form
    def open_user_form(self):

        dialog = QDialog()

        # Set the window as modal
        dialog.setWindowModality(Qt.ApplicationModal)

        # Set the font
        font = QFont()
        font.setPointSize(8)

        # Set the title and size of the form
        dialog.setWindowTitle('User information')
        dialog.resize(550, 400)

        # Remove the close button
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowCloseButtonHint)

        # Set icon
        dialog.setWindowIcon(QIcon(os.path.join(os.getcwd(), 'resources', 'user.png')))

        # Create labels and line edits for user information
        user_label = QLabel('User Information:')
        user_label.setFont(font)
        user_label.setStyleSheet('font-weight: bold')
        name_label = QLabel('Name:')
        name_label.setFont(font)
        dialog.name_edit = QLineEdit()
        dialog.name_edit.setFont(font)
        surname_label = QLabel('Surname:')
        surname_label.setFont(font)
        dialog.surname_edit = QLineEdit()
        dialog.surname_edit.setFont(font)
        email_label = QLabel('Email:')
        email_label.setFont(font)
        dialog.email_edit = QLineEdit()
        dialog.email_edit.setFont(font)

        # Make all line edits required except email
        dialog.name_edit.setPlaceholderText('Required')
        dialog.surname_edit.setPlaceholderText('Required')
        dialog.email_edit.setPlaceholderText('Optional')

        # Create a submit button
        dialog.submit_button = QPushButton('Submit')
        dialog.submit_button.setFont(font)
        dialog.submit_button.clicked.connect(lambda: self.submit_user_info(dialog))

        # Create a layout for the form
        layout = QVBoxLayout()

        # User information label bold and as a separator
        layout.addWidget(user_label)
        layout.addWidget(name_label)
        layout.addWidget(dialog.name_edit)
        layout.addWidget(surname_label)
        layout.addWidget(dialog.surname_edit)
        layout.addWidget(email_label)
        layout.addWidget(dialog.email_edit)
        layout.addWidget(dialog.submit_button)

        dialog.setLayout(layout)

        dialog.show()

    def submit_user_info(self, dialog):
        """
        Save user information in the 'user_info.txt' file and in the Users list.
        """

        # Retrieve user information
        self.Users.insert(0, User.User(dialog.name_edit.text(), dialog.surname_edit.text(), dialog.email_edit.text()))

        now = datetime.datetime.now()
        date_str = now.strftime("%d/%m/%Y")
        self.Users[0].set_date(date_str)
        time_str = now.strftime("%H:%M:%S")
        self.Users[0].set_time(time_str)

        # Write the user in the users.txt file
        # Check if the file exists
        user_exists = False
        users_file = os.path.join(os.getcwd(), 'users.txt')
        if os.path.isfile(users_file):
            # If the file exists, check if the user exists in the file
            with open(users_file, 'r') as f:
                for line in f:
                    if f'{self.Users[0].name} {self.Users[0].surname}' in line:
                        # If the user exists in the file, move it to the top of the file
                        lines = f.readlines()
                        lines.insert(0, line)
                        with open(users_file, 'w') as f2:
                            f2.writelines(lines)
                        user_exists = True
                        break
            if not user_exists:
                # If the user doesn't exist in the file, add it at the end of the file
                with open(users_file, 'a') as f:
                    f.write(f'{self.Users[0].name} {self.Users[0].surname}\n')
        else:
            # If the file doesn't exist, create it
            with open(users_file, 'w') as f:
                f.write(f'{self.Users[0].name} {self.Users[0].surname}\n')

        # Display the name of the user
        self.ui.currentUser.setText(self.Users[0].name + " " + self.Users[0].surname)

        # Add the current user to the comboBox
        self.ui.userSelection.clear()
        self.ui.userSelection.addItems([user.name + " " + user.surname for user in self.Users])

        # Check if the user has entered their name and surname
        if not dialog.name_edit.text():
            QMessageBox.warning(self, 'Error', 'Please enter your name.')
            return

        if not dialog.surname_edit.text():
            QMessageBox.warning(self, 'Error', 'Please enter your surname.')
            return
        
        # Save the user information in the user_info.txt file
        # os.path.dirname(os.getcwd()) returns the path of the parent folder of the current working directory
        user_info_file = os.path.join(os.getcwd(), 'user_info.txt')
        if os.path.exists(user_info_file):
            with open(user_info_file, 'r') as f:
                lines = f.readlines()
            with open(user_info_file, 'w') as f:
                for line in lines:
                    if line.startswith('User information:'):
                        # Go to the next line
                        f.write('User information:\n')
                    elif line.startswith('Name:'):
                        f.write(f'Name: {self.Users[0].name}\n')
                    elif line.startswith('Surname:'):
                        f.write(f'Surname: {self.Users[0].surname}\n')
                    elif line.startswith('Email:'):
                        f.write(f'Email: {self.Users[0].email}\n')
                    elif line.startswith('Date:'):
                        f.write(f'Date: {date_str}\n')
                    elif line.startswith('Time:'):
                        f.write(f'Time: {time_str}\n')
                    else:
                        f.write(line)
        else:
            with open(user_info_file, 'w') as f:
                f.write('User information:\n')
                f.write(f'Name: {self.Users[0].name}\n')
                f.write(f'Surname: {self.Users[0].surname}\n')
                f.write(f'Email: {self.Users[0].email}\n')
                f.write(f'Date: {date_str}\n')
                f.write(f'Time: {time_str}\n')

        # Close the user information form
        dialog.close()

    def add_user(self):
        """
        Add a new user to the Users list.
        """

        print("Adding a new user...")
        # Add message to the status bar
        self.ui.status_bar.setText("Adding a new user...")

        # Open the user information form
        self.open_user_form()

    def update_user_info(self, index):
        """
        Update the user information when the user selection combo box is changed.
        """
        # Get the selected user from the combo box
        selected_user = self.ui.userSelection.currentText()

        # Move the selected user to the top of the self.Users list
        for i, user in enumerate(self.Users):
            if user.name + " " + user.surname == selected_user:
                self.Users.insert(0, self.Users.pop(i))
                break

        # Update the user_info.txt file
        with open(os.path.join(os.getcwd(), 'user_info.txt'), 'r+') as file:
            lines = file.readlines()
            file.seek(0)
            file.truncate()

            # Write the user information to the file
            for line in lines:
                if line.startswith("Name:"):
                    file.write(f"Name: {self.Users[0].name}\n")
                elif line.startswith("Surname:"):
                    file.write(f"Surname: {self.Users[0].surname}\n")
                elif line.startswith("Email:"):
                    file.write(f"Email: {self.Users[0].get_email()}\n")
                elif line.startswith("Date:"):
                    file.write(f"Date: {self.Users[0].get_date()}\n")
                elif line.startswith("Time:"):
                    file.write(f"Time: {self.Users[0].get_time()}\n")
                else:
                    file.write(line)

        # Update the current user label
        self.ui.currentUser.setText(selected_user)

        # Update the current selected item in the combo box
        self.ui.userSelection.setCurrentIndex(index)

    # Save the project to text file
    def write_project_to_text_file(self, name, path):
        """
        Save the current project information to the 'user_info.txt' file.
        """

        print("Saving project information to user_info.txt file...")
        # Add message to the status bar
        self.ui.status_bar.setText("Saving project information to user_info.txt file...")

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
        # Add message to the status bar
        self.ui.status_bar.setText("Opening project: " + self.Projects[0].name)

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
            # Add message to the status bar
            self.ui.status_bar.setText("Opening project: " + self.Projects[0].name)

        except Exception as e:
            # Open message box
            QMessageBox.warning(self, 'Error', f'Error opening project: {str(e)}', QMessageBox.Ok)
            return
        
        else:
            print("Project opened successfully!")
            # Add message to the status bar
            self.ui.status_bar.setText("Project opened successfully!")

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
            # Add message to the status bar
            self.ui.status_bar.setText("Selecting project directory...")

        except Exception as e:
            # Open message box
            QMessageBox.warning(self, 'Error', f'Error opening project directory: {str(e)}', QMessageBox.Ok)
            return
        
        else:
            # Set the project directory
            project_directory_edit.setText(project_directory)

            print(project_directory + " selected successfully!")
            # Add message to the status bar
            self.ui.status_bar.setText(project_directory + " selected successfully!")

    # Save the new project
    def save_new_project(self, project_name_edit, project_directory_edit):
        """
        Save the new project. Add the project to the top of the list of projects. Save the project to the 'user_info.txt' file.
        """
            
        try:

            print("Creating project: " + project_name_edit.text())
            # Add message to the status bar
            self.ui.status_bar.setText("Creating project: " + project_name_edit.text())

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
            # Add message to the status bar
            self.ui.status_bar.setText("Project successfully created!")

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
        # Add message to the status bar
        self.ui.status_bar.setText("Creating new project...")

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
        
    # Open models form
    def open_models_form(self):
        
        dialog = QDialog()

        # Set the window as modal
        dialog.setWindowModality(Qt.ApplicationModal)

        # Add window icon
        dialog.setWindowIcon(QIcon(QPixmap(os.path.join(os.getcwd(), 'resources', 'addModel.png'))))

        # Set the font
        font = QFont()
        font.setPointSize(8)

        # Set the title and size of the form
        dialog.setWindowTitle('New YOLO Model')
        dialog.resize(550, 400)

        dialog.model_edit = QLineEdit()
        dialog.model_weight_edit = QLineEdit()
        
        # Create a layout for the form
        layout = QVBoxLayout()

        labels_and_edits = {
            'Model name:': dialog.model_edit,
            'Model weight:': dialog.model_weight_edit,
        }

        for label_text, line_edit in labels_and_edits.items():
            label = QLabel(label_text)
            label.setFont(font)
            line_edit.setPlaceholderText('Required' if label_text == 'Model name:' else '')
            line_edit.setFont(font)
            layout.addWidget(label)
            layout.addWidget(line_edit)

        dialog.model_weight_button = QPushButton('Browse')
        dialog.model_weight_button.setFont(font)
        dialog.model_weight_button.clicked.connect(lambda: self.open_model_weight(dialog))
        layout.addWidget(dialog.model_weight_button)

        dialog.confusion_matrix_line_edit = QLineEdit()
        dialog.f1_curve_line_edit = QLineEdit()
        dialog.results_line_edit = QLineEdit()
        dialog.opt_yaml_line_edit = QLineEdit()

        buttons_and_edits = [ ('Select Confusion Matrix', 'confusion_matrix', dialog.confusion_matrix_line_edit),
                              ('Select F1 Curve', 'f1_curve', dialog.f1_curve_line_edit),
                              ('Select Results (PNG)', 'results', dialog.results_line_edit),
                              ('Select opt.yaml', 'opt_yaml', dialog.opt_yaml_line_edit),]

        dialog.file_selection_group_box = QGroupBox('Additional Files', dialog)
        dialog.file_selection_group_box.setFont(font)
        dialog.file_selection_group_box.setCheckable(True)
        dialog.file_selection_group_box.setChecked(False)
        dialog.file_selection_layout = QVBoxLayout(dialog.file_selection_group_box)

        for button_text, file_type, line_edit in buttons_and_edits:
            button = QPushButton(button_text, dialog.file_selection_group_box)
            button.setFont(font)
            button.clicked.connect(lambda dialog=dialog, file_type=file_type: self.open_file_dialog(dialog, file_type))
            line_edit.setFont(font)
            dialog.file_selection_layout.addWidget(button)
            dialog.file_selection_layout.addWidget(line_edit)

        # Create a submit button to save the new model
        dialog.submit_button = QPushButton('Submit')
        dialog.submit_button.setFont(font)
        dialog.submit_button.clicked.connect(lambda: self.save_new_model(dialog))

        layout.addWidget(dialog.file_selection_group_box)
        layout.addWidget(dialog.submit_button)

        dialog.setLayout(layout)

        dialog.show()

    def open_model_weight(self, dialog):
        """
        Opens a file dialog to select the model weight file.
        """

        # Open a file dialog to select the model weight file
        model_weight_file, _ = QFileDialog.getOpenFileName(self, 'Select model weight file', os.path.join(os.getcwd(), 'models'), 'Model weight (*.pt)')
        dialog.model_weight_edit.setText(model_weight_file)

    def save_new_model(self, dialog):
        """
        Save the new model in the models directory. It creates a new directory with the model name and copy the model weight file in it, as well as the supplementary files.
        """

        model_name = None
        model_weight = None

        try:
            # Retrieve the model information
            model_name = dialog.model_edit.text()
            model_weight = dialog.model_weight_edit.text()

            # Create a new directory for the model
            if model_name not in self.Models:
                self.Models.insert(0, Model.Model(os.path.join(os.getcwd(), 'models', model_name, model_name + '.pt')))
                # Write the model path to the models.txt file if it doesn't exist in it, else, move it to the top
                with open(os.path.join(os.getcwd(), 'models', 'models.txt'), 'a') as f:
                    f.write(self.Models[0].path + '\n')
                os.makedirs(os.path.join(os.getcwd(), 'models', model_name), exist_ok=True)

            else:
                raise Exception('This model already exists.')

            if not model_name or not model_weight or not os.path.isfile(model_weight):
                raise Exception('Please retry to enter the model information.')

        except Exception as e:
            QMessageBox.warning(self, 'Error', str(e), QMessageBox.Ok)

        else:

            # Copy the model weight file to the models directory
            try:
                print(f'Copying model weight file to {self.Models[0].path}')
                shutil.copy(model_weight, self.Models[0].path)

                if dialog.confusion_matrix_line_edit.text():
                    confusion_matrix_file = dialog.confusion_matrix_line_edit.text()
                    confusion_matrix_path = os.path.join(os.path.dirname(self.Models[0].path), 'confusion_matrix.png')
                    shutil.copy(confusion_matrix_file, confusion_matrix_path)
                    self.Models[0].set_confusion_matrix(confusion_matrix_path)

                if dialog.f1_curve_line_edit.text():
                    f1_curve_file = dialog.f1_curve_line_edit.text()
                    f1_curve_path = os.path.join(os.path.dirname(self.Models[0].path), 'f1_curve.png')
                    shutil.copy(f1_curve_file, f1_curve_path)
                    self.Models[0].set_f1_curve(f1_curve_path)

                if dialog.results_line_edit.text():
                    results_file = dialog.results_line_edit.text()
                    results_path = os.path.join(os.path.dirname(self.Models[0].path), 'results.png')
                    shutil.copy(results_file, results_path)
                    self.Models[0].set_results(results_path)

                if dialog.opt_yaml_line_edit.text():
                    opt_yaml_file = dialog.opt_yaml_line_edit.text()
                    opt_yaml_path = os.path.join(os.path.dirname(self.Models[0].path), 'opt.yaml')
                    shutil.copy(opt_yaml_file, opt_yaml_path)
                    self.Models[0].set_opt_yaml(opt_yaml_path)
                
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'Error copying model weight file: {str(e)}')
                return
            
            # Close the dialog
            dialog.close()

    def open_file_dialog(self, dialog, file_type):
        """
        Open a file dialog to select the supplementary files.
        """

        file_filter = None
        if file_type == 'confusion_matrix':
            file_filter = 'Confusion Matrix (*.png)'
            line_edit = dialog.confusion_matrix_line_edit
        elif file_type == 'f1_curve':
            file_filter = 'F1 Curve (*.png)'
            line_edit = dialog.f1_curve_line_edit
        elif file_type == 'results':
            file_filter = 'Results (*.png)'
            line_edit = dialog.results_line_edit
        elif file_type == 'opt_yaml':
            file_filter = 'opt.yaml (*.yaml)'
            line_edit = dialog.opt_yaml_line_edit
        else:
            return

        file_name, _ = QFileDialog.getOpenFileName(self, f'Select {file_type}', os.getcwd(), file_filter)
        if file_name:
            line_edit.setText(file_name)

    def add_new_model(self):
        """
        Add a new model to the list of models.
        Open a window to add a new model.
        """

        self.open_models_form()

        print("Adding new model...")
        # Add message to the status bar
        self.ui.status_bar.setText("Adding new model...")

    def load_models(self):
        """
        Load the models in the combobox.
        """

        # Clear the combobox
        self.ui.modelSelection.clear()
        for model in self.Models:
            self.ui.modelSelection.addItem(model.name)

    def close_model_form(self):
        """
        Close the model form. Refresh the combobox.
        """
        
        # Refresh the combobox
        self.load_models()

    def edit_models(self):
        """
        Open a window to edit the models. Allow the user to add, remove, and edit models.
        """

        print("Editing models...")
        # Add message to the status bar
        self.ui.status_bar.setText("Editing models...")

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
        table.setRowCount(len(self.Models))
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(['Model', 'Path'])
        # Set the resize mode of the header to allow for resizing of columns
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        table.verticalHeader().setVisible(False)
        table.setFont(font)

        # Add the models to the table
        for i, model in enumerate(self.Models):
            table.setItem(i, 0, QTableWidgetItem(model.name))
            table.setItem(i, 1, QTableWidgetItem(model.path))

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
        if selected_row < 0 or selected_row >= len(self.Models):
            return
        
        # Ask the user to confirm the deletion
        confirmation = QMessageBox.question(
            self, 'Confirm Deletion', 'Are you sure you want to delete the selected model?', 
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if confirmation == QMessageBox.Yes:

            print("Deleting " + self.Models[selected_row].name + " model...")
            # Add message to the status bar
            self.ui.status_bar.setText("Deleting " + self.Models[selected_row].name + " model...")

            # Remove the model from the list
            model_name = self.Models[selected_row].name
            self.Models.pop(selected_row)

            # Remove the model from the table
            table.removeRow(selected_row)
            
            # Delete the model and the model folder from the models folder
            model_path = os.path.dirname(self.Models[selected_row].path)
            if os.path.exists(model_path):
                shutil.rmtree(model_path)
            model_file = self.Models[selected_row].path
            if os.path.exists(model_file):
                os.remove(model_file)

            # Refresh the combobox
            self.load_models()

    def get_image(self):
        """
        Open a dialog to select an image. Add the image to the list of images.
        """

        print("Loading image...")
        # Add message to the status bar
        self.ui.status_bar.setText("Loading image...")

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
        # Add message to the status bar
        self.ui.status_bar.setText("Loading images from folder...")

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
            # Add message to the status bar
            self.ui.status_bar.setText("Saving results in a custom folder...")

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
                        if batch.project == os.path.basename(self.Projects[0].path):
                            file.write(batch.path + '\n')
                
            else:
                shutil.rmtree(folder_path)
                # Move the batch to the top of the list
                self.Batches.insert(0, self.Batches[[batch.path for batch in self.Batches].index(folder_path)])

                # Write the Batches to a text file
                with open(os.path.join(self.Projects[0].path, 'batches.txt'), 'w') as file:
                    for batch in self.Batches:
                        if batch.project == os.path.basename(self.Projects[0].path):
                            file.write(batch.path + '\n')

        # If the user selects the default folder option, create the folder if it doesn't exist
        else:

            print("Saving results in the default folder...")
            # Add message to the status bar
            self.ui.status_bar.setText("Saving results in the default folder...")

            folder_number = 1
            folder_path = os.path.join(self.Projects[0].path, 'exp')
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
                        if batch.project == os.path.basename(self.Projects[0].path):
                            file.write(batch.path + '\n')

            else:
                shutil.rmtree(folder_path)
                # Move the batch to the top of the list
                self.Batches.insert(0, self.Batches[[batch.path for batch in self.Batches].index(folder_path)])

                # Write the Batches to a text file
                with open(os.path.join(self.Projects[0].path, 'batches.txt'), 'w') as file:
                    for batch in self.Batches:
                        if batch.project == os.path.basename(self.Projects[0].path):
                            file.write(batch.path + '\n')

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

        # If the selected model is not the first one, move it to the top of the list and at the top of the text file
        
        if self.Models[0].path != self.Models[self.ui.modelSelection.currentIndex()].path:
            self.Models.insert(0, self.Models[self.ui.modelSelection.currentIndex()])
            self.Models.pop(self.ui.modelSelection.currentIndex() + 1)
            with open(os.path.join(os.getcwd(), 'models', 'models.txt'), 'w') as file:
                for model in self.Models:
                    file.write(model.path + '\n')

        print("Yolo Model selected: " + self.Models[0].name)
        # Add message to the status bar
        self.ui.status_bar.setText("Yolo Model selected: " + self.Models[0].name)

        # Select the folder where the results will be saved
        batch_folder = self.Batches[0].path

        # Run the detection
        model = torch.hub.load('ultralytics/yolov5', 'custom', self.Models[0].path) # load model
        model.conf = 0.5 # confidence threshold

        results = model([im.image_cv for im in self.Images]) # inference

        print("Running detection...")
        # Add message to the status bar
        self.ui.status_bar.setText("Running detection...")

        # Save the results
        results.save(save_dir=batch_folder, exist_ok=True)
        
        print("Processing images...")
        # Add message to the status bar
        self.ui.status_bar.setText("Processing images...")

        # Display the results
        results.print()

        # Rename the images in the folder
        print("Renaming images...")
        # Add message to the status bar
        self.ui.status_bar.setText("Renaming images...")

        for i in range(len(self.Images)):
            # Set the new path of the image
            self.Images[i].new_path_result(batch_folder)
            file = os.path.join(batch_folder, "image" + str(i) + ".jpg")
            if file.lower().endswith('.jpg') or file.lower().endswith('.jpeg') or file.lower().endswith('.png') or file.lower().endswith('.bmp'):
                os.replace(os.path.join(batch_folder, file), self.Images[i].path_result)

        # Save results to text file
        print("Saving results to text file...")
        # Add message to the status bar
        self.ui.status_bar.setText("Saving results to text file...")

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
        # Add message to the status bar
        self.ui.status_bar.setText("Subdirectories created!")

        print("Images moved to subfolders!")
        # Add message to the status bar
        self.ui.status_bar.setText("Images moved to subfolders!")

        # Display results images
        self.load_image_result(self.Images[0])

        # Add the current batch to the list of batches

        # Store the paths of the selected folders in a text file
        with open(os.path.join(os.getcwd(), 'selected_batches.txt'), 'w') as save_results_file:
            save_results_file.write(os.path.join(self.Batches[0].path, 'results.txt'))

        self.batch_results.clear()
        self.batch_results.append(os.path.join(self.Batches[0].path, 'results.txt'))

        # Enable the previous and next buttons
        self.ui.next.setEnabled(True)
        self.ui.previous.setEnabled(True)

        # Set next and previous buttons to navigate through the results
        self.ui.next.clicked.connect(self.show_next_result)
        self.ui.previous.clicked.connect(self.show_previous_result)

        # Disable the Start button
        self.ui.Start.setEnabled(False)

        # Export the report
        self.export_report()

    def export_report(self):
        """
        Export the report in HTML format.
        Rename the HTML file to the name of the batch. Save it in the same folder as the batch.
        """

        print("Exporting report...")
        # Add message to the status bar
        self.ui.status_bar.setText("Exporting report...")
        
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

    def fill_table(self):
        """
        Fill the table with the results of the batch using csv files.
        """

        # Read the data from the Counts.csv file
        data_counts = os.path.join(self.Batches[0].path, 'Counts.csv')

        # Read the data from the Model_Summary.csv file
        data_model = os.path.join(self.Batches[0].path, 'Model_Summary.csv')

        tables = [
            ('Counts.csv', self.ui.statsTable),
            ('Model_Summary.csv', self.ui.modelTable)
        ]

        # Clear the tables
        self.ui.statsTable.clear()
        self.ui.modelTable.clear()
        
        for filename, table in tables:
            with open(os.path.join(self.Batches[0].path, filename)) as file:
                reader = csv.DictReader(file)
                rows = [row for row in reader]
                
            table.setColumnCount(len(rows[0]))
            table.setHorizontalHeaderLabels(rows[0].keys())
            
            for row in rows:
                i = table.rowCount()
                table.insertRow(i)
                for j, value in enumerate(row.values()):
                    item = QTableWidgetItem(value)
                    table.setItem(i, j, item)

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
            file_dialog.setOption(QFileDialog.ShowDirsOnly, True)
            file_dialog.setOption(QFileDialog.DontResolveSymlinks, True)
            file_dialog.setOption(QFileDialog.ReadOnly, True)
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
            # Add message to the status bar
            self.ui.status_bar.setText("Comparing batches: " + ", ".join([os.path.basename(os.path.dirname(path)) for path in self.batch_results]))

            # Create a directory to save the results of the comparison and increment the number of the directory if it already exists
            i = 1
            while os.path.exists(os.path.join(self.Projects[0].path, f'Batch_Comparison_{i}')):
                i += 1
            os.mkdir(os.path.join(self.Projects[0].path, f'Batch_Comparison_{i}'))


        except Exception as e:
            # Message box to inform the user of the error
            QMessageBox.warning(self, 'Error', f'Error selecting the folders to compare: {str(e)}', QMessageBox.Ok)
        
        else:
            print("Exporting batch report...")
            # Add message to the status bar
            self.ui.status_bar.setText("Exporting batch report...")
            
            # Call nbconvert to convert the notebook to HTML
            subprocess.call(["python", "src/layout.py"])

            number = 0
            for i in range(1, len(self.Projects[0].path)):
                if os.path.exists(os.path.join(self.Projects[0].path, 'Batch_Comparison_' + str(i))):
                    number = i

            shutil.move(os.path.join(os.getcwd(), 'Batch_Comparison.html'), os.path.join(self.Projects[0].path, f'Batch_Comparison_' + str(number)))
            webbrowser.open(f'file://{os.path.join(self.Projects[0].path, "Batch_Comparison_" + str(number))}/Batch_Comparison.html')

    def open_app_help(self):
        """
        Open the help window. Gives information about the application (User Guide).
        """

        # Create a window to display the help
        self.help_window = HelpWindow()
        self.help_window.show()