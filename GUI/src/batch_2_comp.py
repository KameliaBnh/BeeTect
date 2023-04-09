import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
import sys
import pandas as pd
import scipy.stats as stats
from scipy.stats import ttest_ind
from scipy.stats import levene
from scipy.stats import shapiro
from scipy.stats import kruskal
from scikit_posthocs import posthoc_dunn
from scipy.stats import f_oneway
import statsmodels.api as sm
from statsmodels.stats.multicomp import pairwise_tukeyhsd

from PySide2.QtWidgets import QApplication

# Import the main window object (mw) to access variables
import MainWindow as mw

# Create the Qt application
app = QApplication(sys.argv)

# Create an object for the main window
main_window = mw.MainWindow()

# Creating a function to extract the bee counts from each results.txt file
def read_results(file_path):
    with open(file_path) as f:
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
    return (filtered_counts, per_image_counts, no_detection_images, image_no)

# Creating a grouped bar plot 
def plot_filtered_counts(paths):
    """
    Plots a grouped bar chart of the filtered counts for the given list of paths.
    """
    filtered_counts_list = []
    folder_names = []
    for path in paths:
        folder_name = os.path.basename(os.path.dirname(path))
        filtered_counts, per_image_counts, no_detection_images, image_no = read_results(path)
        filtered_counts_list.append(filtered_counts)
        folder_names.append(folder_name)

    sorted_keys = sorted(set().union(*filtered_counts_list))

    # Get the sorted values for each dictionary using the sorted keys
    sorted_values_list = []
    for filtered_counts in filtered_counts_list:
        sorted_values = [filtered_counts.get(key, 0) for key in sorted_keys]
        sorted_values_list.append(sorted_values)

    fig, ax = plt.subplots(figsize=(10,5))
    x = np.arange(len(sorted_keys))  

    total_width = 0.8
    n = len(sorted_values_list)
    width = total_width / n
    errors = [np.std(group_counts) for group_counts in sorted_values_list] # calculating the standard deviation

    for i in range(n):
        plt.bar(x + i * width, sorted_values_list[i], width=width, label=folder_names[i], edgecolor='white')
        #plt.errorbar(x + i * width, sorted_values_list[i], yerr=errors[i], fmt='none', ecolor='black', capsize=4, alpha=0.5)
        # if the error bars overlap there is no statistical difference between the groups and vice-versa

    plt.title('Bee species count', fontsize=20)
    plt.xticks(x, sorted_keys, fontsize=8)
    plt.xlabel('Bee species', fontsize=17)
    plt.ylabel('Count', fontsize =17)
    plt.yticks(fontsize=14)
    sns.despine(bottom=True)
    ax.grid(False)
    ax.tick_params(bottom=False, left=True)
    ax.spines['bottom'].set_visible(True)
    plt.legend(frameon=True, fontsize=10)
    if len(paths) > 1:
        plt.savefig('bee_counts.png', dpi=300, bbox_inches='tight')
    plt.close()
    return filtered_counts, filtered_counts_list, per_image_counts, no_detection_images, image_no, folder_names

# Creating a dataframe with all the counts 
def filtered_counts_table(paths):
    """
    Creates a dataframe to store the bee counts

    """

    data = []
    metrics =[]
    for path in paths:
        folder_name = os.path.basename(os.path.dirname(path))
        filtered_counts, _, _, _ = read_results(path)
        data_dict = {'Batch Name': folder_name}
        for key, value in filtered_counts.items():
            data_dict[key] = value
        data.append(data_dict)

    
    df = pd.DataFrame(data)
    df.iloc[:, 1:] = df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)
    
    # creating a dataframe with basic stats - mean, median, standard deviation, sum
    for column in df.columns[1:]:
        column_metrics = [np.mean(df[column]), np.median(df[column]), np.std(df[column]), np.sum(df[column])]
        metrics.append(column_metrics) 

    species_names = df.columns[1:].tolist()
    metric_names = ['Mean', 'Median', 'Standard Deviation', 'Sum']
    overview_df = pd.DataFrame(index=species_names, columns=metric_names)

    # fill in dataframe with metric data
    for i, metric in enumerate(metrics):
        overview_df.iloc[i] = metric
    
    overview_df = overview_df.rename_axis("Species").reset_index()

    # round all values to 3 decimal places, except headers and index
    overview_df = overview_df.round()

    means = overview_df['Mean'].tolist()
    medians = overview_df['Median'].tolist()
    sums = overview_df['Sum'].tolist()

    # set the position of the bars on the x-axis
    r = range(len(species_names))

    # create the bar plot
    fig, ax = plt.subplots()
    bar_width = 0.25
    rects1 = ax.bar(r, means, bar_width, label='Mean')
    rects2 = ax.bar([x + bar_width for x in r], medians, bar_width, label='Median')
    rects3 = ax.bar([x + bar_width*2 for x in r], sums, bar_width, label='Sum')

    # add x-axis labels and tick marks
    ax.set_xticks([x + bar_width for x in r])
    ax.set_xticklabels(species_names, fontsize =6)
    plt.title('Descriptive Statistics', fontsize=20)
    plt.xlabel('Bee species', fontsize=17)
    plt.ylabel('Metric Values', fontsize =17)

    # add a legend
    plt.legend(frameon=True, fontsize=10)

    # display the plot
    if len(paths) > 1:
        plt.savefig('descriptive_stats.png', dpi=300, bbox_inches='tight')
    plt.close()

    return df,overview_df

def normality(df):

    # 1) Checking Normality of Residuals

    # Convert batch names to dummy variables
    dummy_df = pd.get_dummies(df['Batch Name'])

    # Combine the dummy variables with the bee count data
    X = sm.add_constant(dummy_df)
    Y = df.drop('Batch Name', axis=1)

    # Fit the model
    model = sm.OLS(Y, X).fit()
    residuals = model.resid # calculate residuals

    # Creating a QQ-plot

    fig = sm.qqplot(residuals, line='s')
    plt.title("QQ-plot of Residuals")
    if len(df) > 1:
        plt.savefig('QQ-plot.png', dpi=300, bbox_inches='tight')
    plt.close()

   # Performing the Shapiro-Wilk test for normality
    stat, p = shapiro(residuals)
    normality_df = pd.DataFrame({'Test Statistic': [stat], 'p-value': [p]})

    return p, normality_df

# Creating a function that will perform all the statistics 
def comp_stats(paths, filtered_counts_list, folder_names):

    if p > alpha:
        Output1 = " Conclusion: The data is normally distributed. Performing further parametric tests."
    
        if len(paths)==2:
            statistic, p_value1 = levene(batch_values[0], batch_values[1])
            Levene_df = pd.DataFrame({'Statistic': [statistic], 'P-value': [p_value1]})

            if p_value1 > alpha:
                Output2 = " Conclusion: Assuming the variances of the two groups are equal."    
                t_statistic, p_value2 = ttest_ind(batch_values[0], batch_values[1], equal_var=True)

            else:
                Output2= "Conclusion: Assuming the variances of the two groups are unequal. "
                t_statistic, p_value2 = ttest_ind(batch_values[0] , batch_values[1] , equal_var=False)

            ttest_df = pd.DataFrame({'T-statistic': [t_statistic], 'P-value': [p_value2]})

            if p_value2 < alpha:
                Conclusion1 = "There is a statistical difference between the number of bee species found in the organic and conventional fields."    

            else:
                Conclusion1 = "There is no statistical difference between the number of bee species found in the organic and conventional fields."


            return Output1, Levene_df, Output2, ttest_df, Conclusion1

        
        if len(paths)>2:

            #performing one way ANOVA

            f_statistic, p_value = f_oneway(*batch_values)
        
            anova_df = pd.DataFrame({'F-statistic': [f_statistic], 'P-value': [p_value]})
            if p_value < alpha:
                Conclusion2 = "There is a statistically significant difference between at least two batches. Performing Post Hoc Tukey tests. "

                #Creating a boxplot for visual analysis 
                fig, ax = plt.subplots(1, 1)
                ax.boxplot(batch_values, patch_artist=True)
                ax.set_xticklabels(folder_names, fontsize = 6) 
                ax.set_ylabel("Bee Counts") 
                ax.set_xlabel("Batch Name") 
                plt.title("Bee Counts by Batch")
                plt.savefig('Boxplot.png', dpi=300, bbox_inches='tight')
                plt.close()

                data = np.concatenate(batch_values)
                labels = np.repeat(folder_names, [len(batch_values[i]) for i in range(len(batch_values))])

                # Perform the Tukey's HSD test
                tukey_results = pairwise_tukeyhsd(data, labels)

                # Convert results to a pandas DataFrame
                tukey_df = pd.DataFrame(data=tukey_results._results_table.data[1:], columns=tukey_results._results_table.data[0])

                return p_value, Output1, anova_df, Conclusion2

            else:
                Conclusion2 = "There is no statistically significant difference between the batches."
                
                return p_value,Output1, anova_df, Conclusion2



    else:
        Output1 = " Conclusion: The data is not normally distributed. Performing further non-parametric tests."

            
        if len(paths)==2:
            whitney_statistic, p_value3 = stats.mannwhitneyu(batch_values[0] , batch_values[1])

            whitney_df = pd.DataFrame({'Statistic': [whitney_statistic], 'P-value': [p_value3]})

            if p_value3 < alpha:
                Conclusion3 = "There is a statistical difference between the bee counts in the organic and conventional fields. "    
            else:
                Conclusion3 = "There is no statistical difference between the bee counts in the organic and conventional fields."

            return Output1, whitney_df, Conclusion3


        if len(paths)>2:

            # the krushal wallis test outputs the H-statistic which is a measure of how different the medians of the groups are. 
            krushal_stat, krushal_p = kruskal(*batch_values)
            krushal_df = pd.DataFrame({'H-Statistic': [krushal_stat], 'P-value': [krushal_p]})

            if krushal_p < alpha:
                Conclusion4 = "There is at least one group with a different median than the others. "
            else:
                Conclusion4 = "The medians of all groups are equal. "


            return Output1,krushal_p, krushal_df, Conclusion4

# Creating a function to perform Post Hoc Tukey tests
def tukey(p_value):
    #Creating a boxplot for visual analysis 
    fig, ax = plt.subplots(1, 1)
    ax.boxplot(batch_values, patch_artist=True)
    ax.set_xticklabels(folder_names, fontsize = 6) 
    ax.set_ylabel("Bee Counts") 
    ax.set_xlabel("Batch Name") 
    plt.title("Bee Counts by Batch")
    plt.savefig('Boxplot.png', dpi=300, bbox_inches='tight')
    plt.close()

    data = np.concatenate(batch_values)
    labels = np.repeat(folder_names, [len(batch_values[i]) for i in range(len(batch_values))])

    # Perform the Tukey's HSD test
    tukey_results = pairwise_tukeyhsd(data, labels)

    # Convert results to a pandas DataFrame
    tukey_df = pd.DataFrame(data=tukey_results._results_table.data[1:], columns=tukey_results._results_table.data[0])

    return tukey_df

# Creating a function to perform Dunn tests
def dunn(krushal_p):

    if krushal_p < 0.05:
        data = np.array(batch_values, dtype=object)
        #data = np.array(batch_values).astype(float)
        #labels = np.repeat(folder_names, [len(batch_values[i]) for i in range(len(batch_values))])
        dunn_results = posthoc_dunn(data, p_adjust='bonferroni')

        # Convert the results to a pandas DataFrame
        dunn_df = pd.DataFrame(dunn_results)
        dunn_df.columns = folder_names[:dunn_df.shape[1]]
        
    return dunn_df

# Setting the significance level 
alpha = 0.05

filtered_counts, filtered_counts_list, per_image_counts, no_detection_images, image_no, folder_names = plot_filtered_counts(main_window.batch_results)

df, overview_df = filtered_counts_table(main_window.batch_results)

# Calling the normality function
p, normality_df = normality(df)

# Storing all the bee counts 
batch_values = []
for counts in filtered_counts_list:
    batch_values.append(list(counts.values()))

# Extracting stat values from the function

if len(main_window.batch_results) > 1:
    if p > alpha:
        if len(main_window.batch_results)==2:
            Output1, Levene_df, Output2, ttest_df, Conclusion1 = comp_stats(main_window.batch_results,filtered_counts_list, folder_names)
        else:
            p_value, Output1, anova_df, Conclusion2  = comp_stats(main_window.batch_results,filtered_counts_list, folder_names)
            tukey_df = tukey(p_value)
    else: 
        if len(main_window.batch_results)==2:
            Output1, whitney_df, Conclusion3 = comp_stats(main_window.batch_results,filtered_counts_list, folder_names)
        else:
            Output1, krushal_p, krushal_df, Conclusion4 = comp_stats(main_window.batch_results, filtered_counts_list, folder_names)
            #dunn_df = dunn(krushal_p)
