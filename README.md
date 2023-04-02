# Deep Learning Applications for Automated Pollinator Monitoring in Thailand

## Group Project MsC Applied Bioinformatics - Cranfield University 2022/2023



## Conda environement

#### Install conda and dependencies

1. Install Miniconda/Anaconda

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

#### Entering the user information

Once the BeeDeteKt app (GUI) is launched (for the first time), a form asking for the user information pops up:

<img width="252" alt="image" src="https://user-images.githubusercontent.com/126243509/229311728-9885e759-4c02-4a7c-989e-36180e5ccb53.png">

Enter the required (and optional) information and click on the 'Submit' button.
The next time you will open the BeeDeteKt app, yout information will be saved and you will not need to fill this form again.

Then, you will see the following window: 

<img width="567" alt="image" src="https://user-images.githubusercontent.com/126243509/229311819-e307b137-b00a-48ee-94f3-406e924b8a8e.png">

There are different options for you to use here:

* To create a new project, open the 'File' menu item, and select 'New Project':

<img width="172" alt="image" src="https://user-images.githubusercontent.com/126243509/229368830-3c38e79f-7e5a-4919-ac87-2af8f11cc654.png"> <img width="252" alt="image" src="https://user-images.githubusercontent.com/126243509/229368842-05f56846-7016-4341-b52a-bc5232e8fb53.png">

* To open an existing project, use the 'Open Project' option in the 'File' menu:

<img width="168" alt="image" src="https://user-images.githubusercontent.com/126243509/229368864-42c6e8f2-b89f-45e7-85a3-159775106bfb.png">

* Once a project is opened, you have the possibility to either open a single image ('Open Image') or a folder containing several images ('Open Image Folder'). You can either do that from the 'File' menu or directly from the 'Visualisation Pane' by clicking on the corresponding buttons:

<img width="567" alt="image" src="https://user-images.githubusercontent.com/126243509/229368900-dd0854a3-5ab9-4424-a405-70f8022d1667.png">

* To select the YOLO model you want to use, choose an existing one in the dropdown menu. If you want to add your own YOLO model (trained before hand), you can do that bu selecting the 'Add New Model' button. A dialog will open where you can choose the name of the model, and browse through your computer to seect the weights corresponding to the model:

<img width="185" alt="image" src="https://user-images.githubusercontent.com/126243509/229368916-c4163b47-dedd-4db1-8960-7d3ffb0b6d61.png"> <img width="252" alt="image" src="https://user-images.githubusercontent.com/126243509/229368923-62485399-2c20-4c78-bfa5-dcbe5e8ccbe4.png">

* It is also mandatory to select a 'Batch folder' before testing the selected model on the selected images: to do that, click on the 'Select Batch Folder' button in the main window:

<img width="243" alt="image" src="https://user-images.githubusercontent.com/126243509/229368948-3a4cfc31-2225-4aa8-bf02-42766e38baf2.png">


Once all of these steps are done, you can click on the 'Start Detection' button. The results will be saved in the selected fodler, along with a 'results.txt' file containing the data for each image, and an HTML report with statistics, graphs and details on the model and on the batch of images.


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
