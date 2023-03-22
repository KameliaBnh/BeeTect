from GUI_PySide2 import *

import numpy as np

# Get save_dir from the main window
#save_dir = self.save_dir
save_dir = 'C:\\Users\\benha\\Documents\\Cranfield\\Group_Project\\BPT_Cranfield\\GUI\\results_2022'

# Read the data from the results file
with open(os.path.join(save_dir, 'results.txt'), 'r') as data:
    for line in data:
        # Get the number of the images
        if line.startswith('Saved'):
            image_number = int(line.split(' ')[1])
            print('Number of images: ', image_number)
        
        # Get the index of the image
        if line.startswith('image'):
            image_index = int(line.split(' ')[1].split('/')[0])
            print('Image index: ', image_index)
            
            # Associate the image index with the image name from the dictionary
            image_name = resultsImage[image_index]
            



# For the number of images with polinators, get in the text file the number of lines where the polinator is present