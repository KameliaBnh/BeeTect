# Deep Learning Applications for Automated Pollinator Monitoring in Thailand

## Group Project MsC Applied Bioinformatics - Cranfield University 2022/2023

Insect pollinators are crucial for pollinating both wild and crop plants, but their populations are declining rapidly. Limited research has been conducted to assess the impact of habitat changes on pollinator abundance and diversity, particularly in tropical regions. Image-based technologies have provided a cost-effective and non-invasive method for insect monitoring, but data extraction can be time-consuming, especially for large datasets. Our study proposes using deep learning techniques, specifically, the You Only Look Once (YOLO) algorithm, to develop a tool for bee monitoring in single and multiple-batch field analysis and to investigate whether there exist differences in bee counts between organic and conventional fields. We trained our YOLOv5-based models using annotated images from organic and conventional guava farms in central Thailand. Our best YOLOv5 model achieved an average precision of 88.7% and recall of 84.9%, classifying eight important bee species. Our results showed no significant differences between the two field types. 


## Conda environement

#### Install conda and dependencies

1. Install Miniconda/Anaconda (if you don't already have)

2. Open the terminal and write the following commands:

```
conda create -n GUI-env python=3.9.13       # create new virtual env
conda activate GUI-env                      # activate environment in terminal
pip install -r requirements.txt             # install requirements
```

#### Running the script from the command line

3. Run the main.py script from the BPT_Cranfield/GUI folder by using this command:

```
python src/main.py
```
The GUI then opens and you can follow the steps in the next section.

## Use of the GUI

**Before opening the GUI, you should download the weights for the given models in the right folders. Indeed, the '.pt' files are too heavy to be shared on GitHub! You will find a '.txt' file for each model (Named with the following convention: 'Weights_*Name_of_the_Model*') in the 'models' folder containing a link to download the corresponding weights. This step has to be done first before carrying on with the BeeTect app!**

**You can also find the four provided weights to download in the following folder: https://www.dropbox.com/sh/0gsjrr63c385us4/AABUp3cplmssdUmVpY3SzwjJa?dl=0**

#### Entering the user information

Once the BeeTect app (GUI) is launched (for the first time), a form asking for the user information pops up:

<img width="277" alt="image" src="https://user-images.githubusercontent.com/126243509/230937591-4bfe59d7-85d8-485b-ad49-e005500efbdd.png">

Enter the required (and optional) information and click on the 'Submit' button.
The next time you will open the BeeTect app, your information will be saved and you will not need to fill this form again.

#### Change User

If several persons are working on the same project, it is possible to switch users in the BeeTect app:

<img width="208" alt="image" src="https://user-images.githubusercontent.com/126243509/232086518-1d821aea-8c27-494c-9b93-519e1b59982e.png">

#### Creating or opening a project

Then, you will see the following window: 

<img width="567" alt="image" src="https://user-images.githubusercontent.com/126243509/232086712-60ea2cf4-afb5-4e85-874a-5501184245ca.png">

There are different options for you to use here:

* To create a new project, open the 'File' menu item, and select 'New Project':

<img width="268" alt="image" src="https://user-images.githubusercontent.com/126243509/230937968-72e3f121-f9d0-4860-82bb-2b70349cbf16.png"> <img width="252" alt="image" src="https://user-images.githubusercontent.com/126243509/233342401-bbaf63c5-b5b4-4595-aac4-479c1a33846a.png">

All the projects will be saved in the 'projects' folder.

* To open an existing project, use the 'Open Project' option in the 'File' menu:

<img width="265" alt="image" src="https://user-images.githubusercontent.com/126243509/230938342-c92f6297-c6e0-486f-92aa-a70682bdec45.png">

* There is also the possibility to access the five last opened projects from the 'File' menu:

<img width="266" alt="image" src="https://user-images.githubusercontent.com/126243509/230938719-d4e3e6c2-90f2-4cc7-a72b-869f06968331.png">

#### Loading images

* Once a project is opened, you have the possibility to either open a single image ('Open Image') or a folder containing several images ('Open Image Folder'). You can either do that from the 'File' menu or directly from the 'Visualisation Pane' by clicking on the corresponding buttons:

<img width="336" alt="image" src="https://user-images.githubusercontent.com/126243509/230938784-2acf10c6-031a-422d-8c44-a2b6aee33b69.png"> <img width="266" alt="image" src="https://user-images.githubusercontent.com/126243509/230938843-5ba3490d-1b51-4c91-91dc-76888e033327.png">

#### Selecting the YOLOv5 model

* To select the YOLO model you want to use, choose an existing one in the dropdown menu. If you want to add your own YOLO model (trained before hand), you can do that bu selecting the 'Add New Model' button. A dialog will open where you can choose the name of the model, and browse through your computer to seect the weights corresponding to the model:

<img width="150" alt="image" src="https://user-images.githubusercontent.com/126243509/232087311-0b8d247a-af28-4bb1-9872-504f2f354216.png"> <img width="277" alt="image" src="https://user-images.githubusercontent.com/126243509/230938967-3a3b9c05-2385-4237-b27a-d3e83c8edb1a.png">

You can also select supplementary files for the model summary in the HTML report exported to be more complete: the confusion matric .png file, the F1 curve .png file, the results .png file and the opt.yaml file containing the YOLO model parameters. To add these files, you have to check the box and browse through your files via the file dialogs.

When a new model is added, the dropdown menu showing the available models automatically updates itself.

#### Results /  Batch folder

* It is also mandatory to select a 'Batch folder' before testing the selected model on the selected images (You will not be able to start the detection if a folder has not been selected first): to do that, click on the 'Select Batch Folder' button in the main window:

<img width="182" alt="image" src="https://user-images.githubusercontent.com/126243509/230939381-e16cd402-39ac-47cb-a375-48b9e5467f42.png">


Once all of these steps are done, you can click on the 'Start Detection' button. 

<img width="190" alt="image" src="https://user-images.githubusercontent.com/126243509/230941331-12fe7827-8faa-4761-9126-2d14f21a6d15.png">


## Results and HTML Reports

#### Individual Batch Results

The results will be saved in the selected fodler, along with a 'results.txt' file containing the data for each image, and an HTML report with statistics, graphs and details on the model and on the batch of images.

The images with bounding boxes for the detected pollinators (along with a .json file of the same name), are also saved in different subfolders in the selected folder:
* 'No-Pollinator' folder: the images that don't contain any pollinators.
* 'Pollinator' folder: the images containing at least one pollinator.
    * A subfolder with the name of the detected species is created for each pollinator detected on an image: if there is only one pollionator on an image, it will be saved in that subfolder.
    * If there are more than one pollinator on an image, it will be saved in the 'Multiple-Pollinators' subfolder.
    
The HTML report name after the batch is saved in the selected folder.

To have a quick summary of the results, you can check the 'Statistics' pane in the GUI:

<img width="568" alt="image" src="https://user-images.githubusercontent.com/126243509/231149237-73aad710-9aa5-45ab-aa06-5fbcb4f4c9e6.png">

There is a summary of the statistics calculated for the current batch, a summary of the model and two representative graphs.

#### Multiple Batches Comparison Results

To compare different batches from the same project, you can select the 'Export Batch Report' button in the menu bar:

<img width="262" alt="image" src="https://user-images.githubusercontent.com/126243509/230942515-d4d2022f-0563-4fe7-8285-748c85e911e3.png">

It will open a file dialog for you to select multiple batches to be compared:

<img width="354" alt="image" src="https://user-images.githubusercontent.com/126243509/230942625-e8289917-43bb-4679-9e4d-4c8e3e294071.png">

Once you submit the batches you want to comapre, an HTML report will be generated with statistical comaprison of the selected batches.



## Requirements

* python 3.9.13
* opencv-python 4.7.0.72
* PySide2 5.15.2.1
* torch 2.0.0
* torchvision 0.15.1
* matplotlib 3.7.1
* numpy 1.24.2
* pandas 1.5.2
* PyYAML 6.0
* scipy 1.10.1
* seaborn 0.12.2
* psutil 5.9.4
* tqdm 4.65.0
* gitdb 4.0.10
* gitpython 3.1.31
* smmap 5.0.0
* scikit-posthocs 0.7.0
* pandas 1.5.2 (not the latest version)
