# Attributes :
#   - name : Name of the project
#   - path : Path to the project
#   - creation_date : Date of creation of the project
#   - last_modification_date : Date of the last modification of the project
#   - description : Description of the project

# Functions :
#   - __init__(self, name, path) : Class constructor
#   - update_last_modification_date(self) : Update the last modification date of the project

import os

class Project():
    
    def __init__(self, path):

        # Class attributes
        self.path = path
        self.name = os.path.basename(self.path)
        self.creation_date = os.path.getctime(self.path)
        self.last_modification_date = None
        self.description = None

    def update_last_modification_date(self):
        self.last_modification_date = os.path.getmtime(self.path)
