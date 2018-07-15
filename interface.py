import inchlib_clust # API documentation https://openscreen.cz/software/inchlib/inchlib_clust_doc
import pandas as pd

#instantiate the Cluster object
c = inchlib_clust.Cluster()

# load original dataset and made a copy of it in order to modify building name and id feature
df_original_dataset = pd.read_csv('data/ALLFEATURES.CSV')
df_modified_dataset = df_original_dataset.copy()

# delete the building name feature (first column)
del df_modified_dataset['Unnamed: 0'] # the column originally had no header

# insert index as building_ID as first feature
df_modified_dataset.insert(0, 'building_ID', df_modified_dataset.index)

# find missing values, if any
if (df_modified_dataset.isnull().values.any()):
	null_columns = df_modified_dataset.columns[df_modified_dataset.isnull().any()]
	# find number of missing values per column
	print df_modified_dataset[null_columns].isnull().sum()
	# find rows with missing values
	print df_modified_dataset[df_modified_dataset.isnull().any(axis=1)][null_columns].head()

# saved the transformed dataset
df_modified_dataset.to_csv('data/ALLFEATURES_index.csv', index=False)

# read csv data file with specified delimiter, also specify whether there is a header row, the type of the data (numeric/binary) and the string representation of missing/unknown values
print c.read_csv(filename="data/ALLFEATURES_index.csv", delimiter=",", header=True, missing_value="", datatype="numeric")
# c.read_data(data, header=bool, missing_value=str/False, datatype="numeric/binary") use read_data() for list of lists instead of a data file

# normalize data to (0,1) scale, but after clustering write the original data to the heatmap
c.normalize_data(feature_range=(0,1), write_original=True)

# cluster data according to the parameters
c.cluster_data(row_distance="euclidean", row_linkage="single", axis="row", column_distance="euclidean", column_linkage="ward")

# instantiate the Dendrogram class with the Cluster instance as an input
d = inchlib_clust.Dendrogram(c)

# create the cluster heatmap representation and define whether you want to compress the data by defining the maximum number of heatmap rows, the resulted value of compressed (merged) rows and whether you want to write the features
d.create_cluster_heatmap(compress=False, compressed_value="median", write_data=True) # tweak compress

# read metadata file with specified delimiter, also specify whether there is a header row
d.add_metadata_from_file(metadata_file="data/ALLFEATURES_meta_labelled.csv", delimiter=",", header=True, metadata_compressed_value="frequency")

# read column metadata file with specified delimiter, also specify whether there is a 'header' column
# d.add_column_metadata_from_file(column_metadata_file="/path/to/file.csv", delimiter=",", header=bool)

# export the cluster heatmap on the standard output or to the file if filename specified
d.export_cluster_heatmap_as_json("cluesteredBDG.json")
#d.export_cluster_heatmap_as_html("/path/to/directory") function exports simple HTML page with embedded cluster heatmap and dependencies to given directory 

