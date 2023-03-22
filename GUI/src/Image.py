# Attributes:
#   - name: Name of the image
#   - path: Path of the image
#   - pixmap: Pixmap of the image
#   - extension: Extension of the image

# Functions:
#   - open_image: Open an image

import os
import cv2

from PySide2.QtWidgets import QWidget
from PySide2.QtGui import QPixmap

class Image(QWidget):

    def __init__(self, path):

        # Class attributes
        self.path = path
        self.name = os.path.basename(self.path)
        self.pixmap = QPixmap(self.path)
        self.extension = os.path.splitext(self.path)[1]
        self.image_cv = cv2.imread(path)[:, :, ::-1]

        self.path_result = None
        self.name_result = self.name.split('.')[0] + '_result' + self.extension
        self.pixmap_result = None
        self.json_result_path = None

        self.class_name = None
        self.class_folder_name = None

        # Call the parent class constructor
        super().__init__()

    def new_path_result(self, path):
        self.path_result = os.path.join(path, self.name_result)
        self.json_result_path = self.path_result.split('.')[0] + '.json'

    def new_pixmap_result(self, path):
        self.pixmap_result = QPixmap(path)

    def store_class_name(self, class_name):
        self.class_name = class_name

        # Define path to the folder corresponding to the class of the image
        if self.class_name == [] or set(self.class_name) == set(['flower']):
            self.class_folder_name = 'Non-Pollinator'
        else:
            self.class_folder_name = 'Pollinator'

            # Subfolders
            if len(list(set([bee for bee in self.class_name if bee != 'flower']))) >= 2:
                self.class_folder_name = os.path.join(self.class_folder_name, 'Multiple-Pollinators')
            
            else:
                self.class_folder_name = os.path.join(self.class_folder_name, [bee for bee in self.class_name if bee != 'flower'][0])