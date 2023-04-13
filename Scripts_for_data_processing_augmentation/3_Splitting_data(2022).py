"""
This script randomly splits the images and their corresponding
annotations into train, test and val set in 60:20:20 ratio.
"""
#######################
# Importing libraries #
#######################
import os
import random
import shutil

####################################################################
# Set the path to the folder containing the images and annotations #
####################################################################
data_dir = "path/to/primary/folder"

###########################################################
# Set the ratio for the train, test and validation splits #
###########################################################
train_ratio = 0.6
test_ratio = 0.2
val_ratio = 0.2

############################################################################
# Create the train, test and validation folders for images and annotations #
############################################################################
for folder_name in ["train", "test", "val"]:
    os.makedirs(os.path.join(data_dir, "Images", folder_name), exist_ok=True)
    os.makedirs(os.path.join(data_dir, "labels", folder_name), exist_ok=True)

####################################################
# Get a list of all image files in the data folder #
####################################################
image_files = [f for f in os.listdir(os.path.join(data_dir, "Images")) if f.endswith(".JPG")]

# Set Seed 
random.seed(42)

###################################
# Shuffle the list of image files #
###################################
random.shuffle(image_files)

##############################################################
# Split the image files into train, test and validation sets #
##############################################################
num_images = len(image_files)
num_train = int(train_ratio * num_images)
num_test = int(test_ratio * num_images)
num_val = num_images - num_train - num_test
train_images = image_files[:num_train]
test_images = image_files[num_train:num_train+num_test]
val_images = image_files[num_train+num_test:]

random.seed(42)

#############################################################################################
# Move the image files and their corresponding annotation files to their respective folders #
#############################################################################################
for i, image_file in enumerate(train_images):
    annotation_file = image_file[:-4] + ".txt"
    if os.path.exists(os.path.join(data_dir, "labels", annotation_file)):
        shutil.move(os.path.join(data_dir, "Images", image_file), os.path.join(data_dir, "Images", "train", image_file))
        shutil.move(os.path.join(data_dir, "labels", image_file[:-4] + ".txt"), os.path.join(data_dir, "labels", "train", image_file[:-4] + ".txt"))
for i, image_file in enumerate(test_images):
    annotation_file = image_file[:-4] + ".txt"
    if os.path.exists(os.path.join(data_dir, "labels", annotation_file)):
        shutil.move(os.path.join(data_dir, "Images", image_file), os.path.join(data_dir, "Images", "test", image_file))
        shutil.move(os.path.join(data_dir, "labels", image_file[:-4] + ".txt"), os.path.join(data_dir, "labels", "test", image_file[:-4] + ".txt"))
for i, image_file in enumerate(val_images):
    annotation_file = image_file[:-4] + ".txt"
    if os.path.exists(os.path.join(data_dir, "labels", annotation_file)):
        shutil.move(os.path.join(data_dir, "Images", image_file), os.path.join(data_dir, "Images", "val", image_file))
        shutil.move(os.path.join(data_dir, "labels", image_file[:-4] + ".txt"), os.path.join(data_dir, "labels", "val", image_file[:-4] + ".txt"))
