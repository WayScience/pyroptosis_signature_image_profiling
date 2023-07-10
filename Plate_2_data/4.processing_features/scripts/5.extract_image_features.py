#!/usr/bin/env python
# coding: utf-8

# # Extract image features
#
# **Note:** This does not include any processing of the features (e.g. normalization/feature selection/etc.)

# ## Import libraries

# In[1]:


import pathlib
import pandas as pd

from pycytominer import annotate
from pycytominer.cyto_utils import output

import sys

sys.path.append("../../utils")
import extract_image_features_utils as extract_utils


# ## Set paths and constants

# In[2]:


# Set file and directory constants
cp_output_dir = pathlib.Path("../3.cellprofiler_analysis/analysis_output")
features_output_dir = pathlib.Path("./data")
platemap_df = pd.read_csv(
    pathlib.Path("../../metadata/Interstellar_plate2_platemap.csv")
)

# image categories/measurements to extract
image_feature_categories = [
    "Image_Correlation",
    "Image_Granularity",
    "Image_Texture",
    "Image_Intensity",
]
image_cols = "ImageNumber"
# strata are the columns that can be used to groupby and/or aggregate, but I use it to make sure I have all
# metadata I need to use to identify what exact image the features come from
strata = ["Image_Metadata_Well", "Image_Metadata_Plate", "Image_Metadata_Site"]

run_info_dictionary = {
    "SHSY5Y_first_run": {
        "sql_file": "SHSY5Y_cells_incomplete_first_run.sqlite",
        "image_features_output_file": pathlib.Path(
            f"{features_output_dir}/frist_run_image_quality.csv.gz"
        ),
    },
    "SHSY5Y_second_run": {
        "sql_file": "SHSY5Y_cells_second_run.sqlite",
        "image_features_output_file": pathlib.Path(
            f"{features_output_dir}/second_run_image_quality.csv.gz"
        ),
    },
}


# ## Load in the `Per_Image` table as df for both SQLite files (each run) and combine into one df

# In[3]:


# read in SQLite Per_Image table as dataframe for each run
## First run
sql_file_first_run = run_info_dictionary["SHSY5Y_first_run"]["sql_file"]
single_cell_file_first_run = f"sqlite:///{cp_output_dir}/{sql_file_first_run}"
image_df_first_run = extract_utils.load_sqlite_as_df(
    sqlite_file_path=single_cell_file_first_run, image_table_name="Per_Image"
)
## Second run
sql_file_second_run = run_info_dictionary["SHSY5Y_second_run"]["sql_file"]
single_cell_file_second_run = f"sqlite:///{cp_output_dir}/{sql_file_second_run}"
image_df_second_run = extract_utils.load_sqlite_as_df(
    sqlite_file_path=single_cell_file_second_run, image_table_name="Per_Image"
)

# merge the dataframes together into one combined run
SHSY5Y_run_df = pd.concat([image_df_first_run, image_df_second_run], ignore_index=True)

print(SHSY5Y_run_df.shape)
SHSY5Y_run_df.head()


# ## Extract the image features, annotate with metadata, and save as parquet file

# In[4]:


# extract image quality features from merged SHSY5Y runs image table df
image_features_df = extract_utils.extract_image_features(
    image_feature_categories=image_feature_categories,
    image_df=SHSY5Y_run_df,
    image_cols=image_cols,
    strata=strata,
)

# annotate df with platemap file to include all metadata
annotated_image_features_df = annotate(
    profiles=image_features_df,
    platemap=platemap_df,
    join_on=["Metadata_well_id", "Image_Metadata_Well"],
    output_file="none",
)

# output df as parquet file
output(
    df=annotated_image_features_df,
    output_filename=pathlib.Path(
        f"{features_output_dir}/plate2_SHSY5Y_image_features.parquet"
    ),
    output_type="parquet",
)
print("The image features for the SHSY5Y cells have been extracted and saved!")


# ## Confirm that the annotation worked
#
# Check to see that data doesn't show NaNs when there should be values.

# In[5]:


print(annotated_image_features_df.shape)
annotated_image_features_df.head()


# In[6]:


annotated_image_features_df["Metadata_inhibitor"].unique()


# In[7]:


annotated_image_features_df[annotated_image_features_df["Metadata_inhibitor"] == "DMSO"]
