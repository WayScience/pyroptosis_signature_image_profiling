#!/usr/bin/env python
# coding: utf-8

# # Combine both SHSY5Y run parquet files into one

# ## Import libraries

# In[1]:


import pandas as pd
import pathlib

from pycytominer.cyto_utils import output


# ## Set paths

# In[2]:


# set path to parquet directory
parquet_dir = pathlib.Path("./data")

# set paths to each individual run file after annotation
first_run_sc_path = pathlib.Path(f"{parquet_dir}/SHSY5Y_first_run_sc.parquet")
second_run_sc_path = pathlib.Path(f"{parquet_dir}/SHSY5Y_second_run_sc.parquet")

# set path for combined run parquet file
merged_runs_path = pathlib.Path(f"{parquet_dir}/SHSY5Y_sc.parquet")


# ## Combine the parquet files into one

# In[3]:


# read parquet files into pandas dataframes
first_run_sc = pd.read_parquet(first_run_sc_path)
second_run_sc = pd.read_parquet(second_run_sc_path)

# concatenate dataframes and save as parquet file
SHSY5Y_run_sc = pd.concat([first_run_sc, second_run_sc], ignore_index=True)
output(
    df=SHSY5Y_run_sc,
    output_filename=merged_runs_path,
    output_type="parquet",
)
print(f"The runs have been merged into one file called {merged_runs_path.name}!")


# In[ ]:


# check to see if the merge function worked (should be approximately 600,000 rows)
print(SHSY5Y_run_sc.shape)
SHSY5Y_run_sc.head()

