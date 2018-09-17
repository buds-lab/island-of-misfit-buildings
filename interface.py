# API documentation https://openscreen.cz/software/inchlib/inchlib_clust_doc

import inchlib_clust
import pandas as pd

# boolean variable to toggle using less features
feature_subset = 1
# choose the top N high importance features
num_features = 20 # available number of top importance features: 10, 15, 20, 25, 50, 75, 100, 125, 150, 175, 200

#instantiate the Cluster object
c = inchlib_clust.Cluster()

# load original dataset
df_original_dataset = pd.read_csv('data/ALLFEATURES.CSV')

# find labels

# find missing values, if any, and display findings
if (df_original_dataset.isnull().values.any()):
	null_columns = df_original_dataset.columns[df_original_dataset.isnull().any()]
	# find number of missing values per column
	print df_original_dataset[null_columns].isnull().sum()
	# find rows with missing values
	# print df_original_dataset[df_original_dataset.isnull().any(axis=1)][null_columns].head()
	# remove instances with NaN
	df_original_dataset = df_original_dataset.dropna(axis=0)

# if boolean variable is true, continue to slice the original dataset
if feature_subset:
	# load file
	file_name = "jupyter-notebooks/" + str(num_features) + "_features_sub.txt"
	input_file = open(file_name, "r")
	# convert file into list by first removing the end of line character of each line and converting each value to int
	selected_indeces = [int(i.strip("\n")) for i in input_file.readlines()]
	# retain only the columns which indeces are in the .txt file
	df_sliced_dataset = df_original_dataset.iloc[:, selected_indeces] # also keep the ids
	# keep the ids
	df_sliced_dataset.insert(0, "uid", df_original_dataset.iloc[:, 0])
	# transform dataframe into list of lists with header
	header = df_sliced_dataset.columns.values.tolist()
	print header 
	sliced_dataset_list = df_sliced_dataset.values.tolist()
	sliced_dataset_list.insert(0, header)
	# load the data into the cluster object
	c.read_data(sliced_dataset_list, header=True, missing_value="", datatype="numeric")
	# see which features remained
else:
	# read csv data file with specified delimiter, also specify whether there is a header row, the type of the data (numeric/binary) and the string representation of missing/unknown values
	c.read_csv(filename="data/ALLFEATURES.CSV", delimiter=",", header=True, missing_value="", datatype="numeric")
	# c.read_data(data, header=bool, missing_value=str/False, datatype="numeric/binary") use read_data() for list of lists instead of a data file

# normalize data to (0,1) scale, but after clustering write the original data to the heatmap
c.normalize_data(feature_range=(0,1), write_original=True)
# cluster data according to the parameters
c.cluster_data(row_distance="euclidean", row_linkage="centroid", axis="row", column_distance="euclidean", column_linkage="ward")

# instantiate the Dendrogram class with the Cluster instance as an input
d = inchlib_clust.Dendrogram(c)

# create the cluster heatmap representation and define whether you want to compress the data by defining the maximum number of heatmap rows, the resulted value of compressed (merged) rows and whether you want to write the features
d.create_cluster_heatmap(compress=False, compressed_value="median", write_data=True) # tweak compress

# read metadata file with specified delimiter, also specify whether there is a header row
# Contains metadata (i.e., additional information, such as, e.g., class membership, about individual objects) can be detailed in 
# metadata_compressed_value as frequency/median/mean)
# d.add_metadata_from_file(metadata_file="/path/to/file.csv", delimiter=",", header=True, metadata_compressed_value="frequency")
metadata = pd.read_csv('data/meta_open.CSV')
metadata_sliced = metadata[['uid', 'primaryspaceuse_abbrev']]
metadata_sliced_list = 	metadata_sliced.values.tolist()
header_metadata = metadata_sliced.columns.values.tolist()
metadata_sliced_list.insert(0, header_metadata ) # insert metadata header
d.add_metadata(metadata_sliced_list, header=True, metadata_compressed_value='frequency')

# read column metadata file with specified delimiter, also specify whether there is a 'header' column
# Contains column metadata (i.e., additional information, such as, e.g., class membership, about individual columns)
# d.add_column_metadata_from_file(column_metadata_file="/path/to/file.csv", delimiter=",", header=bool)

# export the cluster heatmap on the standard output or to the file if filename specified
d.export_cluster_heatmap_as_json("clusteredBDG.json")
# d.export_cluster_heatmap_as_json("/var/www/html/clusteredBDG.json") # uncomment when running in EC2 solution

# function exports simple HTML page with embedded cluster heatmap and dependencies to given directory 
# d.export_cluster_heatmap_as_html() # currently not working, needs to fix the localhost issue # currently doesn't work
