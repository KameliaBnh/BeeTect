from IPython.display import HTML
from numpy import var
import yaml
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import random
import scipy.stats as stats
from scipy.stats import shapiro
import warnings

from PySide2.QtWidgets import QApplication
import sys

# Import the main window object (mw) to access variables
import MainWindow as mw

# Create the Qt application
app = QApplication(sys.argv)

# Create an object for the main window
main_window = mw.MainWindow()

warnings.filterwarnings("ignore", message="this method is deprecated")

# Path of the text file storing the preferences of the user
user_info_path = os.path.join(os.getcwd(), 'user_info.txt')

# Load the YAML data from the folder corresponding to the currently selected model
with open(os.path.join(main_window.Models.path, main_window.ui.comboBox.currentText(), 'opt.yaml'), 'r') as f:
    data = yaml.safe_load(f)

# Extract the relevant information for the model summary
epochs = data['epochs']
batch_size = data['batch_size']
imgsz = data['imgsz']
optimizer = data['optimizer']
Momentum = data['hyp']['momentum']
Weight_decay= data['hyp']['weight_decay']

# Create a DataFrame to store the summary
summary_df = pd.DataFrame({
    'Number of Epochs': [epochs],
    'Batch Size': [batch_size],
    'Image Size': [imgsz],
    'Optimizer': [optimizer],
    'Momentum':[Momentum],
    'Weight Decay':[Weight_decay]
})
summary_df = summary_df.rename(index={0: ''})

# To read the User Information
with open(user_info_path) as f:
    lines = f.readlines()
    first_name = lines[1].split(':')[1].strip()
    last_name = lines[2].split(':')[1].strip()
    email = lines[3].split(':')[1].strip()
    project_creation = lines[4]
    project_name =lines[8].split(':')[1].strip()

full_user_name = first_name + ' ' + last_name

# Path of the text file storing the YOLO detection results
results_path = os.path.join(main_window.Batches[0].path, 'results.txt')

#creating a directory to save all the output graphs 
output_directory = os.path.join(main_window.Batches[0].path, 'Output_Graphs')
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Getting the results summary 

with open(results_path) as f:
        bee_counts = {"amegilla":0, "ceratina":0, "meliponini":0, "xylocopa_aestuans":0, "pollinator":0, "apis":0, "unknown":0, "apis_cerana":0, "apis_florea":0} # creating empty dictionary to store the counts 
        per_image_counts={}
        no_detection_images=0
        image_no=[]
      
        for line in f:
            line = line.strip() # stripping the line of any white space 
            if line.startswith('image'): # ignore lines that do not start with the word image
                
                img_no = line.split(':',1)[0].strip()
                img_no = img_no.split(' ',1)[1]
                img_no = img_no.split('/',1)[0].strip()
                image_no.append(img_no)
                

                img_part = line.split(':',1)[1].strip() # split the line based on the first colon encountered 
                parts = img_part.split(' ',1) #splitting the line further based on space to get just the bee counts
                image_size = parts[0] # the image size is stored in the image_size variable 
                species_counts = parts[1] 

                if species_counts == "(no detections)":
                    no_detection_images+=1
                    
                else:
                    species_counts = species_counts.split(', ') # all the species counts are splitted based on the comma 
                    
                    species_dict = {}
                    for bee in species_counts:
                        
                        parts = bee.split(' ') ## split the counts based on space 
                        count = int(parts[0])
                        species_name = ' '.join(parts[1:]) 
                        
                        if species_name.endswith("amegillas"):
                            species_name = "amegilla"

                        if species_name.endswith("apis_ceranas"):
                            species_name = "apis_cerana"
                        
                        if species_name.endswith("apis_floreas"):
                            species_name = "apis_florea"

                        if species_name.endswith("ceratinas"):
                            species_name = "ceratina"

                        if species_name.endswith("meliponinis"):
                            species_name = "meliponini"

                        if species_name.endswith("xylocopa_aestuanss"):
                            species_name = "xylocopa_aestuans"

                        if species_name.endswith("pollinators"):
                            species_name = "pollinator"

                        if species_name.endswith("unknowns"):
                            species_name = "unknown"

                        if species_name in bee_counts:
                            bee_counts[species_name.lower()] = bee_counts.get(species_name.lower(), 0) + count

                        species_dict[species_name.lower()] = count 

                    per_image_counts[img_no] = species_dict

filtered_counts = {k:v for k,v in bee_counts.items() if v > 0}


# Getting the number of input Images 
# converting the strings of numbers into integers to calculate max value 
numbers = [int(n) for n in image_no] 
no_input_img= max(numbers)

# Getting the bee species with the highest counts 
max_key = max(filtered_counts, key=lambda k: filtered_counts[k])
max_value = max(filtered_counts.values())

# Finding the bee species which has the lowest counts
min_key = min(filtered_counts, key=lambda k: filtered_counts[k])
min_value = min(filtered_counts.values())


##Creating a table with the above information
#create data
data = [["Number of Input Images","-", no_input_img], 
        ["Number of Images with no Detections","-",no_detection_images],
        ["Highest Bee Species Counts",max_key,max_value],
        ["Lowest Bee Species Counts",min_key,min_value]]

#define header names
col_names = ["Metric","Species Name", "Value"]

#Saving the Information in a dataframe 
overview_df =pd.DataFrame(data, columns=col_names)

#Storing the bee counts in a dataframe 
df = pd.DataFrame(list(filtered_counts.items()), columns=['Species', 'Occurence'])

#Creating a bar chart
colors = plt.cm.Set1(np.linspace(0, 1, len(df['Species'])))
color_dict = dict(zip(df['Species'], colors))
ax = df.plot.bar(x='Species', y='Occurence', rot=0, color=[color_dict[s] for s in df['Species']], legend=False)
ax.set_xlabel('Species')
ax.set_ylabel('Counts')
ax.set_title('Bee Species Counts')
ax.set_xticklabels(df['Species'])
plt.savefig(f'{output_directory}/Bar_plot.png', dpi=700)
plt.close()


#creating dataframe to store species abundance
total_count = df['Occurence'].sum()

df['Abundance'] = df['Occurence'] / total_count
df['Abundance'] = df['Abundance'].round(2)


#creating a pie chart depicting species abundance 
species_names = list(filtered_counts.keys())
species_counts = list(filtered_counts.values())
fig,ax= plt.subplots()
ax.pie(species_counts, labels=species_names, autopct='%1.1f%%')
ax.set_title('Bee Species Abundance')
fig.savefig(f'{output_directory}/bee_species_counts.png', dpi=700)
plt.close()


##Normality Checks 
#1) histogram 
df.hist(column='Occurence', bins=10, grid=False)

# Add labels and title
plt.title('Histogram of Bee Counts')
plt.xlabel('Count')
plt.ylabel('Frequency')
plt.savefig(f'{output_directory}/Normality_check.png', dpi=700)
plt.close()


##2) Q-Q plots 

bee_counts = df['Occurence']
stats.probplot(bee_counts, plot=plt)
plt.title('Q-Q Plot of Bee Counts')
plt.savefig(f'{output_directory}/Q-Q_Plot.png', dpi=700)
plt.close()

##3)Perform the Shapiro-Wilk test for normality
stat, p = shapiro(bee_counts)
alpha = 0.05
results_df = pd.DataFrame({'Test Statistic': [stat], 'p-value': [p]})
results_df = results_df.rename(index={0: ''})


if p > alpha:
    Output1 = " Conclusion: The data is normally distributed. Performing further parametric tests."   

    ##If the data is normally distributed performing parametric tests 
    ##performing independent t-tests


#path to the output folders
output_path = os.path.join(main_window.Batches[0].path, 'Pollinator')
subfolders = [f.path for f in os.scandir(output_path) if f.is_dir()]
random_image_paths = []

# Loop through each subfolder
for subfolder in subfolders:
    # Get a list of all image files within the subfolder
    image_files = [f for f in os.listdir(subfolder) if f.lower().endswith(".jpg")]
    # Choose a random image from the list
    if image_files:
        random_image = random.choice(image_files)
        # Display the path to the random image
        random_image_path = os.path.join(subfolder, random_image)
        
        random_image_paths.append(random_image_path)
    else:
        print("")





# creating html 

#The Quick Links Section
toc_html = f"""
 <div class="quick-links">
 <nav>
        <a href="#yolo-results">YOLO Results</a>
        <a href="#statistics-summary">Statistics Summary</a>
        <a href="#model-summary">Model Summary</a>
        <a href="#output-examples">Output Examples</a>
 </nav>
 </div>
"""

#The User Information section
user_info_html="""
    <div class="user_section" id="User_info">
        <h1 style="margin-left: 490px; width: 50%; height: 20px;">User Information</h1>
        <p style="margin-left: 730px; width: 50%;">
        Username: {0}<br>
        Email: {1}<br>
        Project Name: {2}<br>
        {3}
        </p>
    </div>

""".format(full_user_name, email, project_name, project_creation)


#Contains the Yolo Results and Statistics Summary
section1_html="""
    <a id="yolo-results"></a>
    <div class="section1" id="YOLO-results">
        <h1 style="margin-left: 10px; margin-top: 90px; font-size: 24px; border: 1px solid khaki; padding: 10px; background-color: Teal; color: white;">YOLO Results</h1>
        <h1 style="margin-left: 60px; margin-top: 30px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;"> Species Counts and Abundance Summary</h1>
    </div>


    <div class="flex-container" style="margin-left:200px; margin-top:70px;">
        <div class="flex-item" style="flex-basis: 50%;">{0}</div>
        <div class="flex-item" style="flex-basis: 50%;">{1}</div>
    </div>

    
    <div class="section1" id="YOLO-results">
        <h1 style="margin-left: 60px; margin-top: 70px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;">Visualizing Species Counts and Abundance</h1>
    </div>

    
    <div class="flex-container" style="margin-left:150px; width:1200px; margin-top: 50px;">
        <div class="flex-item" style="flex-basis: 50%;"><img src="{2}/Bar_plot.png" style="width: 600px; height: 500px;">
        </div>
        <div class="flex-item" style="flex-basis: 50%;">
            <img src="{3}/bee_species_counts.png" style="width: 650px; height: 600px;">
        </div>
    </div>

    
    <a id="statistics-summary"></a>
    <div class="section2" id="statistics-summary">
        <h1 style="margin-left: 10px; margin-top: 90px; font-size: 24px; border: 1px solid khaki; padding: 10px; background-color: Teal; color: white;">Statistics Summary</h1>
        <h1 style="margin-left: 60px; margin-top: 30px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;">Histogram and Q-Q Plot: Assessing Normal Distribution</h1>
    </div>


    <div class="flex-container" style="margin-left:150px; width:1200px; margin-top: 50px;">
        <div class="flex-item" style="flex-basis: 50%;"><img src="{4}/Normality_check.png" style="width: 600px; height: 500px;">
        </div>
        <div class="flex-item" style="flex-basis: 50%;">
            <img src="{5}/Q-Q_Plot.png" style="width: 600px; height: 500px;">
        </div>
    </div>

    
     <div class="section1" id="statistics-summary">
        <h1 style="margin-left: 60px; margin-top: 70px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;">Checking for Normality: Shapiro-Wilk Test</h1>
    </div>
    

    <div class="section1" id="statistics-summary">
        <div class="shapiro-test" style="margin-left:90px; margin-top:40px;">{6}</div>   
        <div class="shapiro-test" style="width:680px; margin-left:90px; margin-top:30px; background-color: lightgrey; font-size: 18px;">{7}</div> 
    </div>
    
    """.format(overview_df.style.set_table_styles([{'selector': 'th', 'props': [ ('font-size', '20px'), ('text-align', 'center'), ('color', 'black'), ('background-color', 'lightblue'), ('font-weight', 'bold'),('padding', '5px'), ('border', '1px solid black')]
    }, {'selector': 'td','props': [('font-size', '20px'),('padding', '5px'), ('border', '1px solid black'), ('text-align', 'center')]}]).hide_index().render(),df.style.set_table_styles([{'selector': 'th', 'props': [ ('font-size', '20px'), ('text-align', 'left'), ('color', 'black'), ('background-color', 'lightblue'), ('font-weight', 'bold'),('padding', '5px'), ('border', '1px solid black')]
    }, {'selector': 'td','props': [('font-size', '20px'), ('padding', '5px'),  ('border', '1px solid black')]}]).hide_index().render() ,output_directory,output_directory,output_directory,output_directory,
    results_df.style.set_table_styles([{'selector': 'th', 'props': [ ('font-size', '16px'), ('text-align', 'center'), ('color', 'black'), ('background-color', 'lightblue'), ('font-weight', 'bold'),('padding', '5px'), ('border', '1px solid black')]
    }, {'selector': 'td','props': [('font-size', '25px'), ('padding', '5px'),  ('border', '1px solid black')]}]).hide_index().render(), Output1)


# If the data distribution is normal
if p>alpha:
    parametric_html = """
        <div class="section1" id="statistics-summary">
            <h1 style="margin-left: 60px; margin-top: 30px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;"> Levene's Test - Checking Equality of Variance</h1>
            <div class="Levene's-test" style="margin-left:90px; margin-top:40px;">{0}</div>   
            <div class="Levene's-test" style="width:680px; margin-left:90px; margin-top:30px; background-color: lightgrey; font-size: 18px;"></div> 
            <h1 style="margin-left: 60px; margin-top: 30px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;"> Independent T-Test</h1>
            <div class="t-test" style="margin-left:90px; margin-top:40px;"></div>   
            <div class="t-test" style="width:680px; margin-left:90px; margin-top:30px; background-color: lightgrey; font-size: 18px;"></div> 
            <div><p style="margin-left: 50px; margin-right: 20px;"><img src="" width="500" height="500"></p></div>
        </div>
    """.format(output_directory)

# If the data distribution is not normal
else:
    non_parametric_html ="""

        <div class="section1" id="statistics-summary">
            <h1 style="margin-left: 60px; margin-top: 30px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;"> Mann-Whitney U Test</h1>
            <div class="Mann U-test" style="margin-left:90px; margin-top:40px;">{0}</div>   
            <div class="Mann U-test" style="width:680px; margin-left:90px; margin-top:30px; background-color: lightgrey; font-size: 18px;"></div> 
            <div><p style="margin-left: 50px; margin-right: 20px;"><img src="" width="500" height="500"></p></div>
    """.format(output_directory)
        

# Contains the Model Summary 
section2_html = """
    <a id="model-summary"></a>
    <div class="section2" id="Model-summary">
        <h1 style="margin-left: 10px; margin-top: 90px; font-size: 24px; border: 1px solid khaki; padding: 10px; background-color: Teal; color: white;">Model Summary</h1>
        <h1 style="margin-left: 60px; margin-top: 30px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;">Optimized Parameters for YOLO Model Performance</h1>
    </div>


    <div class="flex-container" style="margin-left:200px; margin-top:60px;">
        <div class="flex-item" style="flex-basis: 100%;">{0}</div>
    </div>

    
    <div class="section2" id="Model-summary">
        <h1 style="margin-left: 60px; margin-top: 90px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;">Performance Graphs for YOLO Model Training</h1>
    </div>

    <div class="section2">
         <div><p style="margin-left: 180px; margin-top: 100px;"><img src="yolov5/results.png" width="1000" height="1000"></p></div>
         <div><p style="margin-left: 180px; margin-top: 100px;"><img src="yolov5/F1_curve.png" width="1000" height="1000"></p></div>
         <div><p style="margin-left: 55px; margin-top: 100px;"><img src="yolov5/confusion_matrix.png" width="1000" height="1000"></p></div>
    </div>

    
    <a id="output-examples"></a>
    <div class="section2" id="Output Examples">
        <h1 style="margin-left: 10px; margin-top: 90px; font-size: 24px; border: 1px solid khaki; padding: 10px; background-color: Teal; color: white;">Output Examples</h1>
        <h1 style="margin-left: 60px; margin-top: 30px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;">Detection of Bees using YOLO</h1>
    </div>


""".format(summary_df.style.set_table_styles([{'selector': 'th', 'props': [ ('font-size', '20px'), ('text-align', 'center'), ('color', 'black'), ('background-color', 'lightblue'), ('font-weight', 'bold'),('padding', '5px'), ('border', '1px solid black')]
    }, {'selector': 'td',
        'props': [
            ('font-size', '24px'),
            ('padding', '5px'), ('border', '1px solid black'), ('text-align', 'center')]
    }]).hide_index().render())


# Contains the Output Example Images
section3_html = '<div style="display: flex; flex-wrap: wrap; margin-top: 60px;">'
for i, path in enumerate(random_image_paths):
    # Extract subfolder name from image path
    subfolder_name = os.path.basename(os.path.dirname(path))
    section3_html += f'<p style="margin-left: 165px;"><img src="{path}" title="{subfolder_name}" width="500" height="500"></p>'

section3_html += '</div>'



# Define HTML with table of contents and sections
if p>alpha:
    html = f"""
        <html>
        <head>
            <title>YOLO Statistics Report</title>
                <style>
                
                    .flex-container {{
                        display: flex;
                        align-items: center;
                        justify-content: space-between;
                        }}

                    .flex-item {{
                        margin-left: -108px;
                        }}
                    
                    .header {{
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        background-color: lightblue;
                        padding: 10px;
                        flex-shrink: 0;
                        }}

                    .user_section {{
                        text-align: right;
                        margin-right: 130px;
                        font-size: 15px;
                        flex-shrink: 0;
                        }}    

                    .quick-links nav a {{
                        text-align: center;
                        padding: 14px 16px;
                        background-color:  #F5F5DC; 
                        color: black !important;
                        font-size: 15px;
                        }}

                    .quick-links nav a:hover {{
                        background-color: lightgrey;
                        }} 
                </style>

        </head>
        <body>
        <div class="header">
            <h1>YOLO Statistics Report</h1>
            {user_info_html} 
        </div>     
            {toc_html}
                <div style="float:left; height:2500px;border-left:10px solid black; margin-left: -850px;"></div>
                        
                    {section1_html}
                    {parametric_html}
                    {section2_html}
                    {section3_html}
           
        </body>
        </html>
        """ 

else:
    html = f"""
        <html>
        <head>
            <title>YOLO Statistics Report</title>
                <style>
                
                    .flex-container {{
                        display: flex;
                        align-items: center;
                        justify-content: space-between;
                        }}
                   
                    .flex-item {{
                        margin-left: -108px;
                        }}
                    
                    .header {{
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        background-color: lightblue;
                        padding: 10px;
                        flex-shrink: 0;
                        }}

                    .user_section {{
                        text-align: right;
                        margin-right: 130px;
                        font-size: 15px;
                        flex-shrink: 0;
                        }}    

                    .quick-links nav a {{
                        text-align: center;
                        padding: 14px 16px;
                        background-color:  #F5F5DC; 
                        color: black !important;
                        font-size: 15px;
                        }}

                    .quick-links nav a:hover {{
                        background-color: lightgrey;
                        }}
                </style>

        </head>
        <body>
        <div class="header">
            <h1>YOLO Statistics Report</h1>
            {user_info_html} 
        </div>     
            {toc_html}
                <div style="float:left; height:2500px;border-left:10px solid black; margin-left: -850px;"></div>
                        
                    {section1_html}
                    {non_parametric_html}
                    {section2_html}
                    {section3_html}               
        </body>
        </html>
        """

##creating the html document 
with open("stats.html", "w") as f:
    f.write(html)


