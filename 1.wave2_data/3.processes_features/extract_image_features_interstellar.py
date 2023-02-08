#!/usr/bin/env python
# coding: utf-8

# # Process image features from CellProfiler readout

# ## Import Libraries

# In[1]:


import pathlib
import pandas as pd
import numpy as np

from pycytominer.cyto_utils import cells, output, util

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
platemap_file = "../../0.wave1_data/2.cellprofiler_analysis/metadata/Interstellar_wave1_platemap.csv"
image_table_name = "Per_Image"

# Set path with name for outputted data
sc_output_file = pathlib.Path(f"{output_dir}/interstellar_wave2.csv.gz")


# ## Set variables for extracting image features

# In[4]:


image_feature_categories = ["Image_Correlation", "Image_Granularity", "Image_ImageQuality", "Image_Intensity"]
image_cols="ImageNumber"
strata=["Image_Metadata_Well", "Image_Metadata_Plate"]


# ## Load and view platemap file

# In[5]:


# Load platemap file
platemap_df = pd.read_csv(platemap_file)
platemap_df.head()


# ## Extract image features from sqlite file

# In[6]:


image_df = extract_utils.load_sqlite_as_df(single_cell_file, image_table_name)

print(image_df.shape)
image_df.head()


# In[7]:


image_features_df = extract_utils.extract_image_features(image_feature_categories, image_df, image_cols, strata)

print(image_features_df.shape)
image_features_df.head()


# ## View info of the dataframe

# In[8]:


image_features_df.info()

