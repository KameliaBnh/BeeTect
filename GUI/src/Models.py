# Attributes:
#   - path: Path to the models directory
#   - list: List of models in the models directory

# Functions:
#   - __init__(self): Class constructor
#   - open_models_form(self): Open the models form
#   - close_models_form(self): Close the models form
#   - open_model_weight(self): Open a file dialog to select the model weight file
#   - save_new_model(self): Save the new model

import glob
import os
import shutil

from PySide2 import QtWidgets
from PySide2.QtWidgets import QMessageBox, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog
from PySide2.QtGui import QFont
from PySide2 import QtCore

class Models(QDialog):

    def __init__(self):

        # Class attributes
        self.path = os.path.join(os.getcwd(), 'models')

        # Get the list of models in the models directory with the glob module
        self.list = [os.path.splitext(os.path.basename(file))[0] for file in glob.glob(os.path.join(self.path, '*', '*.pt'))]

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

        self.model_edit = QLineEdit()
        self.model_weight_edit = QLineEdit()
        
        # Create a layout for the form
        layout = QVBoxLayout()

        labels_and_edits = {
            'Model name:': self.model_edit,
            'Model weight:': self.model_weight_edit,
        }

        for label_text, line_edit in labels_and_edits.items():
            label = QLabel(label_text)
            label.setFont(font)
            line_edit.setPlaceholderText('Required' if label_text == 'Model name:' else '')
            line_edit.setFont(font)
            layout.addWidget(label)
            layout.addWidget(line_edit)

        self.model_weight_button = QPushButton('Browse')
        self.model_weight_button.setFont(font)
        self.model_weight_button.clicked.connect(self.open_model_weight)
        layout.addWidget(self.model_weight_button)

        self.confusion_matrix_line_edit = QLineEdit()
        self.f1_curve_line_edit = QLineEdit()
        self.results_line_edit = QLineEdit()
        self.opt_yaml_line_edit = QLineEdit()

        buttons_and_edits = [
            ('Select Confusion Matrix', self.confusion_matrix_line_edit),
            ('Select F1 Curve', self.f1_curve_line_edit),
            ('Select Results (PNG)', self.results_line_edit),
            ('Select opt.yaml', self.opt_yaml_line_edit),
        ]

        self.file_selection_group_box = QtWidgets.QGroupBox('Additional Files', self)
        self.file_selection_group_box.setFont(font)
        self.file_selection_group_box.setCheckable(True)
        self.file_selection_group_box.setChecked(False)
        self.file_selection_layout = QVBoxLayout(self.file_selection_group_box)

        for button_text, line_edit in buttons_and_edits:
            button = QtWidgets.QPushButton(button_text, self.file_selection_group_box)
            button.setFont(font)
            button.clicked.connect(self.open_file_dialog)
            line_edit.setFont(font)
            self.file_selection_layout.addWidget(button)
            self.file_selection_layout.addWidget(line_edit)

        # Create a submit button to save the new model
        self.submit_button = QPushButton('Submit')
        self.submit_button.setFont(font)
        self.submit_button.clicked.connect(self.save_new_model)

        layout.addWidget(self.file_selection_group_box)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def toggle_files(self):
        if self.file_selection_group_box.isChecked():
            self.confusion_matrix_button.setEnabled(True)
            self.f1_curve_button.setEnabled(True)
            self.results_button.setEnabled(True)
            self.opt_yaml_button.setEnabled(True)
        else:
            self.confusion_matrix_button.setEnabled(False)
            self.f1_curve_button.setEnabled(False)
            self.results_button.setEnabled(False)
            self.opt_yaml_button.setEnabled(False)

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

                if self.confusion_matrix_line_edit.text():
                    confusion_matrix_file = self.confusion_matrix_line_edit.text()
                    shutil.copy(confusion_matrix_file, os.path.join(self.path, self.model_edit.text(), 'confusion_matrix.png'))

                if self.f1_curve_line_edit.text():
                    f1_curve_file = self.f1_curve_line_edit.text()
                    shutil.copy(f1_curve_file, os.path.join(self.path, self.model_edit.text(), 'f1_curve.png'))

                if self.results_line_edit.text():
                    results_file = self.results_line_edit.text()
                    shutil.copy(results_file, os.path.join(self.path, self.model_edit.text(), 'results.png'))

                if self.opt_yaml_line_edit.text():
                    opt_yaml_file = self.opt_yaml_line_edit.text()
                    shutil.copy(opt_yaml_file, os.path.join(self.path, self.model_edit.text(), 'opt.yaml'))
                
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'Error copying model weight file: {str(e)}')
                return
            
            # Add the new model to the models list
            if model_name not in self.list:
                self.list.append(model_name)

    def open_file_dialog(self):
        sender = self.sender()
        if sender.text() == 'Select Confusion Matrix':
            confusion_matrix_file, _ = QFileDialog.getOpenFileName(self, 'Select Confusion Matrix', self.path, 'Confusion Matrix (*.png)')
            self.confusion_matrix_line_edit.setText(confusion_matrix_file)
        elif sender.text() == 'Select F1 Curve':
            f1_curve_file, _ = QFileDialog.getOpenFileName(self, 'Select F1 Curve', self.path, 'F1 Curve (*.png)')
            self.f1_curve_line_edit.setText(f1_curve_file)
        elif sender.text() == 'Select Results (PNG)':
            results_file, _ = QFileDialog.getOpenFileName(self, 'Select Results (PNG)', self.path, 'Results (*.png)')
            self.results_line_edit.setText(results_file)
        elif sender.text() == 'Select opt.yaml':
            opt_yaml_file, _ = QFileDialog.getOpenFileName(self, 'Select opt.yaml', self.path, 'opt.yaml (*.yaml)')
            self.opt_yaml_line_edit.setText(opt_yaml_file)