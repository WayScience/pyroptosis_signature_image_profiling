#!/usr/bin/env python
# coding: utf-8

# # Create and edit LoadData csv and run CellProfiler `illum.cppipe` (IC) pipeline
# 
# In this notebook, we create a LoadData CSV with the raw data (like in the previous module), but we remove all rows except rows with the last z-plane as the names of the maximum projected images are the same and correct the paths from the raw images to the maximum projected images.
# 
# We then run the CellProfiler IC pipeline to calculate the illumination correction functions for all images per channel.

# ## Import libraries

# In[1]:


import pathlib

import sys
sys.path.append("../../utils")
import loaddata_utils as ld_utils
import cp_utils as cp_utils


# ## Set paths
# 
# **Note:** All paths must be absolute since CellProfiler will need to find the images based on your local machine. Please change the `/home/jenna` part of the path to reflect your machine.

# In[2]:


# set paths for pe2loaddata
## path to raw data with index file
index_directory = pathlib.Path("../0.download_data/70117_20230210MM1_Gasdermin514_CP_BC430856__2023-03-22T15_42_38-Measurement1/Images/").absolute()
## path to config file (used for all modules)
config_path = pathlib.Path("../1.cellprofiler_quality_control/config.yml").absolute()

# set paths for CellProfiler
path_to_pipeline = pathlib.Path("./illum.cppipe").absolute()
## path to folder for IC functions
path_to_output = pathlib.Path("./illum_directory").absolute()

# path to LoadData CSV used by both pe2loaddata and CellProfiler
path_to_output_csv = pathlib.Path("./loaddata_with_maxproj.csv").absolute()


# ## Create the LoadData csv with illum correction functions

# In[3]:


ld_utils.create_loaddata_csv(
    index_directory=index_directory,
    config_path=config_path,
    path_to_output=path_to_output_csv,
)


# ## Edit LoadData csv to remove unnecessary rows and correct paths to images

# In[4]:


ld_utils.edit_loaddata_csv(path_to_loaddata_csv=path_to_output_csv)


# ## Run `illum.cppipe` pipeline and calculate + save IC functions

# In[5]:


# Run CellProfiler on the illum pipeline
cp_utils.run_cellprofiler(
    path_to_pipeline=path_to_pipeline,
    path_to_output=path_to_output,
    path_to_loaddata=path_to_output_csv,
)

