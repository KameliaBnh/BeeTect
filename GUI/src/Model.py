import glob
import os
import shutil

class Model():

    def __init__(self, path):
        """
        This class is used to create a new YOLO model.
        """

        # Class attributes
        self.path = path
        self.name = os.path.basename(path).split(".")[0]
        self.confusion_matrix = None
        self.f1_curve = None
        self.results = None
        self.opt_yaml = None

    def set_confusion_matrix(self, confusion_matrix):
        """
        Sets the confusion matrix.
        """

        self.confusion_matrix = confusion_matrix

    def get_confusion_matrix(self):
        """
        Gets the confusion matrix.
        """

        return self.confusion_matrix
    
    def set_f1_curve(self, f1_curve):
        """
        Sets the F1 curve.
        """

        self.f1_curve = f1_curve

    def get_f1_curve(self): 
        """
        Gets the F1 curve.
        """

        return self.f1_curve
    
    def set_results(self, results):
        """
        Sets the results.
        """

        self.results = results

    def get_results(self):
        """
        Gets the results.
        """

        return self.results
    
    def set_opt_yaml(self, opt_yaml):
        """
        Sets the opt.yaml.
        """

        self.opt_yaml = opt_yaml

    def get_opt_yaml(self):
        """
        Gets the opt.yaml.
        """

        return self.opt_yaml