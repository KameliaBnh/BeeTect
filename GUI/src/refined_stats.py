import os 
import shutil
import random
import batch_2_comp as bc 
import seaborn as sns
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import yaml
import base64
import warnings
warnings.filterwarnings("ignore", message="this method is deprecated")

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
model_path = os.path.dirname(bc.main_window.Models[0].path)

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

    # Writing the summary to a csv file
    summary_df.to_csv(os.path.join(bc.main_window.Batches[0].path, 'Model_Summary.csv'), index=False)

    html_summary =  create_styled_table(summary_df)

# Getting the number of input Images 
# converting the strings of numbers into integers to calculate max value 
numbers = [int(n) for n in bc.image_no] 
no_input_img= max(numbers)

# Getting the bee species with the highest counts 
max_key = max(bc.filtered_counts, key=lambda k: bc.filtered_counts[k])
max_value = max(bc.filtered_counts.values())

# Finding the bee species which has the lowest counts
min_key = min(bc.filtered_counts, key=lambda k: bc.filtered_counts[k])
min_value = min(bc.filtered_counts.values())

##Creating a table with the above information
#create data
data = [["Number of Input Images","-", no_input_img], 
        ["Number of Images with no Detections","-",bc.no_detection_images],
        ["Highest Bee Species Counts",max_key,max_value],
        ["Lowest Bee Species Counts",min_key,min_value]]

#define header names
col_names = ["Metric","Species Name", "Value"]

#Saving the Information in a dataframe 
counts_df =pd.DataFrame(data, columns=col_names)

# Writing the information to a csv file
counts_df.to_csv(os.path.join(bc.main_window.Batches[0].path, 'Counts.csv'), index=False)

#Storing the bee counts in a dataframe 
abundance_df = pd.DataFrame(list(bc.filtered_counts.items()), columns=['Species', 'Occurence'])

#creating dataframe to store species abundance
total_count = abundance_df['Occurence'].sum()

abundance_df['Abundance'] = abundance_df['Occurence'] / total_count
abundance_df['Abundance'] = abundance_df['Abundance'].round(2)


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


# Checking if the length of the selected batches is one or more
if len(bc.main_window.batch_results) == 1:

    # Getting example images for each detected species 
    output_path = os.path.join(bc.main_window.Batches[0].path, 'Pollinator')
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
    output_directory_single_batch = os.path.join(bc.main_window.Batches[0].path,'Output_Graphs')
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
    species_names = list(bc.filtered_counts.keys())
    species_counts = list(bc.filtered_counts.values())
    fig,ax= plt.subplots()
    ax.pie(species_counts, labels=species_names, autopct='%1.1f%%')
    ax.set_title('Bee Species Abundance')
    fig.savefig(f'{output_directory_single_batch}/bee_species_counts.png', dpi=700)
    plt.close()

    img_tags = image_encode(output_directory_single_batch, 600, 600)
    img_tags_list = image_encode_list(random_image_paths, 500, 500)

  
else:

    html0 = create_styled_table(bc.normality_df)
    html1 = create_styled_table(bc.df)
    html2 = create_styled_table(bc.overview_df)

    #creating a directory to save all the output graphs
    # Set the output_batch_comparison directory to the 'Batch_Comparison_i' folder with the highest i value
    # set the number variable as the highest i value
    number = 0
    for i in range(1, len(bc.main_window.Projects[0].path)):
        if os.path.exists(os.path.join(bc.main_window.Projects[0].path, 'Batch_Comparison_' + str(i))):
            number = i
    output_directory_batch_comparison = os.path.join(bc.main_window.Projects[0].path, 'Batch_Comparison_' + str(number), 'Output_Graphs')
    if not os.path.exists(output_directory_batch_comparison):
        os.makedirs(output_directory_batch_comparison)

    # Save the plots into the output graphs folder 
    shutil.move(os.path.join(os.getcwd(), 'bee_counts.png'),output_directory_batch_comparison)
    shutil.move(os.path.join(os.getcwd(), 'descriptive_stats.png'),output_directory_batch_comparison)
    shutil.move(os.path.join(os.getcwd(), 'QQ-plot.png'),output_directory_batch_comparison)


    if bc.p > bc.alpha:
        if len(bc.main_window.batch_results)==2:
            html3 = create_styled_table(bc.Levene_df)
            html4 = create_styled_table(bc.ttest_df)

        else: 
            html5 = create_styled_table(bc.anova_df)
            html6 = create_styled_table(bc.tukey_df)
            shutil.move(os.path.join(os.getcwd(), 'Boxplot.png'), output_directory_batch_comparison)

    else:
        if len(bc.main_window.batch_results)==2:
            html7 = create_styled_table(bc.whitney_df)

        else: 
            html8 = create_styled_table(bc.krushal_df)
            if bc.krushal_p < 0.05:
                html9 = create_styled_table(bc.dunn_df)
            else:   
                Conclusion5 = "Cannot Perform dunn test as p-value is greater than 0.05"

    img_tags = image_encode(output_directory_batch_comparison, 800, 600)