#!/usr/bin/env python
# coding: utf-8

# # Create LoadData csv with IC functions and run CellProfiler `analysis.cppipe` pipeline - Wave 1

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

# ## Set paths for `pe2loaddata`
# 

# In[2]:


# path to the directory for the plate containing the images and index file
index_directory = pathlib.Path("../0.download_data/70117_20230118MM1_AbTest_V2__2023-01-25T16_44_54-Measurement1/Images").absolute()
# path to the config file to extract metadata and create LoadData CSV from
config_path = pathlib.Path("../1.cellprofiler_ic_processing/config.yml").absolute()
# path to the original LoadData CSV
path_to_loaddata = pathlib.Path("../1.cellprofiler_ic_processing/wave1_loaddata.csv").absolute()
# path to directory with IC function for both channels
illum_directory = pathlib.Path("../1.cellprofiler_ic_processing/illum_directory").absolute()
# plate name for this wave of data
plate_id = "70117_20230118MM1_AbTest_V2"
# path for LoadData CSV with the paths for IC functions
illum_loaddata_output_path = pathlib.Path("./wave1_loaddata_with_illum.csv").absolute()


# ## Set paths and dictionary for CellProfiler `analysis.cppipe` run

# In[3]:


# path for the output directory
path_to_output = pathlib.Path("./analysis_output").absolute()

# dictionary with variables for each dilation
dilation_info_dictionary = {
    "dilation_25": {
        "path_to_pipeline": pathlib.Path("./pipelines/wave1_analysis_dilate25.cppipe").absolute(),
        "sqlite_name": "dilate25",
    },
    "dilation_50": {
        "path_to_pipeline": pathlib.Path("./pipelines/wave1_analysis_dilate50.cppipe").absolute(),
        "sqlite_name": "dilate50",
    },
    "dilation_75": {
        "path_to_pipeline": pathlib.Path("./pipelines/wave1_analysis_dilate75.cppipe").absolute(),
        "sqlite_name": "dilate75",
    },
}


# ## Create the LoadData csv with IC functions

# In[4]:


ld.create_loaddata_illum_csv(
    index_directory=index_directory,
    config_path=config_path,
    path_to_output=path_to_loaddata,
    illum_directory=illum_directory,
    plate_id=plate_id,
    illum_output_path=illum_loaddata_output_path,
)


# ## Run CellProfiler `analysis.cppipe` pipelines for each dilation

# In[5]:


for dilation, info in dilation_info_dictionary.items():
    # set the parameters for the function as variables based on the dilation dictionary info
    path_to_pipeline = info["path_to_pipeline"]
    sqlite_name = info["sqlite_name"]

    # run CP analysis for each dilation
    cp.run_cellprofiler(
        path_to_pipeline=path_to_pipeline,
        path_to_output=path_to_output,
        path_to_loaddata=illum_loaddata_output_path,
        sqlite_name=sqlite_name,
        hardcode_sqlite_name="wave1",
        analysis_run=True,
    )

