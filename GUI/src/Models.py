# Attributes:
#   - path: Path to the models directory
#   - list: List of models in the models directory

# Functions:
#   - __init__(self): Class constructor
#   - open_models_form(self): Open the models form
#   - close_models_form(self): Close the models form
#   - open_model_weight(self): Open a file dialog to select the model weight file
#   - save_new_model(self): Save the new model

import os
import shutil

from PySide2.QtWidgets import QMessageBox, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog
from PySide2.QtGui import QFont
from PySide2 import QtCore

class Models(QDialog):

    def __init__(self):

        # Class attributes
        self.path = os.path.join(os.getcwd(), 'models')
        self.list = []
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith('.pt') and root.endswith(os.path.basename(file).split('.')[0]):
                    self.list.append(os.path.basename(file).split('.')[0])

        # Call the parent class constructor
        super().__init__()

        # Set the window as modal
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        # Set the font
        font = QFont()
        font.setPointSize(8)

        # Set the title and size of the form
        self.setWindowTitle('New YOLO Model')
        self.resize(550, 400)

        # Create labels and line edits for new model
        model_label = QLabel('Model name:')
        model_label.setFont(font)
        self.model_edit = QLineEdit()
        self.model_edit.setPlaceholderText('Required')
        self.model_edit.setFont(font)

        # Create a model weight label that open a file dialog to select the model weight file
        model_weight_label = QLabel('Model weight:')
        model_weight_label.setFont(font)
        self.model_weight_edit = QLineEdit()
        self.model_weight_edit.setReadOnly(True)
        self.model_weight_edit.setFont(font)
        self.model_weight_button = QPushButton('Browse')
        self.model_weight_button.setFont(font)
        self.model_weight_button.clicked.connect(self.open_model_weight)

        self.submit_button = QPushButton('Submit')
        self.submit_button.setFont(font)
        self.submit_button.clicked.connect(self.save_new_model)

        # Create a layout for the form
        layout = QVBoxLayout()
        layout.addWidget(model_label)
        layout.addWidget(self.model_edit)
        layout.addWidget(model_weight_label)
        layout.addWidget(self.model_weight_edit)
        layout.addWidget(self.model_weight_button)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    # Open models form
    def open_models_form(self):
        self.show()

    # Close models form
    def close_models_form(self):
        self.close()

    def open_model_weight(self):
        # Open a file dialog to select the model weight file
        model_weight_file, _ = QFileDialog.getOpenFileName(self, 'Select model weight file', self.path, 'Model weight (*.pt)')
        self.model_weight_edit.setText(model_weight_file)

    def save_new_model(self):

        model_name = None
        model_weight = None

        #while True:

        try:
            # Retrieve the model information
            model_name = self.model_edit.text()
            model_weight = self.model_weight_edit.text()

            # Create a new directory for the model
            if model_name and model_name not in self.list:
                os.makedirs(os.path.join(self.path, model_name), exist_ok=True)

            if not model_name or not model_weight or not os.path.isfile(model_weight):
                raise Exception('Please retry to enter the model information.')

        except Exception as e:
            QMessageBox.warning(self, 'Error', str(e), QMessageBox.Ok)

        else:
            # Get the path to the model weight file
            model_weight_path = os.path.join(self.path, model_name, model_name + '.pt')

            # Copy the model weight file to the models directory
            try:
                print(f'Copying model weight file to {model_weight_path}')
                shutil.copy(model_weight, model_weight_path)
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'Error copying model weight file: {str(e)}')
                return
            
            # Add the new model to the models list
            if model_name not in self.list:
                self.list.append(model_name)
