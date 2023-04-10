# Deep Learning Applications for Automated Pollinator Monitoring in Thailand

## Group Project MsC Applied Bioinformatics - Cranfield University 2022/2023

In recent years, computer vision and deep learning has become a vital component in monitoring the health of bee colony and their behaviour. In this project we aim to build a deep learning detecting model which enables researchers to better understand the health of honeybee colony in Thailand. Previously, we implemented object detection model using YOLO-v5 for detection and classification of rare and common bee species using a dataset including ~1000 ground truth images from year 2021. This model was later validated on an alternative dataset form year 2022, the results show that the detector performs relatively well (with or without pollinator). However, we strive to further optimize our YOLO-V5 model by increasing our ground truth data, including data collected from year 2022, as well as implementing data augmentation for minority classes alongside hyperparameter evolution tunning. Thus, to build a stand-alone user-friendly application for future use in bee monitoring systems.  


## Conda environement

#### Install conda and dependencies

1. Install Miniconda/Anaconda (if you don't already have)

2. Open the terminal and write the following commands:

```
conda create -n GUI-env python=3.9.13       # create new virtual env
conda activate GUI-env                      # activate environment in terminal
pip install -r https://raw.githubusercontent.com/ultralytics/yolov5/master/requirements.txt # install Yolov5 requirements
pip install -r requirements.txt             # install requirements
```

#### Running the script from the command line

3. Run the main.py script from the BPT_Cranfield/GUI folder by using this command:

```
python src/main.py
```
The GUI then opens and you can follow the steps in the next section.

## Use of the GUI

#### Entering the user information

Once the BeeTect app (GUI) is launched (for the first time), a form asking for the user information pops up:

<img width="277" alt="image" src="https://user-images.githubusercontent.com/126243509/230937591-4bfe59d7-85d8-485b-ad49-e005500efbdd.png">

Enter the required (and optional) information and click on the 'Submit' button.
The next time you will open the BeeTect app, yout information will be saved and you will not need to fill this form again.

#### Creating or opening a project

Then, you will see the following window: 

<img width="568" alt="image" src="https://user-images.githubusercontent.com/126243509/230937830-09084b2e-e66a-455b-8e26-3da5be9fd606.png">

There are different options for you to use here:

* To create a new project, open the 'File' menu item, and select 'New Project':

<img width="268" alt="image" src="https://user-images.githubusercontent.com/126243509/230937968-72e3f121-f9d0-4860-82bb-2b70349cbf16.png"> <img width="252" alt="image" src="https://user-images.githubusercontent.com/126243509/230938062-5c29a169-515d-43c0-aeb1-d9b2f2813fcd.png">

All the projects have to be saved in the 'projects' folder.

* To open an existing project, use the 'Open Project' option in the 'File' menu:

<img width="265" alt="image" src="https://user-images.githubusercontent.com/126243509/230938342-c92f6297-c6e0-486f-92aa-a70682bdec45.png">

* There is also the possibility to access the five last opened projects from the 'File' menu:

<img width="266" alt="image" src="https://user-images.githubusercontent.com/126243509/230938719-d4e3e6c2-90f2-4cc7-a72b-869f06968331.png">

#### Loading images

* Once a project is opened, you have the possibility to either open a single image ('Open Image') or a folder containing several images ('Open Image Folder'). You can either do that from the 'File' menu or directly from the 'Visualisation Pane' by clicking on the corresponding buttons:

<img width="336" alt="image" src="https://user-images.githubusercontent.com/126243509/230938784-2acf10c6-031a-422d-8c44-a2b6aee33b69.png"> <img width="266" alt="image" src="https://user-images.githubusercontent.com/126243509/230938843-5ba3490d-1b51-4c91-91dc-76888e033327.png">

#### Selecting the YOLOv5 model

* To select the YOLO model you want to use, choose an existing one in the dropdown menu. If you want to add your own YOLO model (trained before hand), you can do that bu selecting the 'Add New Model' button. A dialog will open where you can choose the name of the model, and browse through your computer to seect the weights corresponding to the model:

<img width="187" alt="image" src="https://user-images.githubusercontent.com/126243509/230938922-f407da93-4e72-4054-9fe4-5562dbc76288.png"> <img width="277" alt="image" src="https://user-images.githubusercontent.com/126243509/230938967-3a3b9c05-2385-4237-b27a-d3e83c8edb1a.png">

You can also select supplementary files for the model summary in the HTML report exported to be more complete: the confusion matric .png file, the F1 curve .png file, the results .png file and the opt.yaml file containing the YOLO model parameters. To add these files, you have to check the box and browse through your files via the file dialogs.

#### Results /  Batch folder

* It is also mandatory to select a 'Batch folder' before testing the selected model on the selected images: to do that, click on the 'Select Batch Folder' button in the main window:

<img width="182" alt="image" src="https://user-images.githubusercontent.com/126243509/230939381-e16cd402-39ac-47cb-a375-48b9e5467f42.png">


Once all of these steps are done, you can click on the 'Start Detection' button. 

<img width="190" alt="image" src="https://user-images.githubusercontent.com/126243509/230941331-12fe7827-8faa-4761-9126-2d14f21a6d15.png">


## Results and HTML Reports

#### Individual Batch Results

The results will be saved in the selected fodler, along with a 'results.txt' file containing the data for each image, and an HTML report with statistics, graphs and details on the model and on the batch of images.

The images with bounding boxes for the detected pollinators (along with a .json file of the same name), are also saved in different subfolders in the selected folder:
* 'No-Pollinator' folder: the images that don't contain any pollinators.
* 'Pollinator' folder: the images containing at least one pollinator.
    ** A subfolder with the name of the detected species is created for each pollinator detected on an image: if there is only one pollionator on an image, it will be saved in that subfolder.
    ** If there are more than one pollinator on an image, it will be saved in the 'Multiple-Pollinators' subfolder.
    
The HTML report name after the batch is saved in the selected folder.

#### Multiple Batches Comparison Results





## Requirements

* python 3.9.13
* opencv-python 4.7.0.72
* PySide2 5.15.2.1
* torch 2.0.0
* torchvision 0.15.1
* matplotlib 3.7.1
* numpy 1.24.2
* PyYAML 6.0
* scipy 1.10.1
* seaborn 0.12.2
