#!/usr/bin/env python
# coding: utf-8

# # Process image features from CellProfiler readout

# ## Import Libraries

# In[1]:


import pathlib
import pandas as pd

from pycytominer import annotate
from pycytominer.cyto_utils import output

import sys
sys.path.append("../../utils")
import extract_image_features_utils as extract_utils


# ## Set up paths to CellProfiler directory and outputs

# In[2]:


# Set file and directory constants
cp_dir = "../2.cellprofiler_analysis"
output_dir = "data"


# ## Set paths to sqlite files

# In[3]:


# Set name and path of .sqlite file and path to metadata
sql_file = "interstellar_wave2.sqlite"
single_cell_file = f"sqlite:///{cp_dir}/analysis_output/{sql_file}"
platemap_file = "../../metadata/Interstellar_platemap.csv"
image_table_name = "Per_Image"

# Set path with name for outputted data
image_features_output_file = pathlib.Path(f"{output_dir}/interstellar_wave2.csv.gz")


# ## Set variables for extracting image features

# In[4]:


# These categories are based on the measurement modules ran in the CellProfiler pipeline
image_feature_categories = ["Image_Correlation", "Image_Granularity", "Image_ImageQuality", "Image_Intensity"]
image_cols="ImageNumber"
strata=["Image_Metadata_Well", "Image_Metadata_Plate"]


# ## Load and view platemap file

# In[5]:


# Load platemap file
platemap_df = pd.read_csv(platemap_file)
platemap_df.head()


# ## Load in sqlite file

# In[6]:


image_df = extract_utils.load_sqlite_as_df(single_cell_file, image_table_name)

print(image_df.shape)
image_df.head()


# ## Extract image features from sqlite file

# In[7]:


image_features_df = extract_utils.extract_image_features(image_feature_categories, image_df, image_cols, strata)

print(image_features_df.shape)
image_features_df.head()


# ## Merge platemap metadata with extracted image features

# In[8]:


image_features_df = annotate(
    profiles=image_features_df,
    platemap=platemap_df,
    join_on=["Metadata_well", "Image_Metadata_Well"],
    output_file="none",
)


# ## Add condition as a metadata column to the dataframe

# In[9]:


def conditions(well_column):
    """
    function works to add condition based on the well column number for each single cell (row)
    """
    if well_column == 5 or 8:
        return 8
    if well_column == 6 or 7:
        return 7

# add the condition metadata as a column based on the function (adds to the end)
image_features_df['Metadata_condition'] = image_features_df['Metadata_col'].map(conditions)
# pop out the column from the dataframe
condition_column = image_features_df.pop('Metadata_condition')
# insert the column as the third index column in the dataframe
image_features_df.insert(3, 'Metadata_condition', condition_column)

print(image_features_df.shape)
image_features_df.head()


# ## Save image features data frame as `csv.gz` file

# In[10]:


# Save image feature data as a csv
output(image_features_df, image_features_output_file)

print(image_features_df.shape)
image_features_df.head()


# ## View info of the dataframe

# In[11]:


image_features_df.info()

