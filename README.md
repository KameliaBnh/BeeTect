# Deep Learning Applications for Automated Pollinator Monitoring in Thailand

## Group Project MsC Applied Bioinformatics - Cranfield University 2022/2023

Note: ctrl + shift + v to have preview of the readme file

Note: shift + alt + f to convert the .json file to have a data frame format

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

Once the GUI is launched, a form asking for the user information pops up:



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
