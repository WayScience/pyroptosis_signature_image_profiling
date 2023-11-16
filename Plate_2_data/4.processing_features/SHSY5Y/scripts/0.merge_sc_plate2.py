#!/usr/bin/env python
# coding: utf-8

# # Merge single cells from CellProfiler outputs using CytoTable

# In[1]:


import sys
import pathlib

from cytotable import convert, presets

sys.path.append("../../../utils")
import sc_extraction_utils as sc_utils


# ## Set paths and variables
# 
# All paths must be string but we use pathlib to show which variables are paths

# In[2]:


# type of file output from CytoTable (currently only parquet)
dest_datatype = "parquet"

# common configurations to use based on typical CellProfiler SQLite outputs
preset = "cellprofiler_sqlite_pycytominer"

# directory where parquet files are saved to
output_dir = pathlib.Path("./data/converted_data")
output_dir.mkdir(exist_ok=True, parents=True)


# In[3]:




# preset configurations based on typical CellProfiler outputs
preset = "cellprofiler_sqlite_pycytominer"
# remove Image_Metadata_Plate from SELECT as this metadata was not extracted from file names
# add Image_Metadata_Site as this is an important metadata when finding where single cells are located
presets.config["cellprofiler_sqlite_pycytominer"][
    "CONFIG_JOINS"
    # create filtered list of image features to be extracted and used for merging tables
    # with the list of image features, this will merge the objects together using the image number,
    # and parent objects to create all single cells (all objects associated to one cell)
] = """WITH Per_Image_Filtered AS (
                SELECT
                    Metadata_ImageNumber,
                    Image_Metadata_Plate,
                    Image_Metadata_Well,
                    Image_Metadata_Site
                FROM
                    read_parquet('per_image.parquet')
                )
            SELECT
                *
            FROM
                Per_Image_Filtered AS per_image
            LEFT JOIN read_parquet('per_cytoplasm.parquet') AS per_cytoplasm ON
                per_cytoplasm.Metadata_ImageNumber = per_image.Metadata_ImageNumber
            LEFT JOIN read_parquet('per_cells.parquet') AS per_cells ON
                per_cells.Metadata_ImageNumber = per_cytoplasm.Metadata_ImageNumber
                AND per_cells.Metadata_Cells_Number_Object_Number = per_cytoplasm.Metadata_Cytoplasm_Parent_Cells
            LEFT JOIN read_parquet('per_nuclei.parquet') AS per_nuclei ON
                per_nuclei.Metadata_ImageNumber = per_cytoplasm.Metadata_ImageNumber
                AND per_nuclei.Metadata_Nuclei_Number_Object_Number = per_cytoplasm.Metadata_Cytoplasm_Parent_Nuclei
                """


# In[5]:


# sqlite_dir = pathlib.Path(
#     "/scratch/alpine/mlippincott@xsede.org/data/"
# ).resolve(strict=True)

sqlite_dir = pathlib.Path("/media/lippincm/c58d4f19-ae4d-4b78-8370-2c2639886da0/interstellar_data/70117_20230210MM1_Gasdermin514_CP_BC430856__2023-03-22T15_42_38-Measurement1/PBMC_SQLite_Outputs/"
).resolve(strict=True)



# dictionary with info for the sqlite file from each run
sqlite_info_dictionary = {
    "batch_1": {
        # path to outputted SQLite file
        "source_path": str(
            pathlib.Path(
                f"{sqlite_dir}/SHSY5Y_cells_incomplete_first_run.sqlite"
            )
        ),
        "dest_path": str(pathlib.Path(f"{output_dir}/SHSY5Y_cells_first_run.parquet")),
    },
    "batch_2": {
        # path to outputted SQLite file
        "source_path": str(
            pathlib.Path(
                f"{sqlite_dir}/SHSY5Y_cells_second_run.sqlite"
            )
        ),
        "dest_path": str(pathlib.Path(f"{output_dir}/SHSY5Y_cells_second_run.parquet")),
    },
}

   


# ## Convert SQLite file and merge single cells into parquet file
# 
# This was not run to completion as we use the nbconverted python file for full run.

# In[6]:


# run through each run with each set of paths based on dictionary
for sqlite_file, info in sqlite_info_dictionary.items():
    source_path = info["source_path"]
    dest_path = info["dest_path"]
    print(f"Performing merge single cells and conversion on {sqlite_file}!")

    # merge single cells and output as parquet file
    convert(
        source_path=source_path,
        dest_path=dest_path,
        dest_datatype=dest_datatype,
        preset=preset,
    )
    print(f"Merged and converted {pathlib.Path(dest_path).name}!")

    # add single cell count per well as metadata column to parquet file and save back to same path
    sc_utils.add_sc_count_metadata_file(
        data_path=dest_path, well_column_name="Image_Metadata_Well", file_type="parquet"
    )
    print(f"Added single cell count as metadata to {pathlib.Path(dest_path).name}!")

