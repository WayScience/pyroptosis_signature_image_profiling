#!/usr/bin/env python
# coding: utf-8

# # Perform feature selection on normalized data

# ## Import libraries

# In[1]:


import sys
import pathlib

import pandas as pd

from pycytominer import feature_select
from pycytominer.cyto_utils import output


# ## Set paths and variables

# In[2]:


# directory where normalized parquet file is located
data_dir = pathlib.Path("./data/normalized_data")

# directory where the feature selected parquet file is saved to
output_dir = pathlib.Path("./data/feature_selected_data")
output_dir.mkdir(exist_ok=True)

# define input path
normalized_file_path = str(pathlib.Path(f"{data_dir}/SHSY5Y_sc_norm.parquet"))

# define ouput path
feature_select_output_file = str(pathlib.Path(f"{output_dir}/SHSY5Y_sc_norm_fs.parquet"))


# ## Perform feature selection

# In[3]:


# list of operations for feature select function to use on input profile
feature_select_ops = [
    "variance_threshold",
    "correlation_threshold",
    "blocklist",
]

# process each run
normalized_df = pd.read_parquet(normalized_file_path)

print(f"Performing feature selection on normalized annotated merged single cells!")

# perform feature selection with the operations specified
feature_select_df = feature_select(
    normalized_df,
    operation=feature_select_ops,
)

# save features selected df as parquet file
output(
    df=feature_select_df,
    output_filename=feature_select_output_file,
    output_type="parquet"
)
print(f"Features have been selected for SHSY5Y cells and saved to {pathlib.Path(feature_select_output_file).name}!")


# In[4]:


# check to see if the shape of the df has changed indicating feature selection occurred
print(feature_select_df.shape)
feature_select_df.head()

