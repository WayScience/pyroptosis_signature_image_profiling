#!/usr/bin/env python
# coding: utf-8

# # Create LoadData csv and run CellProfiler `illum.cppipe` pipeline - Wave 1

# ## Import libraries

# In[1]:


import os
import pathlib

import sys
sys.path.append("../../utils/")
import cp_utils as cp
import loaddata_utils as ld


# ## Set constant paths
# 
# **Note:** All paths must be absolute (these are added to the CSV) since CellProfiler will need to find the images based on your local machine.

# In[2]:


# path to the LoadData CSV for CellProfiler and pe2loaddata to use
path_to_loaddata = pathlib.Path("./wave1_loaddata.csv").absolute()


# ## Set paths for `pe2loaddata`
# 

# In[3]:


# path to the directory for the plate containing the images and index file
index_directory = pathlib.Path("../0.download_data/70117_20230118MM1_AbTest_V2__2023-01-25T16_44_54-Measurement1/Images").absolute()
# path to the config file to extract metadata and create LoadData CSV from
config_path = pathlib.Path("./config.yml").absolute()


# ## Set paths for CellProfiler `illum.cppipe` run

# In[4]:


# path to the illum pipeline
path_to_pipeline = pathlib.Path("./interstellar_wave1_illum.cppipe").absolute()

# path for the output directory
path_to_output = pathlib.Path("./illum_directory/").absolute()


# ## Create the LoadData csv

# In[5]:


ld.create_loaddata_csv(
    index_directory=index_directory,
    config_path=config_path,
    path_to_output=path_to_loaddata,
)


# ## Run CellProfiler `illum.cppipe` pipeline

# In[6]:


# since we are running an illum pipeline, we do not use `sqlite_name` and `analysis_run`
cp.run_cellprofiler(
    path_to_pipeline=path_to_pipeline,
    path_to_output=path_to_output,
    path_to_loaddata=path_to_loaddata,
)

