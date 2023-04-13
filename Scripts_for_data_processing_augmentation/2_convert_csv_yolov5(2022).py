"""
Reads throught the CSV-Guava-Pollinators-percentages.csv file and gets
the image name, class and axis for the objects, looks inside the images and 
using the information creates yolov5 text format annotations for the existing
images
"""

########################
# import the libraries #
########################

import csv
import os
from tqdm import tqdm
import shutil
from sklearn.model_selection import train_test_split
import cv2
import pandas as pd
from PIL import Image
import yaml

#############################################################
# Set the paths for the input CSV file and the image folder #
#############################################################

csv_file = "path/to/CSV-Guava-Pollinators-percentages.csv" # Path to csv annotation file
img_folder = 'path/to/Images' # Path to the image folder
prim_dir = 'Path/to/primary/directory/with/Images/labels' # current directory path
anno_folder = 'path/to/labels' # path to save annotations in YOLOv5 format

data_yaml = "path/to/data.yaml" # path to data.yaml file which contains information about all the classes

###########################
# Load the data.yaml file #
###########################

with open(data_yaml, 'r') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

#############################################################
# Define a dictionary to map class names to integer indices #
#############################################################

class_dict = {class_name: i for i, class_name in enumerate(data['names'])}

###############################
# Define the labels to change #
###############################

labelsToChange = ["apis_dorsata", "crabronidae", "diptera", "formicidae", "hymenoptera"]

labelsToShift = ["apis_cerana", "apis_florea"]

labelsToAugment = ["apis","amegilla", "ceratina", "meliponini", "xylocopa_aestuans"]

twoLabel = ["apis; guava_flower"]

Flo = ["guava_flower"]

################################################
#Create a text file for over-expressed classes #
################################################

Shift_file_path = os.path.join( prim_dir, 'images_to_shift.txt')
with open(Shift_file_path, 'w') as f:
    pass

############################################
#Create a text file for image augmentation #
############################################

Aug_file_path = os.path.join( prim_dir, 'images_to_augment.txt')
with open(Aug_file_path, 'w') as f:
    pass

###########################################
# Open the CSV file and read its contents #
###########################################

with open(csv_file, 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # Skip the header row
    for row in reader:
        # Extract the fields from the CSV row
        file_name, class_name, xmin, ymin, xmax, ymax = row

        print(f"xmin: {xmin}, xmax: {xmax}")
        
        # Check if the class name should be changed
        if class_name in labelsToChange:
            class_name = "pollinator"
        
        if class_name in twoLabel:
            class_name = "unknown"

        if class_name in Flo:
            continue

        # Check if the class name is not empty
        if not class_name:
            print(f"Empty class name for image {file_name}")
            continue    


        # Determine the integer index for the class name
        class_index = class_dict[class_name]


        ###################################
        # Create the annotation file name #
        ###################################

        anno_file_name = file_name.replace('.JPG', '.txt')
        
        # Check if the image file exists
        img_file_path = os.path.join(img_folder, file_name)
        if not os.path.exists(img_file_path):
            print(f"Image file not found: {img_file_path}")
            continue

        #Calculating size of image
        img = Image.open(img_file_path)
        width, height = img.size
        channels = len(img.getbands())

        if not os.path.exists(img_file_path):
            print(f"Image file not found: {img_file_path}")
            continue
        
        # Calculate the object dimensions and center coordinates
        center_x = (float(xmin) + float(xmax)) / 2
        center_y = (float(ymin) + float(ymax)) / 2
        width = (float(xmax) - float(xmin))
        height = (float(ymax) - float(ymin))
        
        
        
        # Create the annotation string in YOLOv5 format
        anno_str = f"{class_index} {center_x:.3f} {center_y:.3f} {width:.3f} {height:.3f}"
        
        # Write the annotation string to the annotation file
        anno_file_path = os.path.join(anno_folder, anno_file_name)
        with open(anno_file_path, 'a') as f:
            f.write(anno_str + '\n')


        ###################################################################
        # Check if the current image file name is in labelsToAugment list #
        ###################################################################
        
        if class_name in labelsToAugment:
            with open(Aug_file_path, 'a') as f:
                f.write(f"{class_name} {file_name}\n")

        #############################################################
        # Check if current image file name is in labelsToShift list #
        #############################################################
        if class_name in labelsToShift:
            with open(Shift_file_path, 'a') as f:
                f.write(f"{class_name} {file_name}\n")




