#!/usr/bin/env python
# coding: utf-8

# # Extract image features
# 
# **Note:** This does not include any processing of the features (e.g. normalization/feature selection/etc.)

# ## Import libraries

# In[ ]:


import pathlib
import pandas as pd

from pycytominer import annotate
from pycytominer.cyto_utils import output

import sys
sys.path.append("../../../utils")
import extract_image_features_utils as extract_utils


# ## Set paths and constants

# In[ ]:


# Set file and directory constants
cp_output_dir = pathlib.Path("../../3.cellprofiler_analysis/analysis_output")
features_output_dir = pathlib.Path("./data")
platemap_df = pd.read_csv(pathlib.Path("../../../metadata/Interstellar_plate2_platemap.csv"))

# image categories/measurements to extract
image_feature_categories = ["Image_Correlation", "Image_Granularity", "Image_Texture", "Image_Intensity"]
image_cols="ImageNumber"
# strata are the columns that can be used to groupby and/or aggregate, but I use it to make sure I have all
# metadata I need to use to identify what exact image the features come from
strata=["Image_Metadata_Well", "Image_Metadata_Plate", "Image_Metadata_Site"]

# set directory for sqlite files
sqlite_dir = pathlib.Path(
    "/projects/mlippincott@xsede.org/"
).resolve(strict=True)

# dictionary with info for the sqlite file from each run
run_info_dictionary = {
    "batch_1": {
        # path to outputted SQLite file
        "source_path": str(
            pathlib.Path(
                f"{sqlite_dir}/PBMC_batch_1.sqlite"
            )
        ),
        "dest_path": str(pathlib.Path(f"{features_output_dir}/PBMC_batch_1_image_quality.parquet")),
    },
    "batch_2": {
        # path to outputted SQLite file
        "source_path": str(
            pathlib.Path(
                f"{sqlite_dir}/PBMC_batch_2.sqlite"
            )
        ),
        "dest_path": str(pathlib.Path(f"{features_output_dir}/PBMC_batch_2_image_quality.parquet")),
    },
    "batch_3": {
        # path to outputted SQLite file
        "source_path": str(
            pathlib.Path(
                f"{sqlite_dir}/PBMC_batch_3.sqlite"
            )
        ),
        "dest_path": str(pathlib.Path(f"{features_output_dir}/PBMC_batch_3.parquet")),
    },
    "batch_4": {
        # path to outputted SQLite file
        "source_path": str(
            pathlib.Path(
                f"{sqlite_dir}/PBMC_batch_4.sqlite"
            )
        ),
        "dest_path": str(pathlib.Path(f"{features_output_dir}/PBMC_batch_4.parquet")),
    },
    "batch_5": {
        # path to outputted SQLite file
        "source_path": str(
            pathlib.Path(
                f"{sqlite_dir}/PBMC_batch_5.sqlite"
            )
        ),
        "dest_path": str(pathlib.Path(f"{features_output_dir}/PBMC_batch_5.parquet")),
    },
    "batch_6": {
        # path to outputted SQLite file
        "source_path": str(
            pathlib.Path(
                f"{sqlite_dir}/PBMC_batch_6.sqlite"
            )
        ),
        "dest_path": str(pathlib.Path(f"{features_output_dir}/PBMC_batch_6.parquet")),
    },
    "batch_7": {
        # path to outputted SQLite file
        "source_path": str(
            pathlib.Path(
                f"{sqlite_dir}/PBMC_batch_7.sqlite"
            )
        ),
        "dest_path": str(pathlib.Path(f"{features_output_dir}/PBMC_batch_7.parquet")),
    }   
}


# ## Load in the `Per_Image` table as df for both SQLite files (each run) and combine into one df

# In[ ]:


# read in SQLite Per_Image table as dataframe for each run
## First run
sql_file_first_run = run_info_dictionary["batch_1"]["source_path"]
single_cell_file_first_run = f"sqlite:///{cp_output_dir}/{sql_file_first_run}"
image_df_first_run = extract_utils.load_sqlite_as_df(
    sqlite_file_path=single_cell_file_first_run, image_table_name="Per_Image"
)

## Second run
sql_file_second_run = run_info_dictionary["batch_2"]["source_path"]
single_cell_file_second_run = f"sqlite:///{cp_output_dir}/{sql_file_second_run}"
image_df_second_run = extract_utils.load_sqlite_as_df(
    sqlite_file_path=single_cell_file_second_run, image_table_name="Per_Image"
)

## Third run
sql_file_third_run = run_info_dictionary["batch_3"]["source_path"]
single_cell_file_third_run = f"sqlite:///{cp_output_dir}/{sql_file_third_run}"
image_df_third_run = extract_utils.load_sqlite_as_df(
    sqlite_file_path=single_cell_file_third_run, image_table_name="Per_Image"
)

## Fourth run
sql_file_fourth_run = run_info_dictionary["batch_4"]["source_path"]
single_cell_file_fourth_run = f"sqlite:///{cp_output_dir}/{sql_file_fourth_run}"
image_df_fourth_run = extract_utils.load_sqlite_as_df(
    sqlite_file_path=single_cell_file_fourth_run, image_table_name="Per_Image"
)

## Fifth run
sql_file_fifth_run = run_info_dictionary["batch_5"]["source_path"]
single_cell_file_fifth_run = f"sqlite:///{cp_output_dir}/{sql_file_fifth_run}"
image_df_fifth_run = extract_utils.load_sqlite_as_df(
    sqlite_file_path=single_cell_file_fifth_run, image_table_name="Per_Image"
)

## Sixth run
sql_file_sixth_run = run_info_dictionary["batch_6"]["source_path"]
single_cell_file_sixth_run = f"sqlite:///{cp_output_dir}/{sql_file_sixth_run}"
image_df_sixth_run = extract_utils.load_sqlite_as_df(
    sqlite_file_path=single_cell_file_sixth_run, image_table_name="Per_Image"
)

## Seventh run
sql_file_seventh_run = run_info_dictionary["batch_7"]["source_path"]
single_cell_file_seventh_run = f"sqlite:///{cp_output_dir}/{sql_file_seventh_run}"
image_df_seventh_run = extract_utils.load_sqlite_as_df(
    sqlite_file_path=single_cell_file_seventh_run, image_table_name="Per_Image"
)





# merge the dataframes together into one combined run
PBMC_run_df = pd.concat([image_df_first_run, image_df_second_run, image_df_third_run, image_df_fourth_run, image_df_fifth_run, image_df_sixth_run, image_df_seventh_run], ignore_index=True)

print(PBMC_run_df.shape)
PBMC_run_df.head()


# ## Extract the image features, annotate with metadata, and save as parquet file

# In[ ]:


# extract image quality features from merged PBMC runs image table df
image_features_df = extract_utils.extract_image_features(
    image_feature_categories=image_feature_categories,
    image_df=PBMC_run_df,
    image_cols=image_cols,
    strata=strata
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
    output_filename=pathlib.Path(f"{features_output_dir}/plate2_PBMC_image_features.parquet"),
    output_type='parquet',
)
print("The image features for the PBMC cells have been extracted and saved!")


# ## Confirm that the annotation worked
# 
# Check to see that data doesn't show NaNs when there should be values.

# In[ ]:


print(annotated_image_features_df.shape)
annotated_image_features_df.head()


# In[ ]:


annotated_image_features_df["Metadata_inhibitor"].unique()


# In[ ]:


annotated_image_features_df[annotated_image_features_df["Metadata_inhibitor"] == "DMSO"]

