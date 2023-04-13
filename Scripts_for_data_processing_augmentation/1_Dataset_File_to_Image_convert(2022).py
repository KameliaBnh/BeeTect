""" 
This script reads the image-ids-and-filenames.csv file 
and converts the 2022 dataset from file type to .JPG format.
"""


#######################
# Importing Libraries #
#######################

import csv
import os
from PIL import Image

##################################
# Getting all the required paths #
##################################

# Path to the CSV file
csv_path = 'path/to/image-ids-and-filenames.csv'

# Path to the folder containing the original files
folder_path = 'path/to/folder/'

# Path to the folder where you want to save the converted JPG files
output_folder_path = 'path/to/images'

###################################################################################
# Reading csv file with image id and names and convertinf files to images in .JPG #
###################################################################################

# Open the CSV file and read its contents
with open(csv_path, 'r') as file:
    reader = csv.reader(file)
    next(reader) # skip header row
    for row in reader:
        image_id = os.path.splitext(row[1])[0]
        filename = row[2]
        
        # Check if the filename is empty
        if filename:
            # Construct the paths to the original file and the output file
            original_file_path = os.path.join(folder_path, filename)
            print(f"original_file_path: {original_file_path}")
            print(f"filename: {filename}")
            
            output_file_path = os.path.join(output_folder_path, '{}.JPG'.format(image_id))

            # Open the original file and convert it to JPG
            with Image.open(original_file_path) as im:
                im.convert('RGB').save(output_file_path)
        else:
            # If filename is empty, skip to next row
            continue