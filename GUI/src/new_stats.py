import os 
import shutil
import random
import seaborn as sns
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import yaml
import base64
import warnings
warnings.filterwarnings("ignore", message="this method is deprecated")


path = "C:/Users/benha/Documents/Cranfield/Group_Project/BPT_Cranfield/GUI/projects/newProject/exp1/Pa_Toy.txt"

# Creating a function to extract the bee counts from each results.txt file
def read_results(file_path):
    with open(file_path) as f:
            bee_counts = {"amegilla":0, "ceratina":0, "meliponini":0, "xylocopa_aestuans":0, "pollinator":0, "apis":0, "unknown":0, "apis_cerana":0, "apis_florea":0} # creating empty dictionary to store the counts 
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

                        

    filtered_counts = {k:v for k,v in bee_counts.items() if v > 0}
    return (filtered_counts, no_detection_images, image_no)

filtered_counts, no_detection_images, image_no = read_results(path)



# Path of the text file storing the preferences of the user
user_info_path = os.path.join(os.getcwd(), 'user_info.txt')


# Getting the user information 
with open(user_info_path) as f:
    lines = f.readlines()
    first_name = lines[1].split(':')[1].strip()
    last_name = lines[2].split(':')[1].strip()
    email = lines[3].split(':')[1].strip()
    Date = lines[4].split(':')[1].strip()
    Time = lines[5].split(":", 1)[1].strip()
    project_name = lines[8].split(":")[1].strip()
    Project_path = lines[9].split(":", 1)[1].strip()

full_user_name = first_name + ' ' + last_name

#path to the selected model
model_path = "C:/Users/benha/Documents/Cranfield/Group_Project/BPT_Cranfield/GUI/models/YOLO_v5_2022"

file_paths = []
if os.path.isfile(os.path.join(model_path, 'results.png')):
    file_paths.append(os.path.join(model_path, 'results.png'))
if os.path.isfile(os.path.join(model_path, 'confusion_matrix.png')):
    file_paths.append(os.path.join(model_path, 'confusion_matrix.png'))
if os.path.isfile(os.path.join(model_path, 'F1_curve.png')):
    file_paths.append(os.path.join(model_path, 'F1_curve.png'))


#Creating a function to style the tables 
def create_styled_table(df):
    styled_table = df.style.set_table_styles([{'selector': 'th', 'props': [ ('font-size', '24px'), ('text-align', 'center'), ('color', 'black'), ('background-color', 'lightblue'), ('font-weight', 'bold'),('padding', '20px'), ('border', '1px solid black'), ('border-collapse','collapse !important')]}, {'selector': 'td','props': [('font-size', '20px'),('padding', '15px'), ('border', '1px solid black'), ('text-align', 'center')]}])
    html = styled_table.hide_index().render()
    return html


# Creating a function to encode the image data from a directory
def image_encode(directory,width, height):
    img_tags = []

    # get a list of all the image files in the directory
    img_files = [f for f in os.listdir(directory) if f.endswith('.png')]

    for img_file in img_files:
        with open(os.path.join(directory, img_file), 'rb') as f:
            image_bytes = f.read()

            # Encode image data as base64
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')

           # Create data URL for image
            image_data_url = f'data:image/png;base64,{image_base64}'

            # Generate HTML with embedded image
            images = f'<img src="{image_data_url}" alt="plot" style="width: {width}px; height: {height}px;" />'

            img_tags.append(images)
    return img_tags


# Creating a function to encode the image data from a list

def image_encode_list(image_paths, width, height):
    img_tags = []

    for img_path in image_paths:
        with open(img_path, 'rb') as f:
            image_bytes = f.read()

            #extracting subfolder name 
            subfolder_name = os.path.basename(os.path.dirname(img_path))

            # Encode image data as base64
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')

            # Create data URL for image
            image_data_url = f'data:image/png;base64,{image_base64}'

            # Generate HTML with embedded image
            images = f'<img src="{image_data_url}" title ="{subfolder_name}" style="width: {width}px; height: {height}px; margin-left: 165px; margin-top: 60px;" />'

            img_tags.append(images)
    return img_tags


# Checking if the opt.yaml file is provided to create a model summary dataframe 

if os.path.exists(os.path.join(model_path, 'opt.yaml')):
# Getting the Model Summmary 
    with open(os.path.join(model_path, 'opt.yaml'), 'r') as f:
        data = yaml.safe_load(f)

    # Extract the relevant information for the model summary
    epochs = data['epochs']
    batch_size = data['batch_size']
    imgsz = data['imgsz']
    optimizer = data['optimizer']
    Momentum = data['hyp']['momentum']
    Weight_decay= data['hyp']['weight_decay']
    Anchor = data['hyp']['anchor_t']
    learning_rate = data['hyp']['lr0']

    # Create a DataFrame to store the summary
    summary_df = pd.DataFrame({
        'Number of Epochs': [epochs],
        'Batch Size': [batch_size],
        'Image Size': [imgsz],
        'Optimizer': [optimizer],
        'Momentum':[Momentum],
        'Weight Decay':[Weight_decay],
        'Anchor':[Anchor],
        'Learning rate':[learning_rate]
    })


    html_summary =  create_styled_table(summary_df)



# Getting the bee species with the highest counts 
max_key = max(filtered_counts, key=lambda k: filtered_counts[k])
max_value = max(filtered_counts.values())

# Finding the bee species which has the lowest counts
min_key = min(filtered_counts, key=lambda k: filtered_counts[k])
min_value = min(filtered_counts.values())

##Creating a table with the above information
#create data
data = [["Number of Input Images","-", "950"], 
        ["Number of Images with no Detections","-",no_detection_images],
        ["Highest Bee Species Counts",max_key,max_value],
        ["Lowest Bee Species Counts",min_key,min_value]]

#define header names
col_names = ["Metric","Species Name", "Value"]


#Saving the Information in a dataframe 
counts_df =pd.DataFrame(data, columns=col_names)

#Storing the bee counts in a dataframe 
abundance_df = pd.DataFrame(list(filtered_counts.items()), columns=['Species', 'Occurence'])

#creating dataframe to store species abundance
total_count = abundance_df['Occurence'].sum()

abundance_df['Abundance'] = abundance_df['Occurence'] / total_count


# Displaying dataframes as a table 
html_counts = create_styled_table(counts_df)
html_abundance = create_styled_table(abundance_df)


# Getting the model performance graphs in encoded format
perform_graphs = image_encode_list(file_paths, 800, 600)

#Getting the names of the performance grphs
perform_graphs_names = []
for path in file_paths:
    name = os.path.basename(path)
    perform_graphs_names.append(name)

 

# Getting example images for each detected species 
output_path = os.path.join("C:/Users/benha/Documents/Cranfield/Group_Project/BPT_Cranfield/GUI/projects/newProject/exp1", 'Pollinator')
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

#creating a directory to save all the output graphs 
output_directory_single_batch = "C:/Users/benha/Documents/Cranfield/Group_Project/BPT_Cranfield/GUI/projects/newProject/exp1/Output_Graphs"
if not os.path.exists(output_directory_single_batch):
    os.makedirs(output_directory_single_batch)

#Creating a bar chart
colors = plt.cm.Set1(np.linspace(0, 1, len(abundance_df['Species'])))
color_dict = dict(zip(abundance_df['Species'], colors))
ax = abundance_df.plot.bar(x='Species', y='Occurence', rot=0, color=[color_dict[s] for s in abundance_df['Species']], legend=False)
ax.set_xlabel('Species')
ax.set_ylabel('Counts')
ax.set_title('Bee Species Counts')
ax.set_xticklabels(abundance_df['Species'])
plt.savefig(f'{output_directory_single_batch}/Bar_plot.png', dpi=700)
plt.close()


#creating a pie chart depicting species abundance 
species_names = list(filtered_counts.keys())
species_counts = list(filtered_counts.values())
print(species_counts)
print(species_names)
fig,ax= plt.subplots()
ax.pie(species_counts, labels=species_names, autopct='%1.1f%%')
ax.set_title('Bee Species Abundance')
plt.savefig(f'{output_directory_single_batch}/bee_species_counts.png', dpi=700)
plt.close()



img_tags = image_encode(output_directory_single_batch, 600, 600)
img_tags_list = image_encode_list(random_image_paths, 500, 500)

  
 #The quick links section 
toc_html = f"""
    <div class="quick-links">
    <nav>
            <a href="#output-examples">Output Examples</a>
            <a href="#Detection-results">Detection Results</a>
            <a href="#model-summary">Model Summary</a>
    </nav>
    </div>
    """


#The User Information section
user_info_html="""
    <div class="user_section" id="User_info">
        <h1 style="margin-left: 514px; width: 50%; height: 20px;">User Information</h1>
        <p style="margin-left: 514px; width: 50%; font-size: 17px;">
        Username: {0}<br>
        Email: {1}<br>
        Date: {2}<br>
        Time: {3}<br>
        </p>
    </div>

""".format(full_user_name, email, Date, Time)


#Heading contains the title of the sub-section
heading_html = """
<a id="output-examples"></a>
<div class="section2" id="Output Examples">
    <h1 style="margin-left: 10px; margin-top: 90px; font-size: 24px; border: 1px solid khaki; padding: 10px; background-color: Teal; color: white;">Output Examples</h1>
    <h1 style="margin-left: 60px; margin-top: 30px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;">Detection of Bees using YOLO Model</h1>
</div>
    """


#Section 1 contains the output example images 
section1_html = '<div style="display: flex; flex-wrap: wrap; margin-top: 30px;">'
for i, path in enumerate(img_tags_list):

    # Extract subfolder name from image path
    subfolder_name = os.path.basename(os.path.dirname(path))
    section1_html += f'{path}'

section1_html += '</div>'


# Section 2 contains the detection results 
section2_html="""
<a id="Detection-results"></a>
<div class="section1" id="Detection-results">
    <h1 style="margin-left: 10px; margin-top: 90px; font-size: 24px; border: 1px solid khaki; padding: 10px; background-color: Teal; color: white;">Detection Results</h1>
    <h1 style="margin-left: 60px; margin-top: 30px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;"> Species Counts and Abundance Summary</h1>
</div>


<div class="flex-container" style="margin-left:200px; margin-top:70px;">
    <div class="flex-item" style="flex-basis: 50%;">{0}</div>
    <div class="flex-item" style="flex-basis: 50%;">{1}</div>
</div>


<div class="section1" id="Detection-results">
    <h1 style="margin-left: 60px; margin-top: 70px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;">Visualizing Species Counts and Abundance</h1>
</div>


<div class="flex-container" style="margin-left:150px; width:1200px; margin-top: 50px;">
<div class="flex-item" style="flex-basis: 50%;">{2}</div>
<div class="flex-item" style="flex-basis: 50%;">{3}</div>
</div>
    """.format(html_counts,html_abundance,img_tags[0],img_tags[1])


# Contains the Model Summary 
if os.path.exists(os.path.join(model_path, 'opt.yaml')):
    section3_html = """
    
        <a id="model-summary"></a>
        <div class="section2" id="Model-summary">
            <h1 style="margin-left: 60px; margin-top: 30px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;">Optimized Parameters for YOLO Model Performance</h1>
        </div>


        <div class="flex-container" style="margin-left:200px; margin-top:30px;">
            <div class="flex-item" style="flex-basis: 100%;">{0}</div>
        </div>""".format(html_summary)
    
else:
    section3_html = " "

    
# Creating section for the performance graphs that were provided

graph_html_list = []
for img_tag, img_name in zip(perform_graphs, perform_graphs_names):
    image_name = os.path.splitext(img_name)[0]
    graph_html_list.append(
        """
        <div class="graph-container" style="margin: 20px;">
            <h1 style="margin-left: 100px; margin-top: 10px; font-size: 20px; padding: 10px; background-color: lightblue;">{}</h1>
            <div class="flex-item" style="flex-basis: 100%; margin-top: 10px; margin-left: 200px; ">{}</div>
        </div>
        """.format(image_name, img_tag)
    )

# Join the HTML code for each image into a single string
graphs_html = '\n'.join(graph_html_list)

if len(graph_html_list)>0:
    section4_html = """
    <a id="model-summary"></a>
    <div class="section2" id="Model-summary">
        <h1 style="margin-left: 60px; margin-top: 60px; font-size: 20px; border: 1px solid khaki; padding: 10px; background-color: khaki;">Performance Graphs for YOLO Model Training</h1>
    </div>

    <div id="plot-container" style="display: flex; flex-wrap: wrap;">
        {}
    </div>

    """.format(graphs_html)
else:
    section4_html = " "


# Creating the Model Summary header depending whether either section 3 or 4 is present or not 
model_summary_header = ''
if section3_html or section4_html:
    model_summary_header = '<h1 style="margin-left: 10px; margin-top: 90px; font-size: 24px; border: 1px solid khaki; padding: 10px; background-color: Teal; color: white;">Model Summary</h1>'



html = f"""
        <html>
        <head>
            <title> Statistics Report</title>
                <style>
                    .flex-container {{
                        display: flex;
                        align-items: center;
                        justify-content: space-between;
                        }}

                    .flex-item {{
                        margin-left: -98px;
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
                        margin-right: 190px;
                        font-size: 15px;
                        flex-shrink: 0;
                        
                        }}    

                    .quick-links nav a {{
                        text-align: center;
                        padding: 14px 16px;
                        background-color:  #F5F5DC; 
                        color: black !important;
                        font-size: 24px;
                        
                        }}

                    .quick-links nav a:hover {{
                        background-color: lightgrey;
                        }} 

                    body {{
                        background-color: #F8F8FF;
                        }}    

                </style>

        </head>
        <body>
        <div class="header">
            <h1> Statistics Report</h1>
            {user_info_html} 
        </div>     
            {toc_html}
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
                    {heading_html}
                    {section1_html}
                    {section2_html}
                    {model_summary_header}
                    {section3_html}
                    {section4_html}

        </body>
</html>""" 

# with open("C:/Users/daisy/OneDrive/Documents/Group_project/BPT_Cranfield/GUI2/stats.html", "w") as f:
#     f.write(html)

output_path = "C:/Users/benha/Documents/Cranfield/Group_Project/BPT_Cranfield/GUI/stats.html"

if not os.path.exists(output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
# if not os.access(output_path, os.W_OK):
#     print(f"Error: Cannot write to {output_path}.")
# else:
with open(output_path, "w") as f:
    f.write(html)
    print(f"File written to {output_path}.")