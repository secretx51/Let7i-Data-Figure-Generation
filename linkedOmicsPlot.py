import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

MAIN_DIR = str(Path(__file__).resolve().parent) #Directory of python script
COUNTS = f"{MAIN_DIR}/data/microRNA Counts.csv"
OUTPUT = f"{MAIN_DIR}/data/microRNA formatted data.xlsx"

# Set font family to Arial
plt.rcParams['font.family'] = 'Arial'

def countsBarGraph(filename, gene_number):
    df = pd.read_csv(filename)
    df_sorted = df.sort_values(by='Count', ascending=False)
    subset_df = df_sorted.iloc[:gene_number]
    subset_df['Gene'] = subset_df['Gene'].map(lowerCaseSignature)
    
    # Set up the figure size for better visibility
    plt.figure(figsize=(8, 12))  # Width * Height Inches
    # Create the horizontal bar graph
    plt.barh(subset_df['Gene'], subset_df['Count'], color='Black')
    # Invert the y-axis to show the highest count genes at the top
    plt.gca().invert_yaxis()
    # Set the labels and title
    plt.xlabel('Number of Significant Immunological Related GO Pathways', fontsize = 14)
    #plt.title('Top 100 Genes by number immunological pathways according to LinkedOmics')
    
    # Set the font size for y-axis labels
    plt.tick_params(axis='y', labelsize=12)  # Adjust the font size as needed
    plt.tick_params(axis='x', labelsize=12)  # Adjust the font size as needed
    # Add a grid for better readability
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    
    # Remove dead space by adjusting y-axis limits
    factor = (100 / gene_number) * 2
    plt.ylim(top=subset_df['Count'].max() - 37,
            bottom=subset_df['Count'].max() + 58/factor)  # Add some padding at the top
    
    # Save the figure, or use plt.show() to display it in the notebook
    plt.savefig(f'{MAIN_DIR}/plots/FigS1 - Histogram', dpi=600, bbox_inches='tight')

def outputHeatMap(filename, gene_number):
    df = pd.read_excel(filename, sheet_name='P Value', index_col=0)
    # Top 50 genes
    df_index = pd.read_csv(COUNTS)['Gene'].iloc[:gene_number]
    # Sort the dataframe by the index
    df_sorted = df.loc[df_index]
    subset_df = df_sorted.iloc[:gene_number]
    subset_df.index = subset_df.index.map(lowerCaseSignature)
    # Formats the dataframe GO terms for heatmap
    trans_df = formatGOHeatmap(subset_df)
    
    plt.figure(figsize=(12, 9)) # Width * Height Inches
    # Generate the heatmap using seaborn's heatmap function
    heatmap = sns.heatmap(trans_df, cmap='viridis', fmt='.1f', annot=False, 
                        linewidths=0.5, linecolor='black')
    
    # Get the color bar object from the heatmap
    cbar = heatmap.collections[0].colorbar
    # Set the font size of the color bar label
    cbar.ax.set_ylabel('-log10(p-value)', rotation=90, fontsize=14)
    # Set the fontsize of the color bar ticks
    cbar.ax.tick_params(labelsize=12)
    # Set the color of the color bar border to black
    cbar.outline.set_edgecolor('black')
    cbar.outline.set_linewidth(0.5)
    # Move tick labels to left side of colour bar
    cbar.ax.yaxis.set_ticks_position('left')
    #cbar.ax.yaxis.set_label_position('left') #Move cbar label if needed
    
    # Force all y-axis tick labels to appear and highlight sig indexes for let7i
    plt.yticks(np.arange(len(trans_df))+0.5, trans_df.index, fontsize = 12.5)
    # Force all x-axis tick labels to appear and adjust their font size
    plt.xticks(np.arange(len(trans_df.columns))+0.5, trans_df.columns, fontsize=11.5, rotation=90)
    
    # Highlight the most significant GO pathways for let-7i
    idx_mask = getTopMask(trans_df)
    # Update the color for the highlighted rows
    for idx in idx_mask:
        plt.gca().get_yticklabels()[idx].set_color('red')
        
	# Set the title and labels for the plot
    # plt.ylabel('GO Immune Processes', fontsize=1)
    # plt.xlabel('Genes', fontsize=1)
    plt.ylabel('', fontsize=1) # remove axis labels
    plt.xlabel('', fontsize=1)
	# Save the figure, or use plt.show() to display it in the notebook
    plt.savefig(f'{MAIN_DIR}/plots/FigS2 - Heatmap', dpi=600, bbox_inches='tight')

def lowerCaseSignature(s):
    return s[:3] + s[3:].lower()

def goDescriptionNames(colnames):
    df = pd.read_excel(
        f"{MAIN_DIR}/data/microRNA GO Counts.xlsx", sheet_name="GO")
    current_list = []
    for go_term in colnames:
        for index, item in enumerate(df["GO Term"]):
            if str(go_term).lower() == item.lower():
                description = df["Pathway"][index]
                current_list.append(f"{description} ({go_term})")
    return current_list

def formatGOHeatmap(df):
    trans_df = df.transpose()
    trans_df["index"] = goDescriptionNames(trans_df.index)
    # Capitalise first letter of every GO term
    trans_df["index"] = trans_df["index"].apply(lambda term: term[0].upper() + term[1:])
    trans_df.set_index("index", inplace=True)
    # This next section orders the gene sets by non-NaN rows
    # Create a new column that counts the number of non-NaN numbers in each row
    trans_df['non_nan_count'] = trans_df.notnull().sum(axis=1)
    # Sort the DataFrame by descending order based on the new column
    trans_df = trans_df.sort_values(by='non_nan_count', ascending=False)
    # Delete the new column
    trans_df.drop(columns=['non_nan_count'], inplace=True)
    trans_df = trans_df.iloc[:45] # Top 45 pathways
    return trans_df

def getTopMask(trans_df):
    # Calculate the maximum value for each row
    max_values_per_row = trans_df.apply(max, axis=1)
    # Calculate the 10% leeway for each max value
    leeway_values = max_values_per_row * 0.1
    # Compare the 'LET-7i' column with the maximum value of each row with a leeway of ±5%
    result_rows = trans_df[(trans_df['LET-7i'] >= max_values_per_row - leeway_values) & 
                            (trans_df['LET-7i'] <= max_values_per_row + leeway_values)].index.tolist()
    result_rows.append('Myeloid dendritic cell activation (GO:0001773)') # biological
    # Get the index positions of the row labels you want to highlight
    return [trans_df.index.get_loc(idx) for idx in result_rows]

# countGenes("Gene Set")
# countGenes("Size")

def countGenes(column):
    df = pd.read_csv(OUTPUT)
    return df[column].value_counts().to_csv(f"{MAIN_DIR}/data/{column}_counts.csv")

def importFile(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    file.close()
    return lines

def _getGODescriptions():
    filename = f"{MAIN_DIR}/data/microRNA GO Categories.txt"
    lines = importFile(filename)
    go_dict = {}
    lastest_terms = []
    for line in lines:
        if len(go_dict.keys()) != 0:
                latest_key = list(go_dict.keys())[-1]
                go_dict[latest_key] = lastest_terms
        if str(line[0]).isnumeric():
            format_line = line.split(" ", 1)[1]
            format_line = format_line.split(":")[0]
            go_dict[format_line] = ''
            lastest_terms = [] 
        else:
            lastest_terms.append(line.strip())
    return go_dict

def replaceDescriptionsTerms():
    df = pd.read_excel(
        f"{MAIN_DIR}/data/microRNA GO Counts.xlsx", sheet_name="GO")
    go_dict = _getGODescriptions()
    for key, value in go_dict.items():
        current_list = []
        for description in value:
            for index, item in enumerate(df["Pathway"]):
                if str(description).lower() == item.lower():
                    current_list.append(df["GO Term"][index])
        go_dict[key] = current_list
    return go_dict

def getIndexGO(df, go_terms):
    category_data = {}
    # Iterate through the keys and values of the original dictionary
    for category, column_list in go_terms.items():
        # Get the indices of columns based on their names and store them in a new list
        column_indices = [df.columns.get_loc(column_name) for column_name in column_list]
        # Add the category as the key and the column indices list as the value to the updated dictionary
        category_data[category] = column_indices
    return category_data

def groupCategories(go_dict, df):
    # Group the DataFrame by the lists of column indexes from the dictionary
    def get_category(column_name):
        for category, columns in go_dict.items():
            if column_name in columns:
                return category
        return 'Uncategorized'
    # Group the DataFrame by categories
    grouped = df.groupby(get_category, axis=1, sort=False)
    return grouped

def bubblePlot(filename, gene_number):
    df = pd.read_excel(filename, sheet_name='P Value', index_col=0)
    df_index = pd.read_csv(COUNTS)['Gene'].iloc[:gene_number]
    df_sorted = df.loc[df_index]
    subset_df = df_sorted.iloc[:gene_number]
    subset_df.index = subset_df.index.map(lowerCaseSignature)

    go_dict = replaceDescriptionsTerms()
    grouped_df = groupCategories(go_dict, subset_df)

    # Set the figure size (in inches)
    plt.figure(figsize=(12, 18))  # Adjust width and height as needed
    plt.subplots_adjust(left=0.145, right=0.975)
    ax = plt.gca()

    # Create a bubble plot for each group
    max_size = []
    for category, group_df in grouped_df:
        # Calculate bubble size and color for each row
        bubble_size = group_df.notnull().sum(axis=1)
        max_size.append(bubble_size.max())  # Record all bubble sizes
        bubble_color = group_df.mean(axis=1, skipna=True)
        # Plot the bubble chart
        """
        Parameters:
            x: The immune category to be plotted under as determined groupedCategories function
            y: The gene to be plotted under as determined by groupedCategories function
            size: Calculated number of pathways impacted for that gene in that category - sum
            sizes: The range of bubble sizes, correlates with legend plot later
            hue: The colour of each bubble calculated by the mean of the p-values 
            alpha: Opacity of the bubbles, set to 1 to avoid seeing gridlines.
            palette: The green-yellow colour gradient is called viridis
            legend: False, as create custom legend later on
            cmap: Same as hue.
            ax: The plot variable to assign scatterplot to, was declared above. 
            edgecolor: The black outline around the bubbles.
            zorder: Put at higher zorder than gridlines so bubbles are above them.
        """
        sns.scatterplot(x=[category] * len(group_df), y=group_df.index,
                        size=bubble_size, sizes=(10, 300), hue=bubble_color, alpha=1,
                        palette="viridis", legend=False, cmap='viridis', ax=ax, 
                        edgecolor='black', zorder = 2)

    # Create the custom colour bar with correct p-value scale
    norm = plt.Normalize(bubble_color.min(), bubble_color.max())
    sm = plt.cm.ScalarMappable(cmap="viridis", norm=norm)
    sm.set_array([])
    # Add a colorbar
    cbar = ax.figure.colorbar(sm, shrink=0.5,
                            location="right", anchor=(0.3, 0.998))  # Set half size
    # Label for color bar
    cbar.ax.set_ylabel('-log10(p-value)', rotation=90, fontsize=18)
    # Set the fontsize of the color bar ticks
    cbar.ax.tick_params(labelsize=16)
    cbar.ax.yaxis.set_ticks_position('left')

    # Add legend for bubble sizes below the plot
    bubble_sizes = range(1, max(max_size) + 1)  # +1 to account for range ending 1 early
    legend_labels = [f'{size} non-missing values' for size in bubble_sizes]
    for size in bubble_sizes:
        plt.scatter([], [], s=size * 50, label=f'{size}', alpha=0.7, color='black')
    # Set the title of bubble legend and size of bubble text
    size_legend = plt.legend(scatterpoints=1, frameon=False, fontsize=20,
                            title='Number of\nImmune Related\nPathways',
                            loc='right', bbox_to_anchor=(1.295, 0.25))
    # Set size of the title
    size_legend.set_title('Number of\nImmune Related\nPathways',
                        prop={'size': 16})
    plt.gca().add_artist(size_legend)
    # Customize the plot
    # plt.ylabel('Genes', fontsize=20)
    plt.ylabel('', fontsize=1) # Remove y axis label
    plt.xlabel('GO Categories', fontsize=20)
    plt.subplots_adjust(top=0.99, bottom=0.2)  # Adjust the top margin to reduce space above the title

    # Rotate the x-axis labels by 45 degrees
    plt.xticks(rotation=45, fontsize=17, ha='right')
    plt.yticks(fontsize=17)
    
    # Add grey grid lines
    ax.grid(True, color='gray', linestyle='-', alpha=0.5, zorder = 2)
    # Save the plot at set dpi
    plt.savefig(f'{MAIN_DIR}/plots/Fig1 - Bubble Plot', dpi=600)

def main():
    countsBarGraph(COUNTS, 50)
    outputHeatMap(OUTPUT, 50)
    bubblePlot(OUTPUT, 50)

if __name__ == "__main__":
    main()
    