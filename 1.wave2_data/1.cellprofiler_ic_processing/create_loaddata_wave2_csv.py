#!/usr/bin/env python
# coding: utf-8

# # Create LoadData csv for CellProfiler `illum.cppipe` pipeline - Wave 2

# ## Import libraries

# In[1]:


import os
import pathlib

import sys
sys.path.append("../../utils")
import loaddata_utils as ld


# ## Set paths
# 
# **Note:** All paths must be absolute since CellProfiler will need to find the images based on your local machine. Please change the `/home/jenna` part of the path to reflect your machine.

# In[2]:


index_directory = pathlib.Path("/home/jenna/Interstellar_Project/1.wave2_data/0.download_data/70117_20230118MM1_AbTest_ASC__2023-01-27T13_47_00-Measurement1/Images")
config_path = pathlib.Path("/home/jenna/Interstellar_Project/1.wave2_data/1.cellprofiler_ic_processing/config.yml")
path_to_output = pathlib.Path("/home/jenna/Interstellar_Project/1.wave2_data/1.cellprofiler_ic_processing/wave2_loaddata.csv")


# ## Create the LoadData csv with illum correction functions

# In[3]:


ld.create_loaddata_csv(index_directory, config_path, path_to_output)

