#!/usr/bin/env python
# coding: utf-8

# # Annotate merged single cells with metadata from platemap file

# ## Import libraries

# In[1]:


import sys
import pathlib

import pandas as pd
from pycytominer import annotate
from pycytominer.cyto_utils import output


# ## Set paths and variables

# In[2]:


# load in platemap file as a pandas dataframe
platemap_path = pathlib.Path("../../../metadata/Interstellar_plate2_platemap.csv")
platemap_df = pd.read_csv(platemap_path)

# directory where parquet files are located
data_dir = pathlib.Path("./data/converted_data")

# directory where the annotated parquet files are saved to
output_dir = pathlib.Path("./data/annotated_data")
output_dir.mkdir(exist_ok=True)


# In[3]:


# dictionary with each run for the cell type
# dictionary with path to the parquet file from each run
run_info_dictionary = {
    "batch_1": {
        # path to outputted parquet file
        "single_cell_path": str(
            pathlib.Path(
                f"{data_dir}/SHSY5Y_cells_first_run.parquet"
            )
        ),
    },
    "batch_2": {
        # path to outputted parquet file
        "single_cell_path": str(
            pathlib.Path(
                f"{data_dir}/SHSY5Y_cells_second_run.parquet"
            )
        )
    },
}


# ## Annotate merged single cells

# In[4]:


for SHSY5Y_run, info in run_info_dictionary.items():
    # load in converted parquet file as df to use in annotate function
    single_cell_df = pd.read_parquet(info["single_cell_path"])
    output_file = str(pathlib.Path(f"{output_dir}/SHSY5Y_{SHSY5Y_run}_sc.parquet"))
    print(f"Adding annotations to merged single cells for {SHSY5Y_run}!")

    # add metadata from platemap file to extracted single cell features
    annotated_df = annotate(
        profiles=single_cell_df,
        platemap=platemap_df,
        join_on=["Metadata_well_id", "Image_Metadata_Well"],
    )

    # move metadata well and single cell count to the front of the df (for easy visualization in python)
    well_column = annotated_df.pop("Metadata_Well")
    singlecell_column = annotated_df.pop("Metadata_number_of_singlecells")
    site_column = annotated_df.pop("Image_Metadata_Site")
    # insert the column as the second index column in the dataframe
    annotated_df.insert(1, "Metadata_Well", well_column)
    annotated_df.insert(2, "Metadata_number_of_singlecells", singlecell_column)
    annotated_df.insert(3, "Metadata_Site", site_column)

    # save annotated df as parquet file
    output(
        df=annotated_df,
        output_filename=output_file,
        output_type="parquet",
    )
    print(f"Annotations have been added to {SHSY5Y_run} and saved!")


# In[5]:


# check last annotated df to see if it has been annotated correctly
print(annotated_df.shape)
annotated_df.head()

