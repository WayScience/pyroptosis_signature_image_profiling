#!/usr/bin/env python
# coding: utf-8

# # Merge single cells from CellProfiler outputs using CytoTable

# In[1]:


import sys
import pathlib

from cytotable import convert

sys.path.append("../../utils")
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
output_dir = "data"


# In[3]:


# dictionary with info for the sqlite file from each run
sqlite_info_dictionary = {
    "SHSY5Y_first_run": {
        # path to outputed SQLite file
        "source_path": str(
            pathlib.Path(
                "../3.cellprofiler_analysis/analysis_output/SHSY5Y_cells_incomplete_first_run.sqlite"
            )
        ),
        "dest_path": str(pathlib.Path(f"{output_dir}/SHSY5Y_first_run.parquet")),
    },
    "SHSY5Y_second_run": {
        # path to outputed SQLite file
        "source_path": str(
            pathlib.Path(
                "../3.cellprofiler_analysis/analysis_output/SHSY5Y_cells_second_run.sqlite"
            )
        ),
        # path for merged single cell paraquet file (without annotations)
        "dest_path": str(pathlib.Path(f"{output_dir}/SHSY5Y_second_run.parquet")),
    },
}


# ## Convert SQLite file and merge single cells into parquet file
#
# This was not run to completion as we use the nbconverted python file for full run.

# In[4]:


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
