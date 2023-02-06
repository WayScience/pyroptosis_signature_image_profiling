#!/usr/bin/env python
# coding: utf-8

# # Create LoadData with illumination correction functions csv for CellProfiler

# ## Import libraries

# In[1]:


import os
import pathlib


# ## Helper function to run `pe2loaddata`

# In[2]:


def create_loaddata_illum_csv(
    index_directory: pathlib.Path,
    config_path: pathlib.Path,
    path_to_output: pathlib.Path,
    illum_directory:pathlib.Path,
    plate_id:str,
    illum_output_path:pathlib.Path,
):
    """
    Create LoadData csv with illum correction functions for CellProfiler

    Parameters
    ----------
    index_directory : pathlib.Path
        path to the `Index.idx.xml` file for the plate (normally located in the /Images folder)
    config_path : pathlib.Path
        path to the `config.yml' file for pe2loaddata to process the csv
    path_to_output : pathlib.Path
        path to the `wave1_loaddata.csv' file used for generating the illumination correction functions for each channel
    illum_directory : pathlib.Path
        path to folder where the illumination correction functions (.npy files) are located
    plate_id : str
        string of the name of the plate to create the csv
    illum_output_path : pathlib.Path
        path to where the new csv will be created along with the name (e.g. path/to/wave1_loaddata_with_illum.csv)
    """
    command = f"pe2loaddata --index-directory {index_directory} {config_path} {path_to_output} --illum --illum-directory {illum_directory} --plate-id {plate_id} --illum-output {illum_output_path}"
    os.system(command)
    print(f'{illum_output_path.name} is created!')


# ## Set paths
# 
# **Note:** All paths must be absolute since CellProfiler will need to find the images based on your local machine. Please change the `/home/jenna` part of the path to reflect your machine.

# In[3]:


index_directory = pathlib.Path("/home/jenna/Interstellar_Project/0.wave1_data/0.download_data/70117_20230118MM1_AbTest_V2__2023-01-25T16_44_54-Measurement1/Images")
config_path = pathlib.Path("/home/jenna/Interstellar_Project/0.wave1_data/1.cellprofiler_ic_processing/config.yml")
path_to_output = pathlib.Path("/home/jenna/Interstellar_Project/0.wave1_data/1.cellprofiler_ic_processing/wave1_loaddata.csv")
illum_directory = pathlib.Path("/home/jenna/Interstellar_Project/0.wave1_data/1.cellprofiler_ic_processing/illum_directory")
plate_id = "70117_20230118MM1_AbTest_V2"
illum_output_path = pathlib.Path("/home/jenna/Interstellar_Project/0.wave1_data/2.cellprofiler_analysis/wave1_loaddata_with_illum.csv")


# ## Create the LoadData csv with illum correction functions

# In[4]:


create_loaddata_illum_csv(index_directory, config_path, path_to_output, illum_directory, plate_id, illum_output_path)

