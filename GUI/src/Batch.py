import os

class Batch():
    
    def __init__(self, path):

        # Class attributes
        self.path = path
        self.name = os.path.basename(self.path)
        self.project = os.path.basename(os.path.dirname(self.path))
