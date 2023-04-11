import os 
import shutil
import random
import batch_2_comp as bc 
import seaborn as sns
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import yaml
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

# Getting the Model Summmary 
with open(os.path.join(bc.main_window.Models.path, bc.main_window.ui.comboBox.currentText(), 'opt.yaml'), 'r') as f:
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

# Writing the summary to a csv file
summary_df.to_csv(os.path.join(bc.main_window.Batches[0].path, 'Model_Summary.csv'), index=False)

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

#Creating a function to style the tables 
def create_styled_table(df):
    styled_table = df.style.set_table_styles([{'selector': 'th', 'props': [ ('font-size', '24px'), ('text-align', 'center'), ('color', 'black'), ('background-color', 'lightblue'), ('font-weight', 'bold'),('padding', '5px'), ('border', '1px solid black')]}, {'selector': 'td','props': [('font-size', '20px'),('padding', '5px'), ('border', '1px solid black'), ('text-align', 'center')]}])
    html = styled_table.hide_index().render()
    return html

html0 = create_styled_table(bc.normality_df)
html1 = create_styled_table(bc.df)
html2 = create_styled_table(bc.overview_df)
html_summary =  create_styled_table(summary_df)
html_counts = create_styled_table(counts_df)
html_abundance = create_styled_table(abundance_df)

if len(bc.main_window.batch_results) == 1:

    # Getting example images for each detected species 
    output_path = os.path.join(bc.main_window.Batches[0].path, 'Pollinator')
    subfolders = [f.path for f in os.scandir(output_path) if f.is_dir()]
    random_image_paths = []

    # Loop through each subfolder
    for subfolder in subfolders:
    # Get a list of all image files within the subfolder
        image_files = [f for f in os.listdir(subfolder) if f.endswith(".JPG")]

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

else:

    #creating a directory to save all the output graphs
    output_directory_batch_comparison = os.path.join(bc.main_window.Projects[0].path,'Output_Graphs')
    if not os.path.exists(output_directory_batch_comparison):
        os.makedirs(output_directory_batch_comparison)

    # Creating a heatmap 
    bc.df.set_index('Batch Name', inplace=True) # set 'Batch Name' as index
    heatmap = sns.heatmap(bc.df, cmap='coolwarm', center=0, annot=True, fmt='.2f') # plot heatmap with annotations and specified colormap

    # Set the figure size
    fig = heatmap.get_figure()
    fig.set_size_inches(10, 8)
    plt.title("Bee Count Heatmap")
    plt.xlabel('Species')

    # Save the heatmap as an image
    fig.savefig(f'{output_directory_batch_comparison}/heatmap.png', dpi=300, bbox_inches='tight')
    
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
            html9 = create_styled_table(bc.dunn_df)
