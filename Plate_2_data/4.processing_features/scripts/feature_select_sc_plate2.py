#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import pathlib

import pandas as pd
from pycytominer import feature_select
from pycytominer.cyto_utils import output

sys.path.append("../../utils")
import sc_extraction_utils as sc_utils


# In[2]:


# output directory for annotated file
output_dir = pathlib.Path("./data/")

# dictionary with each run for the cell type
run_info_dictionary = {
    "SHSY5Y_first_run": {
        # path to parquet file from annotate function
        "normalized_path": str(pathlib.Path("./data/SHSY5Y_first_run_sc_norm.parquet"))
    },
    "SHSY5Y_second_run": {
        # path to parquet file from annotate function
        "normalized_path": str(pathlib.Path("./data/SHSY5Y_second_run_sc_norm.parquet")),
    },
}


# In[3]:


# list of operations for feature select function to use on input profile
feature_select_ops = [
    "variance_threshold",
    "correlation_threshold",
    "blocklist",
]

# process each run
for SHSY5Y_run, info in run_info_dictionary.items():
    normalized_df = pd.read_parquet(info["normalized_path"])
    output_file = str(pathlib.Path(f"{output_dir}/{SHSY5Y_run}_sc_norm_fs.parquet"))
    print(f"Performing feature selection on normalized annotated merged single cells for {SHSY5Y_run}!")

    # perform feature selection with the operations specified
    feature_select_df = feature_select(
        normalized_df,
        operation=feature_select_ops,
        output_file="none",
    )

    # save features selected df as parquet file
    output(
        df=feature_select_df,
        output_filename=output_file,
        output_type="parquet"
    )
    print(f"Features have been selected for {SHSY5Y_run} and saved!")


# In[4]:


print(feature_select_df.shape)
feature_select_df.head()

