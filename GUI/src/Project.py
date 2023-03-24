# Attributes :
#   - name : Name of the project
#   - path : Path to the project
#   - creation_date : Date of creation of the project
#   - last_modification_date : Date of the last modification of the project

# Functions :
#   - __init__(self, name, path) : Class constructor
#   - open_project(self) : Open the project
#   - create_project(self) : Create a new project
#   - open_project_directory(self, project_directory_edit) : Open a file dialog to select the project directory
#   - save_new_project(self, project_name_edit, project_directory_edit) : Save the new project
#   - save_project(self) : Save the project to text file

import os

from PySide2.QtWidgets import QWidget, QFileDialog, QMessageBox, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PySide2.QtGui import QFont

class Project(QWidget):
    
    def __init__(self):

        # Class attributes
        self.name = None
        self.path = None
        self.creation_date = None
        self.last_modification_date = None

        # Call the parent class constructor
        super().__init__()

    # Open the project
    def open_project(self):

        try:
            # Open the project
            self.path = QFileDialog.getExistingDirectory(self, "Open Project", os.getcwd())
        
        except Exception as e:
            # Open message box
            QMessageBox.warning(self, 'Error', f'Error opening project: {str(e)}', QMessageBox.Ok)
            return
        
        else:
            # Get the project name
            self.name = os.path.basename(self.path)

            # Get the project creation date
            self.creation_date = os.path.getctime(self.path)

            # Get the project last modification date
            self.last_modification_date = os.path.getmtime(self.path)

            # Save project to text file
            self.save_project(self.name, self.path)

    # Open a file dialog to select the project directory
    def open_project_directory(self, project_directory_edit):
        try:
            # Open the project directory
            project_directory = QFileDialog.getExistingDirectory(self, "Select Project Directory", os.getcwd())

        except Exception as e:
            # Open message box
            QMessageBox.warning(self, 'Error', f'Error opening project directory: {str(e)}', QMessageBox.Ok)
            return
        
        else:
            # Set the project directory
            project_directory_edit.setText(project_directory)

    # Save the new project
    def save_new_project(self, project_name_edit, project_directory_edit):
            
        try:
            # Get the project name
            self.name = project_name_edit.text()
    
            # Get the project directory
            self.path = os.path.join(project_directory_edit.text(), project_name_edit.text())

        except Exception as e:
            # Open message box
            QMessageBox.warning(self, 'Error', f'Error saving project: {str(e)}', QMessageBox.Ok)
            return
        
        else:
            # Create the project directory
            os.mkdir(self.path)

            # Get the project creation date
            self.creation_date = os.path.getctime(self.path)

            # Get the project last modification date
            self.last_modification_date = os.path.getmtime(self.path)

            # Open message box
            QMessageBox.information(self, 'Success', 'Project created successfully')

            # Close the dialog
            self.close()

    # Create a new project
    def create_project(self):
        
        # Open a file dialog to select the project name and directory
        dialog = QDialog()
        dialog.setWindowTitle('Create New Project')
        dialog.setModal(True)
        dialog.setFixedSize(500, 300)
        layout = QVBoxLayout(dialog)

        # Set the font
        font = QFont()
        font.setPointSize(8)

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

        # Save project to text file
        self.save_project(self.name, self.path)

        # Close the dialog when the save_new_project dialog is closed
        dialog.close()

    # Save the project to text file
    def save_project(self, name, path):
        # Open 'preferences.txt' file
        with open(os.path.join(os.getcwd(), 'preferences.txt'), 'r') as file:
            # Read the file
            lines = file.readlines()

        # Copy the 5 first lines of the file
        new_lines = lines[:5]

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
        with open(os.path.join(os.getcwd(), 'preferences.txt'), 'w') as file:
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

    