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
