#!/usr/bin/env python
# coding: utf-8

# # Normalize annotated single cells using negative control (DSMO 0.025% and DMSO 0.100%)

# ## Import libraries

# In[1]:


import pandas as pd
import pathlib

from pycytominer import normalize
from pycytominer.cyto_utils import output

import sys
sys.path.append("../../utils")
import sc_extraction_utils as sc_utils


# ## Set paths and variables

# In[2]:


# output directory for annotated file
output_dir = pathlib.Path("./data/")

# dictionary with each run for the cell type
run_info_dictionary = {
    "SHSY5Y_first_run": {
        # path to parquet file from annotate function
        "annotated_path": str(pathlib.Path("./data/SHSY5Y_first_run_sc.parquet"))
    },
    "SHSY5Y_second_run": {
        # path to parquet file from annotate function
        "annotated_path": str(pathlib.Path("./data/SHSY5Y_second_run_sc.parquet")),
    },
}


# ## Normalize with standardize method with negative control on annotated data

# In[3]:


# process each run
for SHSY5Y_run, info in run_info_dictionary.items():
    annotated_df = pd.read_parquet(info["annotated_path"])
    output_file = str(pathlib.Path(f"{output_dir}/{SHSY5Y_run}_sc_norm.parquet"))
    print(f"Normalizing annotated merged single cells for {SHSY5Y_run}!")

    # normalize annotated data
    normalized_df = normalize(
            profiles=annotated_df,
            samples="Metadata_inhibitor == 'DMSO' and Metadata_inhibitor_concentration == 0.025 and Metadata_inducer1 == 'DMSO'",
            method="standardize",
    )

    # save df as parquet file
    output(
        df=normalized_df,
        output_filename=output_file,
        output_type="parquet",
    )
    print(f"Single cells have been normalized for {SHSY5Y_run} and saved!")


# In[4]:


print(normalized_df.shape)
normalized_df.head()

