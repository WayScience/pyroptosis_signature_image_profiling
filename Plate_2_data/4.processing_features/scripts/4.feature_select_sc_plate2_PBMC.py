#!/usr/bin/env python
# coding: utf-8

# # Perform feature selection on normalized data

# ## Import libraries

# In[ ]:


import sys
import pathlib
import gc
import pandas as pd

from pycytominer import feature_select
from pycytominer.cyto_utils import output


# ## Set paths and variables

# In[ ]:


# directory where normalized parquet file is located
data_dir = pathlib.Path("./data/normalized_data")

# directory where the feature selected parquet file is saved to
output_dir = pathlib.Path("./data/feature_selected_data")
output_dir.mkdir(exist_ok=True)

# define input path
normalized_file_path = str(pathlib.Path(f"{data_dir}/PBMC_sc_norm.parquet"))

# define ouput path
feature_select_output_file = str(pathlib.Path(f"{output_dir}/PBMC_sc_norm_fs.parquet"))


# In[ ]:


# process each run
normalized_df = pd.read_parquet(normalized_file_path)


# In[ ]:


normalized_df.shape


# ## Perform feature selection

# In[ ]:


# list of operations for feature select function to use on input profile
feature_select_ops = [
    "variance_threshold",
    "blocklist",
    "drop_na_columns",
]

print(f"Performing feature selection on normalized annotated merged single cells!")

# perform feature selection with the operations specified
feature_select_df = feature_select(
    normalized_df,
    operation=feature_select_ops,
)

del normalized_df
gc.collect()


# In[ ]:


print(feature_select_df.shape)


# In[ ]:


# Assuming 'well' is the column you want to stratify by
feature_select_df = feature_select_df.groupby('Metadata_Well').apply(lambda x: x.sample(frac=0.01, random_state=0)).reset_index(drop=True)
print(feature_select_df.shape)


# In[ ]:


feature_select_ops = [
    "correlation_threshold",
]
# perform feature selection with the operations specified
feature_select_df = feature_select(
    feature_select_df,
    operation=feature_select_ops,
)
print(feature_select_df.shape)
# get the column names of the feature selected dataframe
feature_select_df_columns = feature_select_df.columns.tolist()


# In[ ]:


# reload the normalized dataframe
normalized_df = pd.read_parquet(normalized_file_path)
# filter the normalized dataframe to only include the columns that were selected
feature_select_df = normalized_df.reindex(columns=feature_select_df_columns)
print(feature_select_df.shape)


# In[ ]:


# save features selected df as parquet file
output(
    df=feature_select_df,
    output_filename=feature_select_output_file,
    output_type="parquet"
)
print(f"Features have been selected for PBMC cells and saved to {pathlib.Path(feature_select_output_file).name}!")


# In[ ]:


# check to see if the shape of the df has changed indicating feature selection occurred
print(feature_select_df.shape)
feature_select_df.head()


# In[ ]:


# seperate the metadata and profile data
metadata_cols = feature_select_df.columns[feature_select_df.columns.str.contains("Metadata")]
profile_cols = feature_select_df.columns[~feature_select_df.columns.str.contains("Metadata")]
print(len(metadata_cols))
print(len(profile_cols))
print(len(normalized_df.columns)-len(metadata_cols))

