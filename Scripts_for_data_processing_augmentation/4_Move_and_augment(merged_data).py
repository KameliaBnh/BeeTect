"""
This script performs the following tasks:
1. Looks for annotations inside the trainig set which have overexpressed species whose names
   are mentioned in images_to_shift.txt file and moves 50% of the images and its corresponding
   annotation files mentioned to respective test set.

2. Looks inside the images_to_augment.txt file, checks if image exists in the, performs augmentation
   and creates annotation for the augmented images using the main annotation file as reference. 
"""


import os
import numpy as np
import random
import shutil
from PIL import Image
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
from imgaug import augmenters as iaa

################################################################
# Define the paths to the images, annotations and test folders #
################################################################

images_folder = 'path/to/Images/train' # folder with train dataset
annotations_folder = 'path/to/labels/train'# folder with corresponding annotations for the train set
prim_dir = 'path/to/primary_dir' # Primary directory

test_folder_img = 'path/to/Images/test' # folder with test dataset 
test_folder_anno = 'path/to/labels/test' # folder with corresponding annotations for the test set

augment_list = 'path/to/images_to_augment.txt' # file containing names of images to augment and the species

shift_list = 'path/to/images_to_shift.txt'# file containing names of images that need to split and move to test set


#################################################################
# Splitting overexpressed classes to 50:50 parts to reduce bias #
#################################################################

# Load the list of images to augment
with open(shift_list, "r") as f:
    images_to_shift = [line.strip().split()[1] for line in f.readlines()]


# Look for files in the train folder with the same names as the images to shift
train_images = [f for f in os.listdir(images_folder) if os.path.isfile(os.path.join(images_folder, f)) and f in images_to_shift]

# Randomly split the list into 50:50
random.shuffle(train_images)
test_images = train_images[:len(train_images)//2]
train_images = train_images[len(train_images)//2:]
print("Selected test images", test_images)

# set seed
#random.seed(42)

# Move the test images to the test folder
for file_name in test_images:
    image_path = os.path.join(images_folder, file_name)
    annotation_path = os.path.join(annotations_folder, os.path.splitext(file_name)[0] + ".txt")

    if os.path.isfile(image_path) and os.path.isfile(annotation_path):
        print("Moving files:", file_name)
        print("  Image path:", image_path)
        print("  Annotation path:", annotation_path)
        shutil.move(image_path, test_folder_img)
        shutil.move(annotation_path, test_folder_anno)
        print("Moved file:", file_name)

    else:
        print("Files do not exist:", file_name)
        print("  Image path:", os.path.abspath(image_path))
        print("  Annotation path:", annotation_path)



#####################
# Data Augmentation #
#####################

# Define the augmentation pipeline
aug_pipeline = iaa.Sequential([
    iaa.AdditiveGaussianNoise(scale=0.20*255),
    iaa.Affine(rotate=(-20, 20)),
    iaa.Fliplr(0.10),
    iaa.MultiplyBrightness((0.6, 1.4))
])

# Load the list of images to augment
with open(augment_list, "r") as f:
    images_to_augment = [line.strip().split() for line in f.readlines()]

# set seed
#random.seed(42)

# Loop through the images and augment them if the corresponding annotation file exists
for class_name, file_name in images_to_augment:
    image_path = os.path.join(images_folder, file_name)
    annotation_path = os.path.join(annotations_folder, f"{os.path.splitext(file_name)[0]}.txt")

    # Check if the annotation file exists
    if not os.path.isfile(annotation_path):
        print(f"Annotation file {annotation_path} not found. Skipping augmentation for {file_name}.")
        continue

    # Load the image and the annotation file
    image = np.array(Image.open(image_path))
    with open(annotation_path, "r") as f:
        lines = f.readlines()

   ####################################################
   # Annotating the Augmented images to YOLOv5 format #
   #################################################### 

    # Parse the annotation data in YOLOv5 format
    bboxes = []
    class_ids = []
    for line in lines:
        class_id = int(line.strip().split()[0])
        x_center = float(line.strip().split()[1])
        y_center = float(line.strip().split()[2])
        width = float(line.strip().split()[3])
        height = float(line.strip().split()[4])
        x_min = int((x_center - width / 2) * image.shape[1])
        y_min = int((y_center - height / 2) * image.shape[0])
        x_max = int((x_center + width / 2) * image.shape[1])
        y_max = int((y_center + height / 2) * image.shape[0])
        bboxes.append(BoundingBox(x1=x_min, y1=y_min, x2=x_max, y2=y_max)) 
        class_ids.append(class_id)


    # Apply the augmentation pipeline multiple times to create more than one augmented image
    for i in range(4):  # create 4 augmented images
        # Apply the augmentation pipeline
        bbs = BoundingBoxesOnImage(bboxes, shape=image.shape)
        image_aug, bbs_aug = aug_pipeline(image=image, bounding_boxes=bbs)
        
        # Save the augmented image and the new annotation file
        image_aug_filename = f"{os.path.splitext(file_name)[0]}_aug_{i}.JPG"
        image_aug_path = os.path.join(images_folder, image_aug_filename)
        Image.fromarray(image_aug).save(image_aug_path)

        with open(os.path.join(annotations_folder, f"{os.path.splitext(image_aug_filename)[0]}.txt"), "w") as f:
            for bbox_aug, class_id in zip(bbs_aug, class_ids):
                x_center = (bbox_aug.x1 + bbox_aug.x2) / (2 * image_aug.shape[1])
                y_center = (bbox_aug.y1 + bbox_aug.y2) / (2 * image_aug.shape[0])
                width = (bbox_aug.x2 - bbox_aug.x1) / image_aug.shape[1]
                height = (bbox_aug.y2 - bbox_aug.y1) / image_aug.shape[0]
                f.write(f"{int(class_id)} {x_center:.3f} {y_center:.3f} {width:.3f} {height:.3f}\n")


