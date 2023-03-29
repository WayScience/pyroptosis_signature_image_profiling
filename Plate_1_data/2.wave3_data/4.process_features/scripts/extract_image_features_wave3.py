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
cp_dir = "../3.cellprofiler_analysis"
output_dir = "data"


# ## Set paths to sqlite files

# In[3]:


# Set name and path of .sqlite file and path to metadata
sql_file = "interstellar_wave3_imagequality.sqlite"
single_cell_file = f"sqlite:///{cp_dir}/analysis_output/{sql_file}"
platemap_file = "../../metadata/Interstellar_platemap.csv"
image_table_name = "Per_Image"

# Set path with name for outputted data
image_features_output_file = pathlib.Path(f"{output_dir}/interstellar_wave3_imagequality.csv.gz")


# ## Set variables for extracting image features

# In[4]:


# Only ImageQuality category since the CellProfiler pipeline extract image quality measurements
image_feature_categories = ["Image_ImageQuality"]
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


## Uses pycytominer annotate functionality to merge the platemap and image features and reorder the dataframe
image_features_df = annotate(
    profiles=image_features_df,
    platemap=platemap_df,
    join_on=["Metadata_well", "Image_Metadata_Well"],
    output_file="none",
)


# ## Save image features data frame as `csv.gz` file

# In[9]:


# Save image feature data as a csv
output(image_features_df, image_features_output_file)

print(image_features_df.shape)
image_features_df.head()


# ## View info of the dataframe

# In[10]:


image_features_df.info()

