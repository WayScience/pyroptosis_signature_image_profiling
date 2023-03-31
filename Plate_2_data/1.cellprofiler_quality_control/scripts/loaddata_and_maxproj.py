#!/usr/bin/env python
# coding: utf-8

# # Create LoadData csv and run CellProfiler `zproj.cppipe` pipeline - Plate 2
# 
# This notebook creates a loaddata CSV (`load_data_without_projection.csv`) and use the CSV to execute the `zproj.cppipe` pipeline and output a new image dataset of maximum projection images for the whole plate.

# ## Import libraries

# In[1]:


import os
import pathlib

import sys
sys.path.append("../../utils/")
import loaddata_utils as ld_utils
import cp_utils as cp_utils


# ## Set paths

# In[2]:


# set paths for pe2loaddata
index_directory = pathlib.Path("../0.download_data/70117_20230210MM1_Gasdermin514_CP_BC430856__2023-03-22T15_42_38-Measurement1/Images/").absolute()
config_path = pathlib.Path("./config.yml").absolute()

# set paths for CellProfiler
path_to_pipeline = pathlib.Path("./zproj.cppipe").absolute()
path_to_output = pathlib.Path("../0.download_data/70117_20230210MM1_Gasdermin514_CP_BC430856__2023-03-22T15_42_38-Measurement1/Maximum_Images/").absolute()

# path to LoadData CSV used by both pe2loaddata and CellProfiler
path_to_output_csv = pathlib.Path("./loaddata_without_projection.csv").absolute()


# ## Create the LoadData csv

# In[3]:


ld_utils.create_loaddata_csv(
    index_directory=index_directory,
    config_path=config_path,
    path_to_output=path_to_output_csv,
)


# ## Run `zproj.cppipe` pipeline in CellProfiler

# In[4]:


cp_utils.run_cellprofiler(
    path_to_pipeline=path_to_pipeline,
    path_to_output=path_to_output,
    path_to_loaddata=path_to_output_csv,
)

