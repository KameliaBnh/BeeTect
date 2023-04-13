"""
This script reads the annotations.json using pandas
and converts them to txt for YOLO training.
"""

# import the libraries
import os
from tqdm import tqdm
import shutil
from sklearn.model_selection import train_test_split
import cv2
import pandas as pd
import yaml


#################################################
# Function to get the data from JSON Annotation #
#################################################

def extract_info_from_json(json_file, images_folder, annotations_folder, print_Buffer, print_shift_buff):
    '''Function to get the data from JSON Annotation file.'''
    
    # Initialise the info dict 
    info_dict = {}
    info_dict['bboxes'] = []

    # Get the file name
    img_file = json_file.replace('json', 'JPG')
    info_dict['filename'] = img_file

    # Get the image size
    img = cv2.imread(os.path.join(images_folder, img_file))

    # height, width, number of channels in image
    height = img.shape[0]
    width = img.shape[1]
    channels = img.shape[2]
    info_dict['image_size'] = tuple([width, height, channels])

    # Get details of the bounding box

    # read the json file
    df = pd.read_json(os.path.join(annotations_folder, json_file))

    # get rectangles list from annotations (rectangles has index 4)
    rectangles = df['annotations'][4]

    # rectangles is a list of dictionaries. Get 'coordinates' and 'label' of each.
    for rectangle in rectangles:

        # Get label
        label = rectangle['label']

        #if(label != 'flower'):

        # Initialise bounding box dict
        bbox = {}
        
        # condition to change flower label to guava_flower:
        flo = ["flower"]
        
        # condition to change clasess that we're not interested in to apis
        labelsToChange = ["apis_dorsata", "crabronidae", "diptera", "formicidae", "hymenoptera"]

        
        if (label in labelsToChange):
            bbox['class'] = 'pollinator'

        # condition to skip flower annotation and labelling:
        elif (label in flo):
            continue
        

        else:
            bbox['class'] = label

            # save image names that contains classes to augment
            labelsToAugment = ["apis","amegilla", "ceratina", "meliponini", "xylocopa_aestuans"]
            if (label in labelsToAugment):
                print_Buffer.append("{} {}".format(label, img_file))

            # save image names that contains images that needs to shift (in this case apis_cerana and apis_florea)
            labelsToShift = ["apis_cerana", "apis_florea"]
            if (label in labelsToShift):
                print_shift_buff.append("{} {}".format(label, img_file))

        # Get coordinates
        coordinates = rectangle['coordinates']

        i = 0
        for point in coordinates:
            # Get xmin and ymin
            if i == 0:
                bbox['xmin'] = point['x']
                bbox['ymin'] = point['y']
            
            # Get xmax and ymax
            if i == 2:
                bbox['xmax'] = point['x']
                bbox['ymax'] = point['y']
            
            i+=1

        info_dict['bboxes'].append(bbox)


    return info_dict


######################################################################################
# Function to convert the info dict to the required yolo format and write it to disk #
######################################################################################

def convert_to_yolov5(info_dict, annotations_folder):
    '''Function to convert the data obtained from the json file to the required txt YOLO format and write it to disk.'''

    # Initialise dictionary that maps class names to IDs
    class_name_to_id_mapping = dict()

    # read data.yaml file to get class names and indices
    yaml_file = 'path/to/data.yaml' ##SET PATH TO THE 'data.yaml' FILE##
    try:
        with open(yaml_file, "r") as stream:
            data = yaml.safe_load(stream)
            names = data['names']
            class_name_to_id_mapping = dict(zip(names, range(len(names))))
    
    except BaseException as e:
        print('ERROR:\n' + str(e))


    # Initialise print_buffer
    print_buffer = []
    
    # For each bounding box
    for b in info_dict["bboxes"]:
        try:
            class_id = class_name_to_id_mapping[b["class"]]
        except KeyError:
            print("Invalid Class. Must be one from ", class_name_to_id_mapping.keys())
        
        # Transform the bbox co-ordinates as per the format required by YOLO
        b_center_x = (b["xmin"] + b["xmax"]) / 2 
        b_center_y = (b["ymin"] + b["ymax"]) / 2
        b_width    = (b["xmax"] - b["xmin"])
        b_height   = (b["ymax"] - b["ymin"])
        
        # Write the bbox details to the file 
        print_buffer.append("{} {:.3f} {:.3f} {:.3f} {:.3f}".format(class_id, b_center_x, b_center_y, b_width, b_height))
        
    # Name of the file which we have to save 
    save_file_name = os.path.join(annotations_folder, info_dict["filename"].replace("JPG", "txt"))
    
    # Save the annotation to disk
    print("\n".join(print_buffer), file= open(save_file_name, "w"))


################################################################
# Function to convert all json annotations into YOLO style txt #
################################################################

def convert_all_files(images_folder, annotations_folder):
    '''Function to convert all json files to the txt YOLO format.'''

    # Get the annotations
    annotations = [x for x in os.listdir(annotations_folder) if x[-4:] == "json"]
    annotations.sort()

    # Initialise print_buffer
    print_Buffer = []
    
    #Initialise print_shift_buff
    print_shift_buff = []

    # Convert and save the annotations
    for ann in tqdm(annotations):
        info_dict = extract_info_from_json(ann, images_folder, annotations_folder, print_Buffer, print_shift_buff)
        convert_to_yolov5(info_dict, annotations_folder)
    
    # Save the images_to_augment file to disk
    print("\n".join(print_Buffer), file= open('images_to_augment.txt', "w"))
    
    # Save the images_to_shift file to disk
    print("\n".join(print_shift_buff), file= open('images_to_shift.txt', "w"))


###################################
# Utility function to move images #
###################################

def move_files_to_folder(list_of_files, destination_folder):
    
    for f in list_of_files:
        try:
            shutil.move(f, destination_folder)
        except:
            print(f)
            assert False


########################
# Define Main Function #
########################

def main():

    images_folder = 'path/to/images'
    annotations_folder = 'path/to/labels'

    # Convert all json files and save the annotations
    convert_all_files(images_folder, annotations_folder)

    ## Partition the Dataset

    # Read images and annotations
    images = [os.path.join(images_folder, x) for x in os.listdir(images_folder)]
    annotations = [os.path.join(annotations_folder, x) for x in os.listdir(annotations_folder) if x[-3:] == "txt"]

    images.sort()
    annotations.sort()

    # Split the dataset into train-valid-test splits (60%, 20%, 20%)
    train_images, val_images, train_annotations, val_annotations = train_test_split(images, annotations, test_size = 0.4, random_state = 1)
    val_images, test_images, val_annotations, test_annotations = train_test_split(val_images, val_annotations, test_size = 0.5, random_state = 1)

    # create the folders to hold the newly split data
    try:
        os.makedirs("create/folder/images/train")
        os.makedirs("create/folder/images/val")
        os.makedirs("create/folder/images/test")

        os.makedirs("create/folder/labels/train")
        os.makedirs("create/folder/labels/val")
        os.makedirs("create/folder/labels/test")

    except BaseException as e:
        print('ERROR:\n' + str(e))

    # Move the splits into their folders
    move_files_to_folder(train_images, 'path/to/images/train/')
    move_files_to_folder(val_images, 'path/to/images/val/')
    move_files_to_folder(test_images, 'path/to/images/test/')
    move_files_to_folder(train_annotations, 'path/to/labels/train/')
    move_files_to_folder(val_annotations, 'path/to/labels/val/')
    move_files_to_folder(test_annotations, 'path/to/labels/test/')



if(__name__ == "__main__"):
    main()