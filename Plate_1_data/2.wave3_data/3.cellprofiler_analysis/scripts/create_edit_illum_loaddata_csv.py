#!/usr/bin/env python
# coding: utf-8

# # Create and edit LoadData csv for CellProfiler `analysis.cppipe` pipeline - Wave 3
# 
# This pipeline will create a LoadData csv with the illumination correction functions for each channel and then edited to remove rows that are not the last z-plane and correct the pathing to the maximum prjected images.

# ## Import libraries

# In[1]:


import pathlib

import sys
sys.path.append("../../utils")
import loaddata_utils as ld


# ## Set paths
# 
# **Note:** All paths must be absolute since CellProfiler will need to find the images based on your local machine. Please change the `/home/jenna` part of the path to reflect your machine.

# In[2]:


index_directory = pathlib.Path("/home/jenna/Interstellar_Project/2.wave3_data/0.download_data/70117_20230118MM1_CellPainting_A700_20X_V1__2023-02-06T09_42_13-Measurement1/Images")
# use config file from previous module since it doesn't change
config_path = pathlib.Path("/home/jenna/Interstellar_Project/2.wave3_data/1.cellprofiler_quality_control/config.yml")
path_to_output = pathlib.Path("/home/jenna/Interstellar_Project/2.wave3_data/2.cellprofiler_ic_processing/wave3_loaddata.csv")
illum_directory = pathlib.Path("/home/jenna/Interstellar_Project/2.wave3_data/2.cellprofiler_ic_processing/illum_directory")
plate_id = "70117_20230118MM1_CellPainting_A700_20X_V1"
illum_output_path = pathlib.Path("/home/jenna/Interstellar_Project/2.wave3_data/3.cellprofiler_analysis/wave3_loaddata_with_illum.csv")


# ## Create the LoadData csv with illum correction functions

# In[3]:


ld.create_loaddata_illum_csv(index_directory, config_path, path_to_output, illum_directory, plate_id, illum_output_path)


# ## Edit LoadData csv to remove unnecessary rows and correct paths to images

# In[4]:


# must be illum_output_path as this is the final output path for the csv
ld.edit_loaddata_csv(illum_output_path)

