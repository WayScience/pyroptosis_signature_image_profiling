#!/usr/bin/env python
# coding: utf-8

# # Merge single cells from CellProfiler outputs using CytoTable

# In[ ]:


import sys
import pathlib

from cytotable import convert

sys.path.append("../../utils")
import sc_extraction_utils as sc_utils
from parsl.config import Config
from parsl.executors import HighThroughputExecutor


# ## Set paths and variables
# 
# All paths must be string but we use pathlib to show which variables are paths

# In[ ]:


# type of file output from CytoTable (currently only parquet)
dest_datatype = "parquet"

# common configurations to use based on typical CellProfiler SQLite outputs
preset = "cellprofiler_sqlite_pycytominer"

# directory where parquet files are saved to
output_dir = pathlib.Path("./data/converted_data")
output_dir.mkdir(exist_ok=True, parents=True)


# In[ ]:


# set directory for sqlite files
sqlite_dir = pathlib.Path(
    "/home/lippincm/Desktop/18T/interstellar_data/SHSY5Y_SQLite_Outputs/"
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
        "dest_path": str(pathlib.Path(f"{output_dir}/SHSY5Y_batch_1.parquet")),
    },
    "batch_2": {
        # path to outputted SQLite file
        "source_path": str(
            pathlib.Path(
                f"{sqlite_dir}/SHSY5Y_cells_second_run.sqlite"
            )
        ),
        "dest_path": str(pathlib.Path(f"{output_dir}/SHSY5Y_batch_2.parquet")),
    },
}


# ## Convert SQLite file and merge single cells into parquet file
# 
# This was not run to completion as we use the nbconverted python file for full run.

# In[ ]:


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
        parsl_config=Config(
            executors=[HighThroughputExecutor()],
        ),
        chunk_size=10000,
    )
    print(f"Merged and converted {pathlib.Path(dest_path).name}!")

    # add single cell count per well as metadata column to parquet file and save back to same path
    sc_utils.add_sc_count_metadata_file(
        data_path=dest_path, well_column_name="Image_Metadata_Well", file_type="parquet"
    )
    print(f"Added single cell count as metadata to {pathlib.Path(dest_path).name}!")

