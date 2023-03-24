# Attributes:
#   - name: Name of the user
#   - surname: Surname of the user
#   - email: Email of the user
#   - date: Date and time when the user information was saved

# Functions:
#   - __init__(self): Class constructor
#   - open_user_form(self): Open the user information form
#   - close_user_form(self): Close the user information form
#   - submit_user_info(self): Save the user information

import os
import datetime

from PySide2.QtWidgets import QMessageBox, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PySide2 import QtCore
from PySide2.QtGui import QFont

class User(QWidget):

    def __init__(self):

        # Class attributes
        self.name = None
        self.surname = None
        self.email = None
        self.date = None

        # Call the parent class constructor
        super().__init__()

        # Set the window as modal
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        # Set the font
        font = QFont()
        font.setPointSize(8)

        # Set the title and size of the form
        self.setWindowTitle('User information')
        self.resize(500, 350)

        # Remove the close button
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)

        # Create labels and line edits for user information
        user_label = QLabel('User Information:')
        user_label.setFont(font)
        user_label.setStyleSheet('font-weight: bold')
        name_label = QLabel('Name:')
        name_label.setFont(font)
        self.name_edit = QLineEdit()
        self.name_edit.setFont(font)
        surname_label = QLabel('Surname:')
        surname_label.setFont(font)
        self.surname_edit = QLineEdit()
        self.surname_edit.setFont(font)
        email_label = QLabel('Email:')
        email_label.setFont(font)
        self.email_edit = QLineEdit()
        self.email_edit.setFont(font)

        # Make all line edits required except email
        self.name_edit.setPlaceholderText('Required')
        self.surname_edit.setPlaceholderText('Required')
        self.email_edit.setPlaceholderText('Optional')

        # Create a submit button
        self.submit_button = QPushButton('Submit')
        self.submit_button.setFont(font)
        self.submit_button.clicked.connect(self.submit_user_info)

        # Create a layout for the form
        layout = QVBoxLayout()

        # User information label bold and as a separator
        layout.addWidget(user_label)
        layout.addWidget(name_label)
        layout.addWidget(self.name_edit)
        layout.addWidget(surname_label)
        layout.addWidget(self.surname_edit)
        layout.addWidget(email_label)
        layout.addWidget(self.email_edit)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    # Open user information form
    def open_user_form(self):
        self.show()

    # Close user information form
    def close_user_form(self):
        self.close()

    def submit_user_info(self):
        # Retrieve user information
        self.name = self.name_edit.text()
        self.surname = self.surname_edit.text()
        self.email = self.email_edit.text()

        if not self.name:
            QMessageBox.warning(self, 'Error', 'Please enter your name.')
            return

        if not self.surname:
            QMessageBox.warning(self, 'Error', 'Please enter your surname.')
            return
        
        # Save the user information in the preferences.txt file
        # os.path.dirname(os.getcwd()) returns the path of the parent folder of the current working directory
        with open(os.path.join(os.getcwd(), 'preferences.txt'), 'w') as f:
            f.write('User information:\n')
            f.write(f'Name: {self.name}\n')
            f.write(f'Surname: {self.surname}\n')
            f.write(f'Email: {self.email}\n')
            # Write the date and time when the user information was saved
            now = datetime.datetime.now()
            date_str = now.strftime("%d/%m/%Y")
            time_str = now.strftime("%H:%M:%S")
            f.write(f'Date: {date_str} Time: {time_str}\n')

        # Close the form
        self.close()