#!/usr/bin/env python
# coding: utf-8

# # Create and edit LoadData csv with illumination correction (IC) functions and run CellProfiler `analysis.cppipe` pipeline
# 
# In this notebook, we create a LoadData CSV with the raw data along with the respective IC functions, remove all rows except rows with the last z-plane, and correct the paths from the raw images to the maximum projected images.
# 
# We then run the CellProfiler analysis pipeline to perform IC on the images, segmentation, and feature extraction to output CSV files.

# ## Import libraries

# In[1]:


import pathlib

import sys
sys.path.append("../../utils")
import loaddata_utils as ld_utils
import cp_utils as cp_utils


# ## Set paths and variables
# 
# For these paths, we create absolute paths (which has not been tested yet) and then use `resolve()` to avoid using the symlink paths from the `absolute()` function.

# In[2]:


# set paths for pe2loaddata
## path to raw data with index file
index_directory = pathlib.Path("../0.download_data/70117_20230210MM1_Gasdermin514_CP_BC430856__2023-03-22T15_42_38-Measurement1/Images/").absolute().resolve()
## path to config file (used for all modules)
config_path = pathlib.Path("../1.cellprofiler_quality_control/config.yml").absolute().resolve()
## path for the CSV file without IC (path to old)
path_to_output_csv = pathlib.Path("./loaddata_no_ic.csv").absolute().resolve()
## path to directory with IC functions (npy files)
illum_directory = pathlib.Path("../2.cellprofiler_ic_processing/illum_directory").absolute().resolve()
## plate ID from the names of the IC functions
plate_id = "*70117_20230210MM1_Gasdermin514_CP_BC430856"


# In[3]:


# set paths and variables to split the LoadData CSV by cell type
output_dir = pathlib.Path("./loaddata_by_celltype/").absolute().resolve()
col_metadata_name = "Metadata_Col"
col_val_to_split = 12
first_csv_name = "loaddata_PBMC_with_illum"
second_csv_name = "loaddata_SHSY5Y_with_illum"


# In[4]:


# set path to LoadData CSV with IC function used by pe2loaddata and split function
path_to_output_with_illum_csv = pathlib.Path("./loaddata_with_illum.csv").absolute().resolve()


# In[5]:


# set paths for CellProfiler
## path to folder for IC functions
path_to_output = pathlib.Path("./analysis_output/").absolute().resolve()
## hardcoded name for output
hardcode_sqlite_name = "interstellar_plate2"

## dictionary with paths for each cell type 
celltype_info_dictionary = {
    "SHSY5Y_cells": {
        "path_to_pipeline": pathlib.Path("./pipelines/SHSY5Y_analysis.cppipe").absolute().resolve(),
        "path_to_loaddata": pathlib.Path("./loaddata_by_celltype/loaddata_SHSY5Y_with_illum.csv").absolute().resolve(),
    },
    "PBMC_cells": {
        "path_to_pipeline": pathlib.Path("./pipelines/PBMC_analysis.cppipe").absolute().resolve(), 
        "path_to_loaddata": pathlib.Path("./loaddata_by_celltype/loaddata_PBMC_with_illum.csv").absolute().resolve(),
    },
}


# ## Create the LoadData csv with illum correction functions

# In[6]:


ld_utils.create_loaddata_illum_csv(
    index_directory=index_directory,
    config_path=config_path,
    path_to_output=path_to_output_csv,
    illum_directory=illum_directory,
    plate_id=plate_id,
    illum_output_path=path_to_output_with_illum_csv
)


# ## Edit LoadData CSV with IC functions to remove unnecessary rows and correct paths to max projection images

# In[7]:


ld_utils.edit_loaddata_csv(path_to_loaddata_csv=path_to_output_with_illum_csv)


# ## Split the corrected LoadData CSV by cell type
# 
# Since each cell type differ greatly in shape and size, we need to run separate CellProfiler pipelines as the segmentation parameters will be need to be optimized for each.

# In[8]:


ld_utils.split_loaddata_csv_by_col(
    path_to_loadata=path_to_output_with_illum_csv,
    output_dir=output_dir,
    col_metadata_name=col_metadata_name,
    col_val_to_split=col_val_to_split,
    first_csv_name=first_csv_name,
    second_csv_name=second_csv_name,
)


# ## Run CellProfiler analysis pipeline for each cell type
# 
# In this notebook, we do not run the full pipelines as we use the python file to complete the whole run.

# In[9]:


# run through each plate with each set of paths based on dictionary
for cell_type, info in celltype_info_dictionary.items():
    path_to_pipeline = info["path_to_pipeline"]
    path_to_loaddata = info["path_to_loaddata"]
    print(f"Running analysis on {cell_type}!")

    # run analysis pipeline
    cp_utils.run_cellprofiler(
        path_to_pipeline=path_to_pipeline,
        path_to_output=path_to_output,
        path_to_loaddata=path_to_loaddata,
        # name each SQLite file name from each CellProfiler pipeline
        sqlite_name=cell_type,
        # make analysis_run True to run an analysis pipeline
        analysis_run=True,
    )

